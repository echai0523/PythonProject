### 字体反爬



**什么是字体偏移反爬**

简单而言就是利用css样式将数字进行颠换顺序，进而让爬虫直接获取文本出现错误的结果。



#### 1、解决CSS偏移反爬

对于这种反爬比较理想的就是对css样式进行处理，然后将颠倒或者多余的数字进行回位和覆盖。这里一般需要了解的css样式有display，以及left偏移

- display 可能会设置成none表示直接隐藏

  left偏移，通过宽度以及偏移可以比较每个数字的相对位置



![image-20210806151543724](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210806151543724.png)

上面占位，下面覆盖

根据计算一个位置的距离是16px所以从上图看偏移量分别是-48和-16那么521 的第一个数就是9因为9向左移动了三个字体的位置，而0向左移动了1个位置所以最后结果为920刚好与页面对应



整体效果

```python
# encoding: utf-8
"""
@author: 夏洛
@QQ: 1972386194
@file: xl.py
"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CssOffset:
    def __init__(self):
        """初始化驱动"""
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=option)
        self.url = 'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E4%B8%8A%E6%B5%B7&searchArrivalAirport=%E5%8C%97%E4%BA%AC&searchDepartureTime=2021-08-07&searchArrivalTime=2021-08-11&nextNDays=0&startSearch=true&fromCode=SHA&toCode=BJS&from=qunarindex&lowestPrice=null'
        self.wait = WebDriverWait(self.driver, 10)

    def get_flight_data(self):
        """获取机票数据"""
        script = "Object.defineProperty(navigator, 'webdriver', {get: () => false,});"
        self.driver.get(self.url)
        self.driver.execute_script(script)
        divs = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="m-airfly-lst"]/div')))
        # divs = self.driver.find_elements_by_xpath('//div[@class="m-airfly-lst"]/div')
        return self.parse_line_data(divs)

    def parse_line_data(self, divs):
        """解析每条数据"""
        for div in divs:
            flight_name = div.find_element_by_xpath('.//div[@class="air"]').text   # 机场
            begin_time = div.find_element_by_xpath('.//div[@class="sep-lf"]/h2').text  # 开始时间
            end_time = div.find_element_by_xpath('.//div[@class="sep-rt"]/h2').text   # 结束时间
            prices = div.find_elements_by_xpath('.//div[@class="col-price"]//em[@class="rel"]/b/i')  # 定位占位价格
            price = [price.text for price in prices]
            to_cover_prices = div.find_elements_by_xpath('.//div[@class="col-price"]//em[@class="rel"]/b')  # 定位补坑的
            to_cover_prices_and_styles = [
                (to_cover_price.text, to_cover_price.get_attribute('style')) for to_cover_price in to_cover_prices[1:]
            ]
            true_price = self.replace_price(price, to_cover_prices_and_styles)    # 休整价格
            # print([flight_name, f'{begin_time}-{end_time}', true_price])
            yield [flight_name, f'{begin_time}-{end_time}', true_price]

    @staticmethod
    def replace_price(price, to_cover_prices_and_styles):
        """将价格进行恢复"""
        for to_cover_price, to_cover_style in to_cover_prices_and_styles:
            left = re.search('width: 16px; left: -(\d+)px;', to_cover_style).group(1)  # 提取偏移距离
            price[-int(left) // 16] = to_cover_price
        return ''.join(price)


if __name__ == '__main__':
    css_offset = CssOffset()
    data = [line for line in css_offset.get_flight_data()]
    print(data)
```



#### 2、动态字体反爬虫

在 CSS3 之前，Web 开发者必须使用用户计算机上已有的字体。但是在 CSS3 时代，开发者可以使用@font-face为网页指定字体，对用户计算机字体的依赖。开发者可将心仪的字体文件放在 Web 服务器上，并在 CSS 样式中使用它。用户使用浏览器访问 Web 应用时，对应的字体会被浏览器下载到用户的计算机上。

**注：**

在学习浏览器和页面渲染的相关知识时，我们了解到 CSS 的作用是修饰 HTML ，所以在页面渲染的时候不会改变 HTML 文档内容。由于字体的加载和映射工作是由 CSS 完成的，所以即使我们借助 Splash、Selenium和 Puppeteer 工具也无法获得对应的文字内容。字体反爬虫正是利用了这个特点，将自定义字体应用到网页中重要的数据上，使得爬虫程序无法获得正确的数据。



**采集地址：**https://maoyan.com/films/1218188

分析自定义字体CSS文件



![image-20210806161525545](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210806161525545.png)



一般情况下引用字体@font-face时，会把woff，eot，svg都引用进去，浏览器根据需要下载不同类型的字体

IE--.eot;    其它浏览器--.woff；    手机浏览器一般是--.ttf;

+ truetype:是windows和mac系统最常用的字体格式。

+ eot是嵌入式字体，是微软开发的技术，允许onetype字体用@font-face嵌入到网页。

+ onetype是微软和Adobe共同开发的字体，IE浏览器全部采用这种字体。

+ woff(web开发字体格式)是一种专门为web而设计的字体格式标准，实际上是对truetype/onetype等字体格式的封装，每个字体文件中含有字体以及针对字体

  的元数据（Metadata），字体文件被压缩，以便于网络传输。

+ SVG是由W3C制定的开放标准的图形格式。SVG字体就是使用SVG技术来呈现字体，还有一种gzip压缩格式的SVG字体。



**2.1 字体文件地址**

```python
@font-face{font-family: "mtsi-font";src:url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/9f4f8d1e.eot");src:url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/9f4f8d1e.eot?#iefix") format("embedded-opentype"),url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/9f4f8d1e.woff");} 

```



**2.2 文字对比**

+ 下载字体文件工具

![image-20210806220937664](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210806220937664.png)



查看字体对应关系

![image-20210829154638820](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210829154638820.png)



##### 2.2 案例编写

**2.2.1 首先采集html做分析**

```python
def c_page():
    url = "https://maoyan.com/films/1298542"
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    getFont(r.text)
    with open('indexs.html','wb') as f:
        f.write(r.content)
```



**2.2.2 提取html里面得字体文件做分析**

```python
def getFont(response):
    font_url = 'http:' + re.search(r"url\('(.*\.woff)'\)", response).group(1)
    print('download:\t' + font_url)
    font_file = requests.get(font_url,headers=headers)
    with open('xl.woff', 'wb') as  f:
        f.write(font_file.content)
```



**2.2.3 读取字体文件转xml格式**

+ ```python
   pip install fontTools  # 安装模块
  ```

```python
from fontTools.ttLib import TTFont
xl = TTFont('xl.woff')
# print(xl.getGlyphOrder())  # 读取字体编号  源文件  xml格式得
xl.saveXML('xl.xml') #存储为xml格式文件
```



**2.3.4 手动构造字体文件**

+ 更改字体文件编码和网页格式保持一致，后续做替换使用

```python
# 替换
maoyan_dict = {
        'uniEFE5': '9',
        'uniEAF4': '4',
        'uniE307': '1',
        'uniF8B1': '8',
        'uniF28A': '2',
        'uniF6BA': '3',
        'uniF33F': '0',
        'uniE84E': '7',
        'uniE709': '6',
        'uniF827': '5',
}
uni_base_list = xl.getGlyphOrder()[2:]  # 去除前2位
# 改字体格式
uni = None
font_dict = {}
for gly in uni_base_list:
    m = gly.replace('uni', '&#x').lower() + ';'  # replace字符替换
    font_dict[m] = maoyan_dict[gly]
```



**2.3.5 测试代码**

```python
html = open('ff.html','r',encoding='utf-8').read()
for k in font_dict.keys():
    html = html.replace(k,font_dict[k])
from lxml import etree
body =  etree.HTML(html)
print(body.xpath('//span[@class="index-left info-num "]/span/text()'))
```



**2.3.6 针对每次变化做提取**

可以下载几个字体文件转xml 测试看动态区别：

其实他们的XY坐标差异并不大。

所以我们允许在一定范围内的差异就算一样就好啦。

这样我们就以某字体基准，无论现在实时的字体是哪一个，只要下载下来，再与该字体进行坐标差异对比，相似的就是同一数字。

![image-20210806221819109](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210806221819109.png)

​	

对比2个字体文件观察可以发现同样一个数字得坐标很接近

![image-20210829180450489](C:\Users\Tuling\AppData\Roaming\Typora\typora-user-images\image-20210829180450489.png)





我们下面尝试一下：

1、将新下载的字体文件与base_font对比，找到对应关系

2、前缀替换，并将字体名字和它们所对应的乱码构成一个字典

3、根据字典将加密的数字替换

```python
# encoding: utf-8
"""
@author: 夏洛
@QQ: 1972386194
@file: 猫眼.py
"""
import requests,re
import os
import time
from os import remove
from fontTools.ttLib import TTFont
from lxml import etree
import numpy as np

# 获取字体坐标
def getAxis(font):
    uni_list = font.getGlyphOrder()[2:]
    font_axis = []
    for uni in uni_list:
        axis = []
        for i in font['glyf'][uni].coordinates:
            axis.append(i)
        font_axis.append(axis)
    return font_axis

cur_path = 'fonts'
base_font = TTFont('ff.woff')
base_axis = getAxis(base_font)
base_font.saveXML('base_font.xml')
base_dict = {'uniE02C': '0', 'uniF085': '7', 'uniF5D6': '9', 'uniF46A': '6', 'uniE3B2': '2',
             'uniE189': '1', 'uniF094': '4', 'uniF2AB': '3', 'uniEA44': '8', 'uniF49E': '5'}
base_list = base_font.getGlyphOrder()[2:]

class Maoyan():

    def __init__(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "__mta=108445117.1636534068442.1636549700029.1636550917166.13; uuid_n_v=v1; uuid=E0ABB540420211EC9FBEB19A1A39F786E6FBC7F4F80B48C6BDBD15FCD52B9B63; _csrf=968d276fd2331a017084206e07369db4443d02c22c7b03249b0850afce3e250b; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1636534068; _lxsdk_cuid=17d0908227bc8-05b8e19dbe0e22-b7a1438-1fa400-17d0908227bc8; _lxsdk=E0ABB540420211EC9FBEB19A1A39F786E6FBC7F4F80B48C6BDBD15FCD52B9B63; __mta=108445117.1636534068442.1636549663616.1636549684134.11; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1636550917; _lxsdk_s=17d0a5c1f72-f5c-4d4-e56%7C%7C1",
            "Host": "www.maoyan.com",
            "Pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        self.session =   requests.session()
        self.session.headers = headers

    def get_html(self,url):
        ''' 获取页面数据 '''
        response = self.session.get(url)
        return response

    def get_font(self,url):
        ''' 获取字体数据 '''
        res = requests.get(url)
        return res

    def getFont(self,response):
        '''
        获取最新的字体文件
        :param response:
        :return:
        '''
        # font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', response)[0]
        # font_url = 'http://vfile.meituan.net/colorstone/' + font_file
        font_url = 'http:' + re.search(r"url\('(.*\.woff)'\)", response).group(1)
        new_file = self.get_font(font_url)
        font_file = os.path.join(cur_path, str(time.time()) + '.woff')
        with open(font_file, 'wb') as f:
            f.write(new_file.content)
        return self.parseFont()

    def parseFont(self):
        '''
        获取当前页面动态字体的字典
        :return:
        '''
        print('open:\t' + cur_path)
        file = os.listdir(cur_path)
        curs_font = TTFont(os.path.join(os.getcwd() + '/' + cur_path, file[0]))
        uni_list = curs_font.getGlyphOrder()[2:] # 获取字体映射参数
        cur_axis = getAxis(curs_font)            # 获取当前字体文件坐标
        font_dict = {}
        for i in range(len(uni_list)):
            min_avg, uni = 99999, None
            for j in range(len(base_list)):
                avg = self.compare_axis(cur_axis[i], base_axis[j])
                if avg < min_avg:
                    min_avg = avg
                    uni = base_list[j]
                    # &#xee97  1
                    # print(uni)
            # 把数字替换
            font_dict['&#x' + uni_list[i][3:].lower() + ';'] = base_dict[uni]
        remove(os.path.join(os.getcwd() + '/' + cur_path, file[0]))
        print(font_dict)
        return font_dict

    def compare_axis(self,axis1, axis2):
        '''
        使用欧式距离计算  坐标计算
        距离度量（Distance）用于衡量个体在空间上存在的距离，距离越远说明个体间的差异越大。
        数据分析里面去了   numpy  处理矩阵的
        :param axis1: 新的坐标
        :param axis2: 旧的坐标
        :return:
        '''
        if len(axis1) < len(axis2):
            axis1.extend([0, 0] for _ in range(len(axis2) - len(axis1)))
        elif len(axis2) < len(axis1):
            axis2.extend([0, 0] for _ in range(len(axis1) - len(axis2)))
        axis1 = np.array(axis1)
        axis2 = np.array(axis2)
        return np.sqrt(np.sum(np.square(axis1 - axis2)))

    def parse_info(self,response):
        ''' 解析对应数据 '''
        tree = etree.HTML(response)
        items = []
        for node in tree.xpath('//dd//div[@class="board-item-content"]'):
            item = {}
            item['film_name'] = node.xpath('./div[@class="movie-item-info"]//a/text()')[0]
            item['today_boxoffice'] = node.xpath('.//p[@class="realtime"]/span/span/text()')[0] + node.xpath('.//p[@class="realtime"]//text()[2]')[0].replace('\n', '')
            item['total_boxoffice'] = node.xpath('.//p[@class="total-boxoffice"]/span/span/text()')[0] + node.xpath('.//p[@class="total-boxoffice"]//text()[2]')[0].replace('\n', '')
            from loguru import logger
            logger.info(item)
            items.append(item)
        return items

    def run(self):
        '''
        入口函数
        :return:
        '''
        url = 'https://maoyan.com/board/1'
        response = self.get_html(url).text
        font_dict = self.getFont(response)
        # {'&#xe8d5;': '0', '&#xe6f0;': '2', '&#xe3f1;': '8', '&#xf4d1;': '4', '&#xe189;': '1', '&#xe380;': '7', '&#xf33c;': '9', '&#xe419;': '5', '&#xedff;': '6', '&#xeb1f;': '3'}
        for key in font_dict.keys():
            response = response.replace(key, font_dict[key])
        self.parse_info(response)
        # with open('sss.html', 'w', encoding='utf-8') as f:
        #     f.write(response)
        #     self.parse_info(open('sss.html',encoding='utf-8').read())

if __name__ == '__main__':
    m = Maoyan()
    m.run()
```



