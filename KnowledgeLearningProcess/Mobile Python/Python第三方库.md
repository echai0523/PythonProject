# Pycharm第三方包

## 请求

```python
pip install requests

pip install httpx
import httpx
url = 'http://www.baidu.com/'
# 支持异步 http2.0 
res = httpx.get(url)
# 异步的写法 对于耗时比较多的任务 可以使用异步
httpx.AsyncClient()
```



## 二分查找bisect

https://docs.python.org/zh-cn/3/library/bisect.html

```python
from bisect import bisect

# bisect是python内置模块，用于有序序列的插入和查找。
# 查找array中array[i]<=item或item<=array[i-1]的位置，返回索引值
bisect(array, item)  # 分左右查找
# item插入到array[i]<=item或item<=array[i-1]的位置
insort(array,item)  
```



## MySQL数据库3306

版本最好使用5.6 5.7 如：5.7.72

```

```

## Redis数据库6309

```
pip install redis
```

## MongoDB数据库27017

```

```



## 线程、线程池

```python
# 线程
from threading import Thread
# 线程池
from concurrent.futures import ThreadPoolExecutor
```

## 进程、进程池

```python
# 进程、进程之间的通信
from multiprocessing import Process, Queue
# 进程池
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor # 推荐使用
# 进程池之间的通信
from multiprocessing import Manager
q = Manager().Queue()
```

## 异步

```python
# 异步
pip install asyncio
# aiohttp 是一个基于 asyncio 的异步 HTTP 网络模块
pip install aiohttp
# aiofiles用于处理asyncio应用程序中的本地磁盘文件,爬虫过程中用它来进行文件的异步操作。
pip install aiofiles
# motor是对pymongo进行封装来实现异步操作mongo的Python第三方库
pip install motor


import aiohttp, aiofiles, asyncio
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient('localhost', 27017)  # 连接本地mongo数据库(ip,端口)
db = client['python']['data']
```

## 协程

```python
pip install gevent -i https://pypi.tuna.tsinghua.edu.cn/simple
    
# 所有的io行为进行打包 > monkey.patch_all()
from gevent import monkey
# 创建协程对象，导入gevent管理的任务 > g = spawn(函数, 参数)
from gevent import spawn
# 等待所有任务执行完毕 > joinall([g1, g2, ···])
from gevent import joinall
```



## 处理表格

```python
# openpyxl, xlwt, pandas, csv
pip install openpyxl

from openpyxl import Workbook
wb = Workbook()
wb.save('xx.xlsx')
```



## 随机生成伪数据

```python
pip install faker

from faker import Faker
f = Faker(locale='zh_CN')   # 为生成数据的文化选项，默认为en_US，
```



## yaml文件

```python
pip install pyyaml==5.4.1

>>yaml
>>PyYAML-5.4.1.dist-info

import yaml
```





## 美化打印

```
from pprint import pprint  
```



## 当前时间

```python
from datetime import datetime
# 例 当前年份
datetime.now().year
```



## 打包exe文件

```
pip install pyinstaller

路径下终端输入命令
pyinstaller -F xxx.py  产生单个的可执行文件
pyinstaller -D xxx.py  产生一个目录（包含多个文件）作为可执行程序
```

## 打包pyc文件

py_compile模块用于从源文件生成字节码文件，以及在将模块源文件作为脚本调用时使用的另一个函数。

虽然并不经常需要，但是在安装用于共享使用的模块时，这个函数非常有用，特别是如果某些用户可能没有权限在包含源代码的目录中编写字节码缓存文件的话。

```
import py_compile

py_compile.compile(file, cfile=None, dfile=None, doraise=False, optimize=-1)
```



## 去重

布隆

```python
# python2
pip install pybloom  
# python3
pip install D:\下载\bitarray-2.3.5-cp38-cp38-win_amd64.whl
pip install pybloom-live  

from pybloom_live import BloomFilter
```

python3安装时，要安装live版本，pybloom版本在python3中不支持。

同时安装[pybloom-live](https://www.lfd.uci.edu/~gohlke/pythonlibs/#bitarray)需要先安装`bitarray-2.3.5-cp38-cp38-win_amd64.whl`

其中 cp38为 python3.8 版本， amd64为操作系统64位。

**requests_cache**

```python
pip install requests_cache

import requests_cache

url = 'http://www.baidu.com/'
# 同级生成一个文件夹
requests_cache.init_backend('demo_cache', backend='filesystem')
# 数据存在系统缓存中
# requests_cache.init_backend('demo_cache', backend='filesystem', use_cache_dir=True)
session = requests.session()
for i in range(1,100):
    session.get(url)
```



## 加密库

```python
pip install pycryptodome

>Crypto # 不可用
>pycryptodome-3.11.0.dist-info
from Crypto.Cipher import DES
```



## python运行js文件

```js
npm install crypto-js    # 需要安装node.js

CryptoJS = require("D:\\nodejs\\node_global\\node_modules\\crypto-js");
```



## python调用js文件

```python
pip install PyExecJS  # 需要注意， 包的名称：PyExecJS  

import execjs
print(execjs.get())  # ExternalRuntime(Node.js (V8))
print(execjs.get().name)  # Node.js (V8)
# eval()
print(execjs.get().eval('1+2'))  # 3
print(execjs.eval('1+3'))  # 4

# compile()
num = execjs.compile(
    """
    function add(x, y){
        return x + y
    }
    """
).call('add', 1, 4)
print(num)
# 打开js文件 并 读取内容
with open('test.js') as f:
    js_data = f.read()
    print(js_data)
# compile执行(读取的js文件或"""js文本"""),call(调用函数,传递参数)
ctx = execjs.compile(js_data).call('add', 1, 5)

# 获取毫秒 (13位)  时间戳
print(execjs.eval('Date.now()'))  # 1644297310500
```

`text.js`

```js
function add(x,y){
    return x+y;
};
```

## 使用execjs报错问题

报错内容：

```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xaf in position 36: illegal multibyte sequence
```

具体：

```
Exception in thread Thread-1:
Traceback (most recent call last):
  File "D:\tools\Python3.6\lib\threading.py", line 916, in _bootstrap_inner
    self.run()
  File "D:\tools\Python3.6\lib\threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "D:\tools\Python3.6\lib\subprocess.py", line 1083, in _readerthread
    buffer.append(fh.read())
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa1 in position 26: illegal multibyte sequence

Traceback (most recent call last):
  File "D:/zjf_workspace/003、自己测试用的/002加密和验证码破解/02-js加密破解/022、梦幻西游藏宝阁/执行.py", line 11, in <module>
    result = ct.call('decode_desc', _0x1c0cdf)
  File "D:\tools\Python3.6\lib\site-packages\execjs\_abstract_runtime_context.py", line 37, in call
    return self._call(name, *args)
  File "D:\tools\Python3.6\lib\site-packages\execjs\_external_runtime.py", line 92, in _call
    return self._eval("{identifier}.apply(this, {args})".format(identifier=identifier, args=args))
  File "D:\tools\Python3.6\lib\site-packages\execjs\_external_runtime.py", line 78, in _eval
    return self.exec_(code)
  File "D:\tools\Python3.6\lib\site-packages\execjs\_abstract_runtime_context.py", line 18, in exec_
    return self._exec_(source)
  File "D:\tools\Python3.6\lib\site-packages\execjs\_external_runtime.py", line 87, in _exec_
    output = self._exec_with_pipe(source)
  File "D:\tools\Python3.6\lib\site-packages\execjs\_external_runtime.py", line 103, in _exec_with_pipe
    stdoutdata, stderrdata = p.communicate(input=input)
  File "D:\tools\Python3.6\lib\subprocess.py", line 863, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
  File "D:\tools\Python3.6\lib\subprocess.py", line 1133, in _communicate
    stdout = stdout[0]
IndexError: list index out of range
```

**解决方法1：**

问题起源，代码放在浏览器中直接执行代码和nodejs中执行也是可以的，就是python的execjs不能执行。

将js的fromCharCode**用python chr函数处理报错地方**。

**解决方法2：**

**修改编码文件的默认编码格式为utf-8,默认window下是gbk。**

解决步骤：

**注：建议备份一行，修改的是模块的源码，万一弄错了好改回来。敲代码最忌不懂，乱改还不保留，这样很招人烦的，尤其团队合作时。**

1、进去错误这个D:\tools\Python3.6\lib\subprocess.py文件

![](https://img-blog.csdnimg.cn/20190822162618700.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjA4MTM4OQ==,size_16,color_FFFFFF,t_70)

2、搜索：`encoding=` ，修改编码格式为utf-8

![](https://img-blog.csdnimg.cn/20190822163012262.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjA4MTM4OQ==,size_16,color_FFFFFF,t_70)



## 字体处理

```
pip install fontTools

from fontTools.ttLib import TTFont
```



## 图像处理

```
pip install pillow==8.1.2

# 处理图形模块
from PIL import Image
```

## 生成验证码

```
pip install captcha

from captcha.image import ImageCaptcha
```



## OCR识别

```python
# pytesseract
pip install pytesseract

import pytesseract
# 配置
# 1、环境变量：Administrator用户变量 > 新建 > {变量名:TESSDATA_PREFIX, 变量值: tessdata路径D:\Tesseract-OCR\tessdata}
# 2、修改文件：pytesseract.py > 搜索'cmd' 修改 tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'



# ddddocr
pip install ddddocr=1.4.0

ocr = ddddocr.DdddOcr()
```

## 滑块验证码

```python
# cv2模块
pip install opencv-python

import cv2
```



## Scrapy框架

```
pip install scrapy
```



## Scrapy发送邮件

```
pip install yagmail
```



## Feapder框架

```
pip install feapder==1.6.7
```



## 图片生成二维码

```
from MyQR import myqr
```





## 生成个性名片

```
from segno import helpers
```



## 人工智能-抠图

```
pip install removebg
```

## 

## 游戏开发-做小游戏

```
pip install pygame
```



## 
