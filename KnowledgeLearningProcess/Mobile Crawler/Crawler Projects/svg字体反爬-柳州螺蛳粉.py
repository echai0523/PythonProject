# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 10:01

input: 
output: 
Short Description: 
    - Steamoat 反爬虫练习 (链接：http://www.porters.vip/confusion/food.html)
        - 在food.html主页面源码内，获取获取css接口、class属性名；
        - css请求响应获取svg接口、字体class名及对应的坐标；
        - 提取svg图片中字体大小、x的文本、y的文本；
        - 二分查找法bisect(a,b,lo,li) (链接：https://docs.python.org/zh-cn/3/library/bisect.html)
Change History:

"""
import requests, re
from lxml import etree
from bisect import bisect


class cssSvg():
    def __init__(self):
        self.headers = {
            'user-agent': '添加ua'
        }
        # 用于拼接
        self.prefix = 'http://www.porters.vip/confusion'
        self.lamBda = lambda x: x[0] if x else []

    def parse(self, url):
        response = requests.get(url, headers=self.headers)
        if response.ok:
            return response.text

    def dispose_css(self, response):
        """
        在food.html主页面源码内，获取内容
        :param response: food.html主页面的响应
        :return: svg接口、字体class名及对应的坐标
        """
        """在food.html主页面源码内，获取css接口、class属性名"""
        # css接口
        href = re.findall('<link href="(.*?)" rel="stylesheet">', response)[1]
        css_url = self.prefix + href.strip('.')
        # class属性名
        selector = etree.HTML(response)
        labelList = selector.xpath('//div[@class="col details"]/div')
        # className推导式结果['vhk6zl', 'vhk9or', ···, 'vhk6zl'] <class 'list'>
        # 使用推导式问题：['', ]内部<class 'lxml.etree._ElementUnicodeResult'>而不是<class 'str'>,但不影响使用也可以str(c)转字符串。
        className = [c for s in labelList for c in s.xpath('.//d/@class') if c != '']
        print('className: ', className)

        """css响应：提取svg接口、class名对应的坐标"""
        cssResponse = self.parse(css_url)
        # svg接口
        svg_url = self.prefix + re.findall('background-image: url\(..(.*)\);', cssResponse)[0]
        # 去空换行方便提取
        res = re.sub('[ \n]', '', cssResponse)
        # 提取className对应的坐标 [[('274', '141')], [('7', '15')], [('133', '97')]···]
        fontXy = [re.findall('.%s{background:-(\d+)px-(\d+)px;}' % name, res) for name in className]
        # 形成映射{'vhk08k': ('274', '141'), 'vhk6zl': ('7', '15'), 'vhk0ao': ('133', '97')}
        classXy = {}
        for k, v in zip(className, fontXy):
            classXy[k] = self.lamBda(v)

        print('classXy: ', classXy)
        # svg_url用于获取svg坐标数据, classXy用于解析svg字体
        return svg_url, classXy

    def dispose_svg(self, svg_url):
        """
        提取svg图片中字体大小、x的文本、y的文本
        :param svg_url: svg接口
        :return: 字体大小、x的文本、y的值、y的文本
        """
        response = self.parse(svg_url)
        """svg响应：提取字体大小、x的文本、y的文本"""
        # 字体大小
        fontSize = int(re.findall('font-size:(\d+)px;', response)[0])
        print('fontSize: ', fontSize)
        # x的文本
        textXy = re.findall('<text x="(.*) " y="(.*)">(.*)</text>', response)

        x = []
        yValues = []
        y = []
        for text in textXy:
            # 使用字体大小的方法获取索引值，不使用classX在x数据中的索引判断在y中取值
            x.append([int(x) for x in text[0].split(' ')])  # [[int]]
            yValues.append(int(text[1]))  # [int]
            y.append(text[2])  # [str]
        print('x =', x)
        print('y =', y)
        print('yValues =', yValues)

        return fontSize, x, y, yValues

    def core(self, classXy, fontSize, x, y, yValues):
        """
        解析判断 class属性名 下的 对应的值(str)
        :param classXy: {str:(str(x), str(y))},class名映射xy坐标
        :param fontSize: int, svg图片文字大小
        # :param x: [[int]], [x的数据]
        :param y: [[int]], [y的数据]
        :param yValues: [[int]], [y的值]
        :return: 最终值 str
        """
        """
        1. svg响应：[x的数据] -对应-> [y的值] -对应-> [y的数据]
        2. 先根据class的坐标y与svg响应[y的值]做比较
        3. 判断x取哪一个[x的数据]的索引 >决定> [y的数据]取该索引下的值
        4. 再根据获取的索引 获取 [y的数据]
        """
        result = {}
        for name, Xy in classXy.items():
            print('当前class名：', name, 'Xy:', Xy)
            if Xy == []:
                result[name] = ' '
            else:
                coordinateX = int(Xy[0])
                coordinateY = int(Xy[1])

                # 二分查找法 bisect(a,b,lo,li) # a是列表，b是元素值，lo,li设置查找区间
                # bisect默认bisect_right,a中存在b则返回b的索引，若不存在，返回大于b的元素索引
                # 参考：'https://docs.python.org/zh-cn/3/library/bisect.html'
                # bisect(yValues, coordinateY)：查看y坐标在第几行(索引)
                # x[bisect(yValues, coordinateY)]： x中的第几行数据
                # bisect(x[bisect(yValues, coordinateY)], coordinateX)： 查看x坐标在第几个元素(索引)
                result[name] = y[bisect(yValues, coordinateY)][bisect(x[bisect(yValues, coordinateY)], coordinateX)]

        print('result:', result)
        return result

    def replaceHtml(self, response, data):
        htmlStr = str(etree.tostring(etree.HTML(response)).decode())
        # 替换
        for k, v in data.items():
            str1 = f'<d class="{k}"/>'
            str2 = f'<d class="{k}">{v}</d>'
            htmlStr = re.sub(str1, str2, htmlStr)
        # 提取数据
        # print(htmlStr)
        h = etree.HTML(htmlStr)
        title = h.xpath('//div[@class="col title"]')[0].xpath('string(.)').strip().replace('\t\t\t\t\t', '')
        # 人均
        rjPrice = h.xpath('//span[@class="avgPriceTitle"]')[0].xpath('string(.)')
        # 口味、环境、服务
        kw = h.xpath('//span[@class="comment_score"]/span')[0].xpath('string(.)')
        hj = h.xpath('//span[@class="comment_score"]/span')[1].xpath('string(.)')
        fw = h.xpath('//span[@class="comment_score"]/span')[2].xpath('string(.)')
        address = ''.join([t.xpath('string(.)') for t in h.xpath('//div[@class="col address"]/span')])
        characteristic = h.xpath('//div[@class="col characteristic"]/span')[0].xpath('string(.)')
        more = h.xpath('//div[@class="col more"]')[0].xpath('string(.)')
        print(title, rjPrice, kw, hj, fw, address, characteristic, more)

    def run(self):
        url = 'http://www.porters.vip/confusion/food.html'
        response = self.parse(url)
        svg_url, classXy = self.dispose_css(response)
        fontSize, x, y, yValues = self.dispose_svg(svg_url)
        result = self.core(classXy, fontSize, x, y, yValues)
        self.replaceHtml(response, result)


if __name__ == '__main__':
    cssSvg().run()
