

## 一、正则

开源测试工具 http://tool.oschina.net/regex/

官网：https://docs.python.org/zh-cn/3/library/re.html



![1](/imgs/正则样式.png)



| .    | 匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用象 '[.\n]' 的模式。 |
| ---- | ------------------------------------------------------------ |
| \d   | 匹配一个数字字符。等价于 [0-9]。                             |
| \D   | 匹配一个非数字字符。等价于` [^0-9]`。                        |
| \s   | 匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。 |
| \S   | 匹配任何非空白字符。等价于 `[^ \f\n\r\t\v]`。                |
| \w   | 匹配包括下划线的任何单词字符。等价于[A-Za-z0-9_]。           |
| \W   | 匹配任何非单词字符。等价于` [^A-Za-z0-9_]`。                 |

![1](/imgs/正则模式.png)

### 1.match

+ match 方法会尝试从字符串的起始位置匹配正则表达式，如果匹配，就返回匹配成功的结果；如果不匹配，就返回 None

```
re.match(pattern, string, flags=0)
```

参数说明：

|  参数   |                             描述                             |
| :-----: | :----------------------------------------------------------: |
| pattern |                  这是正则表达式来进行匹配。                  |
| string  |      这是字符串，这将被搜索匹配的模式，在字符串的开头。      |
|  flags  | 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。 |

匹配成功re.match方法返回一个匹配的对象，否则返回None。

我们可以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式。

| 匹配对象的方法 | 描述                                                 |
| -------------- | ---------------------------------------------------- |
| group(num=0)   | 此方法返回整个匹配（或指定分组num）,带参必须有()才行 |
| groups()       | 此方法返回所有元组匹配的子组（空，如果没有）         |




```python
import re
content = 'Hello 123 456 welcome to tuling'
print(len(content))   # 31
result = re.match('^Hello\s\d\d\d\s\d{3}\s\w{7}', content)
print(result)   # <re.Match object; span=(0, 21), match='Hello 123 456 welcome'>
print(result.group())   # Hello 123 456 welcome
print(result.start())   # 0
print(result.span())    # (0, 21)
result = re.match('^Hello(\s\d\d\d\s\d{3}\s\w{7})', content)
print(result.group(1))
```

- group() 返回被 正则 匹配的字符串，带参数必须要有元组()

- start() 返回匹配开始的位置

- span() 返回一个元组包含匹配 (开始,结束) 的位置



##### 1、匹配数字

```python
import re

content = 'Hello 123456 welcome to tuling'
result = re.match('^Hello\s(\d+)\swelcome', content)
print(result)  # <re.Match object; span=(0, 20), match='Hello 123456 welcome'>
print(result.group(1))  # 123456
print(result.span())  # (0, 20)
```



##### 2、通用匹配

```python
import re

content = 'Hello 123 456 welcome to tuling'
# 匹配所有数据
result = re.match('^Hello.*ng$', content)
print(result)   # <re.Match object; span=(0, 31), match='Hello 123 456 welcome to tuling'>
print(result.group())  # Hello 123 456 welcome to tuling
# print(result.group(1))   # 报错 IndexError: no such group 必须有元组()
# 匹配某某开始到某某结束
result = re.match('^Hello(.*)ng$', content)
print(result)   #  <re.Match object; span=(0, 31), match='Hello 123 456 welcome to tuling'>
print(result.group())  # Hello 123 456 welcome to tuling
print(result.group(1))   # ' 123 456 welcome to tuli'
```

##### 3、匹配中文

```python
import re
# 匹配中文 [\u4e00-\u9fa5]
s = '大家晚上好asdasdsad'
aa = re.findall('[\u4e00-\u9fa5]+', s)
bb = re.match('[\u4e00-\u9fa5]+', s).group()
print(aa)  # ['大家晚上好']
print(bb)  # 大家晚上好
```

##### 4、匹配单个字符

在上一小节中，了解到通过re模块能够完成使用正则表达式来匹配字符串

本小节，将要讲解正则表达式的单字符匹配

| 字符 | 功能                             |
| :--: | :------------------------------- |
|  .   | 匹配任意1个字符（除了\n）        |
| [ ]  | 匹配[ ]中列举的字符              |
|  \d  | 匹配数字，即0-9                  |
|  \D  | 匹配非数字，即不是数字           |
|  \s  | 匹配空白，即 空格，tab键         |
|  \S  | 匹配非空白                       |
|  \w  | 匹配单词字符，即a-z、A-Z、0-9、_ |
|  \W  | 匹配非单词字符                   |

##### 5、匹配多个字符

匹配多个字符的相关格式

| 字符  | 功能                                                |
| :---: | :-------------------------------------------------- |
|   *   | 匹配前一个字符出现0次或者无限次，即可有可无         |
|   +   | 匹配前一个字符出现1次或者无限次，即至少有1次        |
|   ?   | 匹配前一个字符出现1次或者0次，即要么有1次，要么没有 |
|  {m}  | 匹配前一个字符出现m次                               |
| {m,n} | 匹配前一个字符出现从m到n次                          |

##### 6、匹配开头结尾

| 字符 | 功能           |
| :--: | :------------- |
|  ^   | 匹配字符串开头 |
|  $   | 匹配字符串结尾 |

##### 7、匹配分组

|     字符     | 功能                             |
| :----------: | :------------------------------- |
|      \|      | 匹配左右任意一个表达式           |
|     (ab)     | 将括号中字符作为一个分组         |
|    `\num`    | 引用分组num匹配到的字符串        |
| `(?P<name>)` | 分组起别名                       |
|  (?P=name)   | 引用别名为name分组匹配到的字符串 |

##### 9、贪婪和非贪婪

+ python默认贪婪模式
+ 在"*","?","+","{m,n}"后面加上？，使贪婪变成非贪婪

```python
import re

content = 'http://feier.com/yyds'
result1 = re.match('http.*?com/(.*?)', content)
result2 = re.match('http.*?com/(.*)', content)
print('result1', result1.group()) # result1 http://feier.com/
print('result2', result2.group()) # result2 http://feier.com/yyds
```

##### 5、修饰符

| 修饰符 |                             功能                             |
| :----: | :----------------------------------------------------------: |
|  re.I  |                     使匹配对大小写不敏感                     |
|  re.L  |               做本地化识别（locale-aware）匹配               |
|  re.M  |                    多行匹配，影响 ^ 和 $                     |
|  re.S  |               使 . 匹配包括换行在内的所有字符                |
|  re.U  |   根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.    |
|  re.X  | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。 |

```python
import re
# 这个修饰符的作用是匹配包括换行符在内的所有字符。
content = '''Hello 1234567 World_This
is a Regex Demo
'''
result = re.match('^He.*?(\d+).*?Demo$', content)
print(result.group())  # 存在换行，报错AttributeError: 'NoneType' object has no attribute 'group'
result = re.match('^He.*?(\d+).*?Demo$', content,re.S)
print(result.group())
# 结果：
# Hello 1234567 World_This
# is a Regex Demo
```



### 2、search

匹配时会扫描整个字符串，然后返回第一个成功匹配的结果,如果搜索完了还没有找到，就返回 None。

 案例文本

```html
html = '''<div id="songs-list">
<h2 class="title">经典老歌</h2>
<p class="introduction">
经典老歌列表
</p>
<ul id="list" class="list-group">
<li data-view="2">一路上有你</li>
<li data-view="7">
<a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
</li>
<li data-view="4" class="active">
<a href="/3.mp3" singer="齐秦">往事随风</a>
</li>
<li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
<li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
<li data-view="5">
<a href="/6.mp3" singer="邓丽君">但愿人长久</a>
</li>
</ul>
</div>'''
```



**1、提取符合规则的**

```python
res = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S) 
if res:  
    print(res.group(1), res.group(2))
```



练习：提取字符串里面的数字

```text
str1 = 'asdbsd12312312eqw'
```

答案

```python
re.search('bsd(\d+)eq', str1).group(1)
```



**2、匹配所有**

```python
results = re.findall('<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>', html, re.S)
print(results)  
print(type(results))  
for result in results:  
    print(result)  
    print(result[0], result[1], result[2])
```



### 3、compile

**compile 函数用于编译正则表达式，生成一个 Pattern 对象**，它的一般使用形式如下：

```python
re.compile(pattern[, flag])
```

语法结构

```python
import re

content = 'Hello 123 456 welcome to tuling'
regex = re.compile('\w*o\w*')
x = regex.findall(content)
print(x)
```

### 4、sub

通过re.sub()**替换**函数可以匹配任意字符，并将其替换

```
re.sub(r"匹配字符", '替换', 字符串)
re.sub('[ \n]', '', res) # 去掉空格和换行
```

### 5、split

 根据匹配进行**切割字符串**，并返回一个**列表**

- `|`：或

```python
ss = "info:xiaoZhang 33 shandong"
ret = re.split(r':', ss)   # # 匹配以':'进行切割
print(ret)  # ['info', 'xiaoZhang 33 shandong']
ret = re.split(r":| ", ss)  # 匹配以':'或' '进行切割
print(ret)  # ['info', 'xiaoZhang', '33', 'shandong']
```

### 6、findall

re.findall()如果可以匹配返回的是一个**列表**

```python
content = '八神是我的好朋友，他的手机电话是18381665314， 他的QQ是1911966573， 他女朋友的电话是18381665315, QQ:1911966574 ！'
regex = re.compile(r'\d{11}')
tels = regex.findall(content)
# 结果 # ['18381665314', '18381665315']
```

### 7、finditer

re.finditer()返回的是一个**迭代器**，需要对其进行遍历，才能获取数据。

```python
content = '八神是我的好朋友，他的手机电话是18381665314， 他的QQ是1911966573， 他女朋友的电话是18381665315, QQ:1911966574 ！'
regex = re.compile(r'\d{11}')
tels_obj = regex.finditer(content)
tels_list = []
for tel in tels_obj:
    tels_list.append(tel.group())
print(tels_list)
# 结果 # ['18381665314', '18381665315']
```

### 常见问题

#### 转义问题

```python
# ',' '(' ')' '-' '@'五种特殊符号替换为空格
re = re.sub(r'[,()-@]', ' ', str)  # 错误写法
re = re.sub(r'[,()\-@]', ' ', str) # -表示区间，需要转义'\-'或者写为[,()@-]
```



### 案例

淘宝数据

```python
import urllib.request
headers = {
    'cookie': 'miid=120076508994945398; cna=s5XgGHTA/QACAa8N+wOHxkKB; thw=cn; t=09ef0b533d5f5014504435330c5b23a7; _m_h5_tk=9afb8815f59ecdd6d90f960fa950b608_1632318660385; _m_h5_tk_enc=32d88fe37367c7d8191e0d6ccaa6aeb8; xlly_s=1; _samesite_flag_=true; cookie2=11352226bbcc90e131fb8e2d9a3a78a2; _tb_token_=ed63bd661b9e0; sgcookie=E1002hzxj0%2BkNyK8SW%2BdTaNG6Ou62zkRwlh9oIg6TSxlgEVkBKN0WwQH%2Fw9SRRgzrUuiBsCz5ZwM5v0Z0kwmK1MF3NBMh3Yh3q5FfwrTVvf7M0s%3D; unb=3071675414; uc3=nk2=AQc0Nbnx9S4H8pkl%2BA%3D%3D&vt3=F8dCujdzW2tWEWdg7bI%3D&id2=UNDTw7IM5DYpuA%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; csg=bc1d7fa4; lgc=bcptbtptp%5Cu5F20%5Cu5F20; cancelledSubSites=empty; cookie17=UNDTw7IM5DYpuA%3D%3D; dnk=bcptbtptp%5Cu5F20%5Cu5F20; skt=d666d4e9a1995a28; existShop=MTYzMjMwOTgxNQ%3D%3D; uc4=id4=0%40UgcjZF9065lxnqGgFvjXZ5vSp20%2B&nk4=0%40A6qJ%2FkooLkypmChVx5EvcDW8EO%2BkDz4V; tracknick=bcptbtptp%5Cu5F20%5Cu5F20; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%BC%A043; _nk_=bcptbtptp%5Cu5F20%5Cu5F20; cookie1=BxZoM4%2FT%2BmdjW5MEqR9Mt5craH93rw995UJ3Ud496K4%3D; enc=zdYu03KQWYVyBA9LCueMaJsN0HdEWldS4oFNif9IGQEQaT%2B3o%2Bpb4Mv8qOADxIw325G1hjBZ8c6veP2pQaHigw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=109_1; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie14=Uoe3dYITfaJ8EQ%3D%3D&existShop=false&cookie15=UtASsssmOIJ0bQ%3D%3D&pas=0; JSESSIONID=A10BE1A97F1454FFCFEE08EC1DA77AD4; tfstk=cmMcB3i71jPXWIPoOKwjV8YaxfORZiBa-AkSUvVE8Z3Q65kPiGfPThuHqr0mB11..; l=eBNHRWw4gR5fSGh9BOfwourza77OSIRA_uPzaNbMiOCPOzfp5yfRW6FgCAT9C3GVh6k6R35NsM4TBeYBqS24n5U62j-la_kmn; isg=BNDQjj_8hRiU-VkcaLeqLGneoR4imbTjIXyEsMqhnCv-BXCvcqmEcya33c3l0my7',
    'referer': 'https://s.taobao.com/search?q=%E4%B9%90%E9%AB%98%E6%95%B0%E6%8D%AE&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210922&ie=utf8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
url = 'https://s.taobao.com/search?q=%E7%A7%AF%E6%9C%A8&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&p4ppushleft=2%2C48&s=44'
req = urllib.request.Request(url,headers=headers)
res = urllib.request.urlopen(req)
response = (res.read().decode('utf-8'))
regex = re.compile('<script>\s*g_page_config = (.*?);\s*g_srp_loadCss')
lst_res = regex.findall(response)
print(lst_res)
```



### 练习

提取单前网站所有的图片地址

+ https://pic.netbian.com/4kmeinv/index.html



参考答案

```python
from pyquery import PyQuery as pq
import requests, re
res = requests.get('https://pic.netbian.com/4kmeinv/index.html')
res.encoding = 'gbk'
qq = pq(res.text)
qqq = qq('div.slist')
pattern = '<img[^>]*>'
result1 = re.findall(pattern, str(qqq))
for i in result1:
    print(re.search('src="(.*?)"',i).group(1))
```



## 二、 Pyquery

环境安装

```python
pip install pyquery(或者pyquery==1.4.3)  # 版本：pyquery==1.4.3
```

利用它，我们可以直接解析 DOM 节点的结构，并通过 DOM 节点的一些属性快速进行内容提取。

```html
html = '''
<div id="cont">
    <ul class="slist">
         <li class="item-0">web开发</li>
         <li class="item-1"><a href="link2.html">爬虫开发</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">数据分析</span></a></li>
         <li class="item-1 active"><a href="link4.html">深度学习</a></li>
         <li class="item-0"><a href="link5.html">机器学习</a></li>
     </ul>
 </div>
'''
```



#### 1、实例演示

```python
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('li'))
```



#### 2、解析网页

```python
from pyquery import PyQuery as pq
doc = pq(url='https://www.python.org/')
print(doc('title'))
```



#### 3、css选择器

```python
doc = pq(html)
print(doc('#cont .slist li'))
print(type(doc('#cont .slist li')))

```

#### 4、获取text

遍历这些节点，然后调用 text 方法，就可以获取节点的文本内容，代码示例如下：

```python
for item in doc('#cont .slist li').items():
    print(item.text())
```



#### 5、子节点

```python
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.slist')
print(type(items))
print(items)       # 提取节点所有内容
lis = items.find('li')    # 获取符合条件的li标签
print(type(lis))
print(lis)
```

**5.1 子节点**

```python
lis = items.children()
print(type(lis))
print(lis)
```

#### 6、父节点

```python
co = items.parent()
print(type(co))
print(co)
```

#### 7、兄弟节点

前面我们说明了子节点和父节点的用法，还有一种节点叫作兄弟节点。如果要获取兄弟节点，可以使用 siblings 方法。

```python
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.slist .item-0.active')
# print(li.siblings())
print(li.siblings('.active'))
```



#### 8、 属性获取

```python
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a, type(a))
print(a.attr('href'))
```

+ 遍历提取

  ```python
  doc = pq(html)
  a = doc('a')
  for s in a.items():
      print(s.attr('href'))  # 属性获取
      print(s.text())   #  值获取
  ```



#### 9、节点添加与移除

对节点进行动态修改，比如为某个节点添加一个 class，移除某个节点等，这些操作有时会为提取信息带来极大的便利。

`addClass` 和 `removeClass`：

```python
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.removeClass('active')
print(li)
li.addClass('active')
```



#### 10、伪类选择器

```python
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li:nth-child(2)')    # 第二个节点
li = doc('li:nth-child(2n)')   # 偶数位节点
li = doc('li:last-child')      # 最后一个节点
print(li)
```



## 三、 xpath

- XPath开发工具  [插件下载](https://chrome.zzzmh.cn/index)
  1. 开源的XPath表达式编辑工具:XMLQuire(XML格式文件可用)
  2. chrome插件 XPath Helper
  3. firefox插件 XPath Checker

- XPath语法[XPath语法参考文档](http://www.w3school.com.cn/xpath/index.asp)

  XPath 是一门**在 XML 文档中查找信息的语言**。【只存在于XML】

  **xml类型转换： html.etree.HTML()**

XPath 的选择功能十分强大，它提供了非常简洁明了的路径选择表达式。另外，它还提供了超过 100 个内建函数，用于字符串、数值、时间的匹配以及节点、序列的处理等。几乎所有我们想要定位的节点，都可以用 XPath 来选择。

官网：https://www.w3.org/TR/xpath/。 

**安装：**

```
pip install  lxml
```

**XPath 常用规则**

| 表　达　式 | 描　　述                       |
| ---------- | ------------------------------ |
| nodename   | 选取此节点的所有子节点         |
| /          | 直接，从当前节点选取直接子节点 |
| //         | 简介，从当前节点选取子孙节点   |
| .          | 选取当前节点                   |
| ..         | 选取当前节点的父节点           |
| @          | 选取属性                       |

**XPath 通配符**

| 通配符 | 描述               |
| ------ | ------------------ |
| *      | 匹配任何元素节点。 |
| @*     | 匹配任何属性节点。 |

**谓语条件**

谓语用来查找**某个特定的信息**或者**包含某个指定的值**的节点。所谓"谓语条件"，就是对路径表达式的附加条件。谓语是**被嵌在方括号**中，都写在方括号"[]"中，表示对节点进行进一步的筛选。

| 路径表达式                         | 结果                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。                |
| /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。              |
| /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。            |
| /bookstore/book[position()<3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
| //title[@lang]                     | 选取所有拥有名为 lang 的属性的 title 元素。                  |
| //title[@lang=’eng’]               | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。   |
| //book[price]                      | 选取所有 book 元素，且被选中的book元素必须带有price子元素    |
| /bookstore/book[price>35.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

**选取未知节点**

| 路径表达式   | 结果                              |
| ------------ | --------------------------------- |
| /bookstore/* | 选取 bookstore 元素的所有子元素。 |
| //*          | 选取文档中的所有元素。            |
| //title[@*]  | 选取所有带有属性的 title 元素。   |

**选取若干路径**

通过在路径表达式中使用“|”运算符，您可以选取若干个路径。

| 路径表达式                       | 结果                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| //book/title \| //book/price     | 选取 book 元素的所有 title 和 price 元素。                   |
| //title \| //price               | 选取文档中的所有 title 和 price 元素。                       |
| /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |



#### 1、解析

```python
from lxml import etree

html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))
```



#### 2、节点操作

我们一般会用 // 开头的 XPath 规则来选取所有符合要求的节点。这里以前面的 HTML 文本为例，如果要选取所有节点，可以这样实现：

```python
result = html.xpath('//*')

# 这里使用 * 代表匹配所有节点，也就是整个 HTML 文本中的所有节点都会被获取。可以看到，返回形式是一个列表，每个元素是 Element 类型，其后跟了节点的名称，如 html、body、div、ul、li、a 等，所有节点都包含在列表中了。
```

#### 3、文本

- `text()`：提取文本
- `@href`：提取属性值

- `string(.)`：提取某标签内多条文本。

```html
<div id="test3">
    我左青龙，
    <span id="tiger">
        右白虎，
        <ul>
            上朱雀，
            <li>
                下玄武。
            <a href="link1.html">first item</a>
            </li>
        </ul>
        老牛在当中，
    </span>
    龙头在胸口。
<div>
```



```python
html = etree.HTML(html)
print(html.xpath('//li/a/text()'))  # ['first item']
print(html.xpath('//li/a/@href'))  # ['link1.html']
print(html.xpath('string(.)'))
"""
    我左青龙，
    
        右白虎，
        
            上朱雀，
            
                下玄武。
                first item
            
        
        老牛在当中，
    
    龙头在胸口。


"""
```



#### 4、指定节点获取

- `//li[@id=" "]`
- `//li[@class=" "]`
- `//li[@class=" " and @name=" "]`：多种属性的且的关系

```python
result = html.xpath('//li[@class="item-0"]/a/text()')  
```



#### 5 、节点轴选择

```html
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
```

XPath 提供了很多节点轴选择方法，包括获取子元素、兄弟元素、父元素、祖先元素等，示例如下：

```python
html = etree.HTML(text)
result = html.xpath('//li[1]/ancestor::*')  # 选取当前节点的所有先辈
print(result)
result = html.xpath('//li[1]/attribute::*')   # 选取当前节点的所有属性
print(result)
result = html.xpath('//li[1]/child::a[@href="link1.html"]')  # 选取当前节点的所有子元素
print(result)
result = html.xpath('//li[1]/following::*[2]')    # 选取文档中当前节点的结束标签之后的所有节点
print(result)
result = html.xpath('//li[1]/following-sibling::*')  # 选取当前节点之后的所有同级节点
print(result)

//input[@id='123']/following-sibling::input # 找下一个兄弟节点
//input[@id='123']/preceding-sibling::span  # 上一个兄弟节点
//input[starts-with(@id,'123')]     # 以什么开头
//span[not(contains(text(),'xpath')）]  # 不包含xpath字段的span
```



#### 6、翻页

翻页提取案例

```python
#  最后一个
//span[contains(@class,'s-pagination-strip')]/span[last()]
#  提取下一页     
//span[contains(@class,'s-pagination-strip')]/*[last()]
#  下一页
//span[@class="s-pagination-strip"]/a[text()="下一页"]
```



#### 7、逻辑运算

- `//title/text() | //img/@src`：同时提取两个元素。

- `//li[@class=" " and @name=" "]`：多种属性的且的关系
- `//span[@name='bruce'][text()='bruce1'][1] `
-  `//span[@id='bruce1' or text()='bruce2'] `：多种属性的或的关系



#### 8、模糊条件

- `//li[contains(@class, "item-0")]`：查找class属性**包含**item-0的所有div。
- `//span[not(contains(text(),'xpath')）] ` ：不包含xpath字段的span

- `//li[starts-with(@class, "item-0")]`：第一个class为item-0的div。
- `//li[ends-with(@class, "item-0")]`：最后一个class为item-0的div。



#### 9、索引

```
//div/input[2]
//div[@id='position']/span[3]
//div[@id='position']/span[position()=3]
//div[@id='position']/span[position()>3]
//div[@id='position']/span[position()<3]
//div[@id='position']/span[last()]
//div[@id='position']/span[last()-1]
```



#### 10、substring 截取判断

```
<div data-for="result" id="swfEveryCookieWrap"></div>
//*[substring(@id,4,5)='Every']/@id  截取该属性 定位3,取长度5的字符 
//*[substring(@id,4)='EveryCookieWrap']  截取该属性从定位3 到最后的字符 
//*[substring-before(@id,'C')='swfEvery']/@id   属性 'C'之前的字符匹配
//*[substring-after(@id,'C')='ookieWrap']/@id   属性'C之后的字符匹配
```



## 四、 Beautiful Soup

[Beautiful Soup 4.4.0 文档 — Beautiful Soup 4.2.0 中文 文档](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

[爬虫BS4 使用 ](https://www.jianshu.com/p/845c819a20a3)

**安装**

```python
pip install beautifulsoup4   # bs4
```



**表 4-1　Beautiful Soup 支持的解析器**


| 解析器           | 使用方法                             | 优势                                                        | 劣势                                          |
| ---------------- | ------------------------------------ | ----------------------------------------------------------- | --------------------------------------------- |
| Python 标准库    | BeautifulSoup(markup, "html.parser") | Python 的内置标准库、执行速度适中 、文档容错能力强          | Python 2.7.3 or 3.2.2) 前的版本中文容错能力差 |
| LXML HTML 解析器 | BeautifulSoup(markup, "lxml")        | 速度快、文档容错能力强                                      | 需要安装 C 语言库                             |
| LXML XML 解析器  | BeautifulSoup(markup, "xml")         | 速度快、唯一支持 XML 的解析器                               | 需要安装 C 语言库                             |
| html5lib         | BeautifulSoup(markup, "html5lib")    | 最好的容错性、以浏览器的方式解析文档、生成 HTML5 格式的文档 | 速度慢、不依赖外部扩展                        |

通过以上对比可以看出，lxml 解析器有解析 HTML 和 XML 的功能，而且速度快，容错能力强。



**节点选择器**

直接调用节点的名称就可以选择节点元素，再调用 string 属性就可以得到节点内的文本了，这种选择方式速度非常快。如果单个节点结构层次非常清晰，可以选用这种方式来解析。

下面再用一个例子详细说明选择元素的方法：

```python
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
# soup 对象
print(soup)
# 格式化输出soup 对象
print(soup.prettify())
# 获取文本
print(soup.p.string)
print(soup.title.string)

print(soup.title)
print(type(soup.title))
print(soup.head)
print(soup.p)
```



#### 1、获取属性

每个节点可能有多个属性，比如 id 和 class 等，选择这个节点元素后，可以调用 attrs 获取所有属性：

```python
print(soup.p.attrs)
print(soup.p.attrs['name'])
```



#### 2、嵌套选择

```python
from bs4 import BeautifulSoup

url = http://www.porters.vip/confusion/css/food.css
response = requests.get(url).text
   
soup = BeautifulSoup(response, 'lxml')
print(soup.head.title)  # html的头部标题
print(type(soup.head.title))  # <class 'bs4.element.Tag'>
print(soup.head.title.string) # html的头部标题的文本

# <title>Steamoat 反爬虫练习</title>
# <class 'bs4.element.Tag'>
# Steamoat 反爬虫练习
```



#### 3、关联选择

在做选择的时候，有时候不能做到一步就选到想要的节点元素，需要先选中某一个节点元素，然后以它为基准再选择它的子节点、父节点、兄弟节点等，这里就来介绍如何选择这些节点元素

```python
html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
# 类型列表，该标签下的没有内容，一行为一个元素
print(soup.p.contents)  
```



#### 4、select

用到的**方法是 soup.select()**，**返回类型是 list**。

标签选择器（a），类选择器（.dudu），id选择器（#lala），组合选择器（a, .dudu, #lala, .meme），层级选择器（div.dudu#lala.meme.xixi 表示下面好多级和 div>p>a>.lala 只能是下面一级 ），伪类选择器（不常用），属性选择器 （input[name=‘lala’]）

- `soup.select('title') `：通过标签名查找

- ` soup.select('.sister')`：通过类名查找

- `soup.select('#link1')`：通过 id 名查找

- `soup.select("head > title")`：直接子标签查找

- `soup.select('p #link1')`：组合查找

  组合查找即标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，**属性和标签不属于同一节点 二者需要用空格分开。**

- `soup.select('a[class="sister"]')`：属性查找

  查找时还可以加入属性元素，属性需要用中括号括起来，**注意属性和标签属于同一节点，所以中间不能加空格**，否则会无法匹配到。



##### Tag

Tag 是什么？通俗点讲就是 HTML 中的一个个标签，例如

```
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
```

对于 Tag，它有两个重要的属性，是 name 和 attrs。

- `soup.name`：soup 对象本身比较特殊， name 即 [document]。
- `soup.select('a')[0].name`：内部标签，输出的值便为标签本身的名称a
- `soup.select('a')[0].attrs`：把 soup.select('a')[0] 标签的所有属性输出，得到的类型是一个字典。
- `soup.select('a')[0].attrs['class']`：单独获取某个属性。
- `soup.select('a')[0].get_text()`：获取文本。

**样例**

```html
htmls = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1" title="xl">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""
```

案例一（层级选择器，返回的都是列表）

```python
soup.select('.story > a > span')[0].text
```

案例二（id选择器）

```python
print(soup.select('#link1'))
```

案例三（提取属性）

```python
soup.select('#link1')[0].attrs['href']
```

案例四（提取实际数据）

url地址：https://www.qiushibaike.com/8hr/page/1/

```python
ht = open('s.html',encoding='utf-8').read()
soup1 = BeautifulSoup(ht, 'lxml')
text = soup1.select('.recmd-content')
for i in text:
    print(i.text)
```

