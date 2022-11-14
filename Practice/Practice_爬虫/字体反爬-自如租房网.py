# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 10:06


input:
    - 图片映射字体
output: 
Short Description:
    - 处理流程：
        - 构建脚本框架
        - 分析租房信息生成
            - 页面分析 (../EthanFileData/File img/3ac96999b99f41f7bcd47414c40ac1dd.png)
            - 字体映射图片 (../EthanFileData/File img/69fc41a0b7cab6e4f7be8e4564fa79b8.png)
            - css接口 (../EthanFileData/File img/179746d2214e4900b0d6117e95a38919.png)
            由上图分析得知，下一步需要获取到图片url及px像素值，而通过图片识别的结果及px像素值也无法得出对应的映射字体，还需找到另外一个值background-size: auto 20px。
            分析多家租房价格后，发现图片是同一张。但为了防止后面有差别，将图片url全部提取出来，一对一处理。
            注意：价格固定，但图片和像素值是动态变化的，只要最终计算的结果与房源对应且价格一直，就说明成功了。
            具体步骤：
                - 获取图片url、px像素值、size像素值；
                - 请求获取图片content并进行识别，得到映射字体字符串/列表；
                - 通过px像素值、size像素值之间的计算得出映射字体字符串/列表的索引值。
                注意：px像素值需要转为int做计算，提取的类型str且为浮点型字符串，无法直接str转为int。
                解决方法：使用float()转为浮点型即可。
                通过我的测试得出计算：取整，int(float(px像素值)//int(background-size))。
        - 解决图片映射问题
            - 通过前面分析，需要处理图片映射，大概思路就是将图片中的数字整合成一个字典或字符串，通过像素值进行提取。
        - 数据提取
            - 这里我们需要用到ocr图像识别技术。推荐两种ocr识别库：ddddocr、tesseract。(../PythonLib/ocr库安装_win.md)

Change History:

"""
import requests
from lxml import etree
import re
from ddddocr import DdddOcr
import pytesseract  # 还需要使用Image图片处理
from PIL import Image  # 图片处理


class ziRoom():
    def __init__(self):
        # 匿名函数，对空列表进行取值，防止[0]异常
        self.LamBDa = lambda x: x[0] if x else ''

    def crawl(self, url, flag=True):
        """
        请求接口获取响应
        :param url: 请求接口
        :return: 响应
        """
        headers = {
            'User-Agent': '添加ua'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if flag:
                # 用于提取数据
                return response.text
            else:
                # 用于处理图片
                return response.content

    def selector(self, html, path, flag=True):
        """
        xpath提取数据
        :param html: html元素
        :param path: xpath路径
        :param flag: 标志位，默认解析响应数据
        :return: xpath提取的数据
        """
        if flag:
            node = etree.HTML(html)
            extract = node.xpath(path)
        else:
            extract = html.xpath(path)
        return extract

    def parse(self, response):
        """
        解析页面，处理映射字体
        :param response: 接口响应
        :return:
        """
        # 取出当前页面 所有 客源标签 的 价格标签 --> 每家客源的价格标签
        divs = self.selector(html=response, path='//div[@class="Z_list-box"]/div[@class="item"]')
        # 所有价格加密图片
        for div in divs[:2]:
            # 房源图片
            roomPic = 'https:' + self.LamBDa(self.selector(flag=False, html=div, path='.//img[@class="lazy"]/@src'))
            # 房源名  ['整租·星河城东区2室1厅-西南'] 当前标签下(.//)   # h5标签的class不同,不可添加[@class] 否则丢失数据
            roomName = self.LamBDa(self.selector(flag=False, html=div, path='.//h5/a/text()'))
            # 房源信息  # 97.62㎡ | 16/20层 > 房源距草桥站步行约702米
            desc = self.LamBDa(self.selector(flag=False, html=div, path='.//div[@class="desc"]')).xpath(
                'string(.)').strip().replace('\n', '').replace(' ', '').replace('\t\t\t', ' > ')
            # 房源标签  # 自如客转租 | 离地铁近 | 木棉6.0
            tag = self.LamBDa(self.selector(flag=False, html=div, path='.//div[@class="tag"]')).xpath(
                'string(.)').strip().replace('\n', '').replace(' ', '').replace('\t\t\t\t\t', ' | ')

            # 房源价格
            # ？？？ 那先提取文本 在处理价格
            # 1 提取文本
            priText = self.LamBDa(self.selector(flag=False, html=div, path='.//div[@class="price "]')).xpath(
                'string(.)').strip().replace('\n', '').replace(' ', '').replace('\t\t\t\t', '')
            # 2 处理价格：获取price的style属性
            items = self.selector(flag=False, html=div, path='.//div[@class="price "]//span[@class="num"]/@style')
            priPicUrl = []  # 当前价格字体映射图片
            priPicPx = []  # 对应的像素值
            for item in items:
                # 提取价格字体映射图片，与对应的像素值
                pri = self.LamBDa(re.findall('url\((.*?)\);background-position: -(.*?)px', item))
                pUrl = 'https:' + pri[0]
                pPx = pri[1]
                # 如果存在，说明图片相同，就不存储了
                # if pUrl not in priPicUrl:
                #     priPicUrl.append(pUrl)
                # 防止后面有差别，全部提取出来，一对一处理。
                priPicUrl.append(pUrl)
                priPicPx.append(float(pPx))  # 像素值需要做计算
            # 提取background-size
            sizeHref = self.selector(html=response, path='//head/link[@rel="stylesheet"]/@href')
            sizeCssurl = 'https:' + self.LamBDa([href for href in sizeHref if 'list.css?' in href])
            backgroundSize = int(self.LamBDa(re.findall('background-size:auto (.\d+)px', self.crawl(url=sizeCssurl))))

            """ddddocr使用(简单)"""
            # 创建ocr识别对象，show_ad=False(进入源码你就明白了)
            ocr = DdddOcr(show_ad=False)
            # 识别图片获取映射字体mapChar
            ocrImg = [self.crawl(url=url, flag=False) for url in priPicUrl]
            # 直接读取字节
            mapChar = [ocr.classification(o) for o in ocrImg]

            """tesseract使用(繁琐)
            mapChar = []  # 用于存放识别的字符串
            ocrImg = [self.crawl(url=url, flag=False) for url in priPicUrl]
            for o in ocrImg:
                # 需要将字节保存为图片，使用Image模块读取，最终识别也会出现空格换行等符号
                with open('o.png', 'wb') as f:
                    f.write(o)
                mapChar.append(pytesseract.image_to_string(Image.open('o.png')).replace(' ', '').replace('\n', ''))
            """

            # 计算：int(float(px像素值)//int(background-size))  取整
            price = priText.replace('￥',
                                    '￥' + ''.join([mapChar[i][int(priPicPx[i] // 20)] for i in range(len(mapChar))]))

            # 结果
            print('-' * (len(roomPic) * 3 // 2) + '\n', '\t' + roomPic + '\n', '\t' + roomName,
                  ' ' * len(roomName), price + '\n', '\t' + desc + '\n', '\t' + tag + '\n',
                  '-' * (len(roomPic) * 3 // 2))

    def run(self):
        for p in range(1, 11):
            url = 'https://www.租房网.com/z/p(p)/'
            response = self.crawl(url)
            self.parse(response)


if __name__ == '__main__':
    ziRoom().run()
