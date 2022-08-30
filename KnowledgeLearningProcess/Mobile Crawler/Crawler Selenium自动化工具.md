

# Selenium 的使用

[Python Selenium库的使用](https://blog.csdn.net/weixin_36279318/article/details/79475388)

[参考官方文档](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains。)

[selenium启动Chrome配置参数问题](https://zhuanlan.zhihu.com/p/60852696)

 Ajax 的分析方法，利用 Ajax 接口我们可以非常方便地完成数据的爬取。只要我们能找到 Ajax 接口的规律，就可以通过某些参数构造出对应的的请求，数据自然就能被轻松爬取到。

但是，在很多情况下，Ajax 请求的接口通常会包含加密的参数，如 token、sign 等，如：https://dynamic2.scrape.cuiqingcai.com/，它的 Ajax 接口是包含一个 token 参数的，如图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200817172536726.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
由于接口的请求加上了 token 参数，如果不深入分析并找到 token 的构造逻辑，我们是难以直接模拟这些 Ajax 请求的。

此时**解决方法**通常有两种，一种是**深挖其中的逻辑**，把其中 token 的构造逻辑完全找出来，再用 Python 复现，构造 Ajax 请求；另外一种方法就是直接**通过模拟浏览器的方式，绕过这个过程**。因为在浏览器里面我们是可以看到这个数据的，如果能直接把看到的数据爬取下来，当然也就能获取对应的信息了。

由于第 1 种方法难度较高，在这里我们就先介绍第 2 种方法，模拟浏览器爬取。

这里使用的工具为 Selenium，我们先来了解一下 Selenium 的基本使用方法吧。

Selenium 是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，如点击、下拉等操作，同时还可以获取浏览器当前呈现的页面的源代码，做到可见即可爬。对于一些 JavaScript 动态渲染的页面来说，此种抓取方式非常有效。本节中，就让我们来感受一下它的强大之处吧。



**Selenium库下webdriver模块常用方法的使用**

## 操作浏览器的方法

|                 方法                 |                        说明                        |
| :----------------------------------: | :------------------------------------------------: |
|          set_window_size()           |                  设置浏览器的大小                  |
|          maximize_window()           |                  浏览器最大化显示                  |
|                back()                |                   控制浏览器后退                   |
|              forward()               |                   控制浏览器前进                   |
|              refresh()               |                    刷新当前页面                    |
|               clear()                |                      清除文本                      |
|          send_keys (value)           |                    模拟按键输入                    |
|               click()                |                      单击元素                      |
|               submit()               |                    用于提交表单                    |
|         get_attribute(name)          |                   获取元素属性值                   |
|            is_displayed()            |               设置该元素是否用户可见               |
|                 size                 |                   返回元素的尺寸                   |
|                 text                 |                   获取元素的文本                   |
|             page_source              |                   获取页面源代码                   |
|             current_url              |               用户获得当前页面的URL                |
| find_element().send_keys('文件路径') |                      上传文件                      |
|      save_screenshot(filename)       | 窗口截图保存，filename设置路径，必须保存为png格式  |
|   get_screenshot_as_file(filename)   | 窗口截图保存，filename设置路径，必须保存为png格式  |
|       get_screenshot_as_png()        | 截取当前整个窗口并把图片保存到本地，不可以设置路径 |



## 鼠标事件

鼠标操作的方法封装在 ActionChains 类

https://blog.csdn.net/jamieblue1/article/details/89856576

|                           方法                            |                     说明                      |
| :-------------------------------------------------------: | :-------------------------------------------: |
|                   ActionChains(driver)                    |             构造ActionChains对象              |
|                  click(on_element=None)                   |                 点击鼠标左键                  |
|              click_and_hold(on_element=None)              |              点击鼠标左键不松开               |
|            **context_click**(on_element=None)             |                 点击鼠标右键                  |
|               double_click(on_element=None)               |                 双击鼠标左键                  |
|             **drag_and_drop**(source, target)             |   拖拽指定元素source，到指定target，并松开    |
|     drag_and_drop_by_offset(source, xoffset, yoffset)     |   拖拽指定元素source到指定的x,y坐标，并松开   |
|               key_down(value, element=None)               |              按下某个键盘上的键               |
|                key_up(value, element=None)                |                  松开某个键                   |
|             move_by_offset(xoffset, yoffset)              |         鼠标从当前位置移动到某个坐标          |
|              **move_to_elemen**t(to_element)              |           鼠标移动到指定元素的中间            |
| move_to_element_with_offset(to_element, xoffset, yoffset) |      鼠标移动到距离指定元素x,y坐标的位置      |
|                      pause(seconds)                       |          在指定时间内暂停所有的输入           |
|                       **perform**()                       |              执行链中的所有动作               |
|                 release(on_element=None)                  |          在某个元素位置松开鼠标左键           |
|                      reset_actions()                      |   清空ActionChains对象中原存储的所有动作。    |
|               **send_keys**(*keys_to_send)                |          发送某些键到当前焦点的元素           |
|                   send_keys_to_element                    | (element, *keys_to_send) 发送某些键到指定元素 |
|                                                           |                                               |

## 键盘事件

Selenium中的Key模块提供了模拟键盘按键的方法send_keys()方法。可以模拟键盘输入，也可模拟键盘的操作。

|        模拟键盘按键         |        说明         |
| :-------------------------: | :-----------------: |
| send_keys(Keys.BACK_SPACE)  | 删除键（BackSpace） |
|    send_keys(Keys.SPACE)    |   空格键（Space）   |
|     send_keys(Keys.TAB)     |    制表键（Tab）    |
|   send_keys(Keys.ESCAPE)    |    回退键（Esc）    |
|    send_keys(Keys.ENTER)    |   回车键（Enter）   |
| send_keys(Keys.CONTROL,‘a’) |   全选（Ctrl+A）    |
| send_keys(Keys.CONTROL,‘c’) |   复制（Ctrl+C）    |
| send_keys(Keys.CONTROL,‘x’) |   剪切（Ctrl+X）    |
| send_keys(Keys.CONTROL,‘v’) |   粘贴（Ctrl+V）    |
|    send_keys(Keys.F1…Fn)    |     键盘 F1…Fn      |



### 1. 准备工作

本节以 Chrome 为例来讲解 Selenium 的用法。在开始之前，请确保已经正确安装好了 Chrome 浏览器并配置好了 ChromeDriver。另外，还需要正确安装好 Python 的 Selenium 库。

安装过程可以参考：https://cuiqingcai.com/5135.html 和 https://cuiqingcai.com/5141.html。

1.1 安装

```python
pip install selenium
```

1.2  安装驱动

驱动文件(webdriver)：selenium调用浏览器必须有一个webdriver驱动文件。

官网：http://chromedriver.storage.googleapis.com/index.html

获得驱动压缩包，放置[python解释器的目录](D:\software\Python3.8.8)下解压得到[驱动文件](chromedriver.exe)并删除压缩包。

注意：

+ 驱动要对应[浏览器版本](浏览器设置>>关于Chrome)，否则会无法启动
+ 禁止浏览器自动更新： 在[服务](services.msc)中找到[浏览器更新服务](Google 更新服务(gupdate)、Google 更新服务(gupdatem))设置启动类型为禁止 



### 2. 基本使用

准备工作做好之后，首先来大体看一下 Selenium 有一些怎样的功能。示例如下：

准备工作做好之后，首先来大体看一下 Selenium 有一些怎样的功能。示例如下：

```python
from selenium import webdriver 
from selenium.webdriver.common.by import By  # 定位.定位方式
from selenium.webdriver.common.keys import Keys   # 键盘事件
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标动作链
from selenium.webdriver.support import expected_conditions as EC  # 定位器
from selenium.webdriver.support.wait import WebDriverWait  # 等待  # 等待js渲染的数据出现

# 创建自动化实例对象，以谷歌浏览器启动自动化程序
browser = webdriver.Chrome()
# 跳转
browser.get('https://www.baidu.com')
# 定位输入框
# input_box = browser.find_element_by_id("kw")  # 现版本已弃用，但不影响使用
input_box = browser.find_element(By.ID, 'kw')   # 新定位方式 # 需要导入'定位By'包
# 输入内容
input_box.send_keys('python')
# 模拟点击'百度一下'或者模拟'回车'
# browser.find_element_by_id('su').click()  # 模拟点击'百度一下'
input_box.send_keys(Keys.ENTER)  # 模拟'回车'  # 需要导入'键盘事件Keys'包

# 若遇到需要输入验证码等其他情况，需要添加延迟等待，进行手动操作
# 简单方法: sleep等待延迟   time.sleep(3)  ——> 手动操作   # 不推荐使用
# 设置等待wait：等待js渲染的数据出现，若在等待时长内出现数据则会结束等待
wait = WebDriverWait(browser, 10)   # 设置等待WebDriverWait(浏览器对象, 等待时长)
# 等待.直到(定位器.定位器方法(定位.定位方式()))
    # presence_of_element_located: 等待定位器定位的元素出现内容
    # presence_of_all_elements_located: 等待定位器定位的元素全部出现
# 定位器定位 # dri = wait.until(EC.presence_of_element_located((By.定位方式, '')))
# 定位器是一个元组(By.选择器样式, 选择器样式路径)
wait.until(EC.presence_of_element_located((By.ID, 'content_left'))) 

# 提取页面源代码html
print(browser.page_source)
# 提取cookie
print(browser.get_cookie('PSTM')) # 提取cookies中的'某键'的'值'
print(browser.get_cookies())  # 提取完整cookies  # 列表键值对形式[{" ":" "},{},{}···]
# 提取当前url
print(browser.current_url)
# 截图
browser.save_screenshot('baidu.png')

# close()关闭 quit()退出
browser.close()
```

运行代码后会自动弹出一个 Chrome 浏览器，浏览器会跳转到百度，然后在搜索框中输入 Python，接着跳转到搜索结果页，如图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200817173116910.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)

源代码过长，在此省略。可以看到，当前我们得到的 URL、Cookies 和源代码都是浏览器中的真实内容。

所以说，**用 Selenium 来驱动浏览器加载网页，可以直接拿到 JavaScript 渲染的结果，不用担心使用的是什么加密系统。**

下面来详细了解一下 Selenium 的用法。

### 3. 声明浏览器对象

Selenium 支持非常多的浏览器，如 Chrome、Firefox、Edge 等，还有 Android、BlackBerry 等手机端的浏览器。另外，也支持无界面浏览器 PhantomJS。

```python
webdriver.***()
```

此外，我们可以用如下方式初始化：

```python
from selenium import webdriver
# 驱动文件放在python目录下，初始化时不需要写入路径参数
browser = webdriver.Chrome() 
browser = webdriver.Firefox()
browser = webdriver.Edge() 
browser = webdriver.PhantomJS()
browser = webdriver.Safari()
```

这样就完成了浏览器对象的初始化并将其赋值为 browser 对象。接下来，我们要做的就是调用 browser 对象，让其执行各个动作以模拟浏览器操作。

### 4. 获取页面

我们可以用 get 方法来请求网页，只需要把参数传入链接 URL 即可。比如，这里用 get 方法访问淘宝，然后打印出源代码，代码如下：

```powershell
from selenium import webdriver
browser = webdriver.Chrome() 
browser.get('https://www.taobao.com') # 跳转
print(browser.page_source)   #获取源代码
browser.close()
```

运行后会弹出 Chrome 浏览器并且自动访问淘宝，然后控制台会输出淘宝页面的源代码，随后浏览器关闭。

通过这几行简单的代码，我们就可以驱动浏览器并获取网页源码，非常便捷。

### 5. 查找节点

Selenium 可以驱动浏览器完成各种操作，比如填充表单、模拟点击等。比如，我们想要完成向某个输入框输入文字的操作，首先需要知道这个输入框在哪，而 Selenium 提供了一系列查找节点的方法，我们可以用这些方法来获取想要的节点，以便下一步执行一些动作或者提取信息。

#### 定位元素方式

| id   | class name | name | tag name | link text | partial link text | xpath | css selector |
| ---- | ---------- | ---- | -------- | --------- | ----------------- | ----- | ------------ |

**1、通用方法 find_element()与find_elements()需要传入两个参数：查找方式 By 和 值。**

【该方法需要导'By'包：`from selenium.webdriver.common.by import By  # 定位方式`】

```python
# 例find_element(By.ID, 'kw') 
```

|            定位一个元素             |  定位多个元素(element改为elements)   |         含义          |
| :---------------------------------: | :----------------------------------: | :-------------------: |
|       find_element(By.ID, id)       |       find_elements(By.ID, id)       |    通过元素id定位     |
|     find_element(By.NAME,name)      |     find_elements(By.NAME,name)      |   通过元素name定位    |
|    find_element(By.XPATH,xpath)     |    find_elements(By.XPATH,xpath)     |  通过xpath表达式定位  |
|   find_element(By.LINK_TEXT,text)   |   find_elements(By.LINK_TEXT,text)   |  通过完整超链接定位   |
| find_element(By.PARTIAL_LINK_TEXT,) | find_elements(By.PARTIAL_LINK_TEXT,) |   通过部分链接定位    |
|     find_element(By.TAG_NAME,)      |     find_elements(By.TAG_NAME,)      |     通过标签定位      |
|    find_element(By.CLASS_NAME,)     |    find_elements(By.CLASS_NAME,)     |   通过类名进行定位    |
|   find_element(By.CSS_SELECTOR,)    |   find_elements(By.CSS_SELECTOR,)    | 通过css选择器进行定位 |



**2、方法find_element_by_id()与find_elements_by_id()需传入一个参数：值。** 【新版本已弃用但不影响使用。】

```python
# 例：find_element_by_id("kw")
```

|            定位一个元素             |  定位多个元素(element改为elements)   |         含义          |
| :---------------------------------: | :----------------------------------: | :-------------------: |
|        find_element_by_id()         |        find_elements_by_id()         |    通过元素id定位     |
|       find_element_by_name()        |       find_elements_by_name()        |   通过元素name定位    |
|       find_element_by_xpath()       |       find_elements_by_xpath()       |  通过xpath表达式定位  |
|     find_element_by_link_text()     |     find_elements_by_link_text()     |  通过完整超链接定位   |
| find_element_by_partial_link_text() | find_elements_by_partial_link_text() |   通过部分链接定位    |
|     find_element_by_tag_name()      |     find_elements_by_tag_name()      |     通过标签定位      |
|    find_element_by_class_name()     |    find_elements_by_class_name()     |   通过类名进行定位    |
|   find_element_by_css_selector()    |   find_elements_by_css_selector()    | 通过css选择器进行定位 |

**单个节点：**

当我们想要从淘宝页面中提取搜索框这个节点，首先要观察它的源代码，如图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200817173345550.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)

可以发现，它的 id 是 q，name 也是 q，此外还有许多其他属性。此时我们就可以用多种方式获取它了。比如，find_element_by_name 代表根据 name 值获取，find_element_by_id 则是根据 id 获取，另外，还有根据 XPath、CSS 选择器等获取的方式。

我们用代码实现一下：


```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 模拟键盘操作

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')

# s = browser.find_element_by_id('q')
# s.send_keys('衣服')
# s = browser.find_element_by_css_selector('div.search-combobox-input-wrap>input')
# s.send_keys('衣服')
# s = browser.find_elements_by_xpath('//div[@class="search-combobox-input-wrap"]/input')
# s.send_keys('衣服')
s = browser.find_element_by_xpath("//div[@class='search-combobox-input-wrap']/child::input")
s.send_keys('衣服')
s.send_keys(Keys.ENTER)   # 回车 确定的意思
```

这里我们使用 3 种方式获取输入框，分别是根据 id、CSS 选择器和 XPath 获取，它们返回的结果完全一致，这 3 个节点的类型是一致的，都是 WebElement。

另外，Selenium 还提供了**通用方法 find_element()**，它**需要传入两个参数：查找方式 By 和值**。实际上，它就是 find_element_by_id() 这种方法的通用函数版本，比如 **find_element_by_id(id) 就等价于 find_element(By.ID, id)**，二者得到的结果完全一致。我们用代码实现一下：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.ID, 'q')
input_first.send_keys('衣服')
print(input_first)
browser.close()
```

实际上，这种查找方式的功能和上面列举的查找函数完全一致，不过**参数更加灵活**。



**多个节点：**

如果查找的目标在网页中只有一个，那么完全可以用 find_element() 方法。但如果有多个节点，再用 find_element() 方法查找，就只能得到第一个节点了。如果要查找所有满足条件的节点，需要用 find_elements() 这样的方法。**注意，在这个方法的名称中，element 多了一个 s，注意区分**。

举个例子，假如你要查找淘宝左侧导航条的所有条目，就可以这样来实现：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()
```

得到的内容变成了列表类型，列表中的每个节点都是 WebElement 类型。

也就是说，如果**用 find_element() 方法，只能获取匹配的第一个节点**，结果是 WebElement 类型。如果**用 find_elements() 方法，则结果是列表类型**，列表中的每个节点是 WebElement 类型。

当然，也可以直接用 find_elements() 方法来选择，这时可以这样写：
```python
from selenium.webdriver.common.by import By
lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
```

结果是完全一致的。



### 6. 节点交互

Selenium 可以驱动浏览器来执行一些操作，也就是说可以让浏览器模拟执行一些动作。比较常见的用法有：**输入文字时用 send_keys 方法，清空文字时用 clear 方法，点击按钮时用 click 方法**。示例如下：

```python
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')  # 定位到输入框
input.send_keys('iPhone')   # 输入文本'iPhone'
time.sleep(1)
input.clear()   # 清空输入框
input.send_keys('iPad')  # 重新输入文本'ipad'
button = browser.find_element_by_class_name('btn-search')  # 定位到'搜索'
button.click()  # 点击
```

这里首先驱动浏览器打开淘宝，用 find_element_by_id 方法获取输入框，然后用 send_keys 方法输入 iPhone 文字，等待一秒后用 clear 方法清空输入框，接着再次调用 send_keys 方法输入 iPad 文字，之后再用 find_element_by_class_name 方法获取搜索按钮，最后调用 click 方法完成搜索动作。

通过上面的方法，我们就完成了一些**常见节点的动作操作，更多的操作**可以参见官方文档的交互动作介绍
：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement。

### 7. 切换Frame

在Web应用中经常会遇到frame/iframe表单嵌套页面的应用，WebDriver只能在一个页面上对元素识别与定位，对于frame/iframe表单内嵌页面上的元素无法直接定位。这时就需要通过switch_to.frame()方法将当前定位的主体切换为frame/iframe表单的内嵌页面中。

|            方法             |                        说明                        |
| :-------------------------: | :------------------------------------------------: |
|      switch_to.frame()      | 将当前定位的主体切换为frame/iframe表单的内嵌页面中 |
| switch_to.default_content() |                  跳回最外层的页面                  |

我们知道网页中有一种节点叫作 iframe，也就是子 Frame，相当于页面的子页面，它的结构和外部网页的结构完全一致。Selenium 打开页面后，它默认是在父级 Frame 里面操作，而此时如果页面中还有子 Frame，Selenium是不能获取到子 Frame 里面的节点的。这时就需要使用 switch_to.frame() 方法来切换 Frame。

示例一：豆瓣

```python
browser = webdriver.Chrome()
# 跳转豆瓣
browser.get('https://www.douban.com/')
# 先定位到iframe标签在使用Switch_to.frame切换到该标签
login = browser.find_element(By.XPATH, '//div[@class="login"]/iframe')
browser.switch_to.frame(login)
time.sleep(2)
# 切到密码登录
browser.find_element(By.XPATH, '//ul[@class="tab-start"]/li[@class="account-tab-account"]').click()
# browser.find_element_by_class_name('account-tab-account').click()
# 输入账号、密码、点击登录
browser.find_element(By.ID, 'username').send_keys('12345677899')
browser.find_element(By.ID, 'password').send_keys('117899')
browser.find_element(By.CSS_SELECTOR, '.btn.btn-account').click()
```

示例二：乌海市详情页

```python
detail_url = 'http://www.whggzy.com/PurchaseAdvisory/MostImportant/11947573.html'
browser = webdriver.Chrome()
browser.get(detail_url)
# 以id='iframe'定位切换到iframe中
browser.switch_to.frame('iframe')
# 定位iframe下的body标签 获取详情并写入文件保存
detail = browser.find_element(By.XPATH, '//body[@class="view"]')
# detail输出属性类型 detail.text输出文本内容
# print(detail.text)
with open(f'{title}.doc', 'w', encoding='utf-8') as f:
    f.write(detail.text)
```

示例三：菜鸟

```python
import time 
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable' 
browser.get(url) 
browser.switch_to.frame('iframeResult')  # 定位frame的id标签
try:
    logo = browser.find_element_by_class_name('logo') 
except NoSuchElementException:
    print('NO LOGO')  # NO LOGO
browser.switch_to.parent_frame() 
logo = browser.find_element_by_class_name('logo')
print(logo) # <selenium.webdriver.remote.webelement.WebElement(session="4bb8ac03ced4ecbdefef03ffdc0e4ccd",element="0.13792611320464965-2")> 
print(logo.text)  # RUNOOB.COM
```

这里还是以前面演示动作链操作的网页为例，首先通过 switch_to.frame 方法切换到子 Frame 里面，然后尝试获取子 Frame 里的 logo 节点（这是不能找到的），如果找不到的话，就会抛出 NoSuchElementException 异常，异常被捕捉之后，就会输出 NO LOGO。接下来，我们需要重新切换回父级 Frame，然后再次重新获取节点，发现此时可以成功获取了。

所以，当页面中包含子 Frame 时，如果想获取子 Frame 中的节点，需要先调用 switch_to.frame 方法切换到对应的 Frame，然后再进行操作。





### 8. 切换window

**多窗口切换**

在页面操作过程中有时候点击某个链接会弹出新的窗口，这时就需要主机切换到新打开的窗口上进行操作。WebDriver提供了**switch_to.window()方法，可以实现在不同的窗口之间切换。**

|             方法              |                             说明                             |
| :---------------------------: | :----------------------------------------------------------: |
|     current_window_handle     |                       获得当前窗口句柄                       |
|        window_handles         |                 返回所有窗口的句柄到当前会话                 |
|      switch_to.window()       | 用于切换到相应的窗口，与上一节的switch_to.frame()类似，前者用于不同窗口的切换，后者用于不同表单之间的切换。 |
| switch_to.window(handles[-1]) |                     切换到最新打开的窗口                     |
| switch_to.window(handles[-2]) |                  切换到倒数第二个打开的窗口                  |
| switch_to.window(handles[0])  |                    切换到最开始打开的窗口                    |

在访问网页的时候，会开启一个个选项卡。在 Selenium 中，我们也可以对选项卡进行操作。示例如下：

```python
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
# # 打开一个空白的新选项卡
browser.execute_script('window.open()')
# # 打开一个新的窗口跳转'百度'
browser.execute_script('window.open("https://www.baidu.com/")')
# 打开一个空白的新选项卡
browser.execute_script('window.open()')
# 获取打开的多个窗口句柄
handles = browser.window_handles  # 列表
# 切换到最开始打开的窗口
browser.switch_to.window(handles[0])
input_box = browser.find_element(By.ID, 'kw')   # 定位到输入框
input_box.send_keys('美女')  # 输入'美女'
input_box.send_keys(Keys.ENTER)  # 模拟'回车'  搜索'美女'
time.sleep(3)
# 切换到第二个窗口
browser.switch_to.window(handles[1])
browser.get('https://www.taobao.com/')
time.sleep(3)
# 切换到当前最新打开的窗口
browser.switch_to.window(handles[-1])
browser.get('https://pic.netbian.com/')
time.sleep(3)
# 切换到倒数第二个打开的窗口
browser.switch_to.window(handles[-2])
browser.get('https://bz.zzzmh.cn/index#index')
time.sleep(3
```

窗口句柄：

```python
['CDwindow-4f58e3a7-7167-4587-bedf-9cd8c867f435', 'CDwindow-6e05f076-6d77-453a-a36c-32baacc447df']
```

首先访问了百度，然后调用了 execute_script() 方法，这里传入 window.open() 这个 JavaScript 语句新开启一个选项卡。然后切换到该选项卡，调用 window_handles 属性获取当前开启的所有选项卡，后面的参数代表返回选项卡的代号列表。要想切换选项卡，只需要调用 switch_to.window() 方法即可，其中参数是选项卡的代号。这里我们将第2个选项卡代号传入，即跳转到第2个选项卡，接下来在第2个选项卡下打开一个新页面，如果你想要切换回第 2 个选项卡，只需要重新调用 switch_to.window() 方法，再执行其他操作即可。



### 9. 动作链

在上面的实例中，一些交互动作都是针对某个节点执行的。比如，对于输入框，我们就调用它的输入文字和清空文字方法；对于按钮，就调用它的点击方法。其实，还有另外一些操作，它们没有特定的执行对象，比如**鼠标拖曳、键盘按键**等，这些动作用另一种方式来执行，那就是动作链ActionChains。

#### 鼠标拖曳

比如，现在实现一个节点的拖曳操作，将某个节点从一处拖曳到另外一处，可以这样实现：

```python
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'  # 拖曳实例
browser.get(url)
# 切换iframe
browser.switch_to.frame('iframeResult')
# 定位到 [目标, 目标地]
a = browser.find_element(By.ID, 'draggable')  # 可拖曳目标
b = browser.find_element(By.ID, 'droppable')  # 放置目标

# 将对象创建为动作链对象
actions = ActionChains(browser)
# 将[目标, 目标地]形成拖曳  # 可拖曳目标(drag) 拖到 放置目标(drop)
actions.drag_and_drop(a, b)
# 执行动作链对象
actions.perform()
```

首先，打开网页中的一个拖曳实例，然后依次选中要拖曳的节点和拖曳到的目标节点，接着声明 ActionChains 对象并将其赋值为 actions 变量，然后通过调用 actions 变量的 drag_and_drop() 方法，再调用 perform() 方法执行动作，此时就完成了拖曳操作，如图所示：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200817174903639.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
拖拽前页面![在这里插入图片描述](https://img-blog.csdnimg.cn/20200817174919366.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
拖拽后页面
以上两图分别为在拖拽前和拖拽后的结果。



### 10. 执行JavaScript

虽然WebDriver提供了操作浏览器的前进和后退方法，但对于浏览器滚动条并没有提供相应的操作方法。在这种情况下，就可以借助JavaScript来控制浏览器的滚动条。WebDriver提供了execute_script()方法来执行JavaScript代码。

|                             方法                             |                            说明                             |
| :----------------------------------------------------------: | :---------------------------------------------------------: |
|                       execute_script()                       |                    JavaScript控制浏览器                     |
| window.scrollTo(document.body.scrollWidth,document.body.scrollHeight) | 设置浏览器窗口滚动条的水平和垂直位置；body或documentElement |
| document.documentElement.scroll`顶`/`左`=document.documentElement.scroll`高`/`宽` |    设置浏览器窗口滚动条的水平和垂直位置；documentElement    |

#### 打开一个新窗口

```python
# 通过js新打开一个窗口
driver.execute_script('window.open("https://www.baidu.com");')
browser = webdriver.Chrome()
```

#### 滚动条

对于某些操作，Selenium API 并没有提供。比如，下拉进度条，它可以直接模拟运行 JavaScript，此时使用 execute_script() 方法实现滚动滚动条的两种(同理的)方法，代码如下：

```python
from selenium import webdriver
import time, random

browser = webdriver.Chrome()
# 淘宝'包臀裙'
browser.get('https://ai.taobao.com/search/index.htm?spm=a231o.13503973.1998549605.22.10f268edFPHL4D&&pid=mm_49060511_2224600175_111161850090&app_pvid=f7fa533b-1369-4f9b-b344-9ae17f27f5e5&channelId=4&key=%E5%8C%85%E8%87%80%E8%A3%99&unid=&scm=1007.23044.123524.0&engPvid=f7fa533b-1369-4f9b-b344-9ae17f27f5e5&cat=1623/')
# 设置滚动条
# 方法一  或 方法二
browser.close()
```

**方法一：**使用`execute_script('window.scrollTo(水平的左间距,垂直的上边距)')`方法处理。

```python
# """垂直滚动 - 一次性滚动"""
# # 一次性滚动到 底部
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# time.sleep(2)
# # 一次性滚动到 顶部
# browser.execute_script('window.scrollTo(0, 0)')
# time.sleep(2)
# # browser.execute_script('alert("To Bottom")')
# 
# """垂直滚动 - 慢慢滚动"""
# # 慢慢的滚动到 底部
# for i in range(1, 9):
#     time.sleep(random.randint(100, 300) / 1000)  # 设置随机延时
#     browser.execute_script('window.scrollTo(0, {})'.format(i * 700))
# # 慢慢的滚动到 顶部
# for i in range(1, 9):
#     time.sleep(random.randint(100, 300) / 1000)  # 设置随机延时
#     browser.execute_script('window.scrollTo(0, document.body.scrollHeight-{})'.format(i * 700))
# """水平滚动 - 一次性滚动"""
# # 一次性滚动到 右端
# browser.execute_script('window.scrollTo(document.body.scrollWidth, 0)')
# time.sleep(2)
# # 一次性滚动到 左端
# browser.execute_script('window.scrollTo(0, 0)')
# time.sleep(2)
# """水平滚动 - 慢慢滚动"""
# # 慢慢的滚动到 右端
# for i in range(1, 9):
#     time.sleep(random.randint(100, 300) / 1000)  # 设置随机延时
#     browser.execute_script('window.scrollTo({}, 0)'.format(i * 700))
# # 慢慢的滚动到 左端
# for i in range(1, 9):
#     time.sleep(random.randint(100, 300) / 1000)  # 设置随机延时
#     browser.execute_script('window.scrollTo(document.body.scrollHeight-{}, 0)'.format(i * 700))
```

**方法二：**使用`execute_script('document.documentElement.scroll左=document.documentElement.scroll宽')`与`execute_script('document.documentElement.scroll顶=document.documentElement.scroll高')`

```python
"""水平滚动 - 一次性滚动"""
# 滚动左右滚动条---向右滚动最右端
browser.execute_script('document.documentElement.scrollLeft=document.documentElement.scrollWidth')
time.sleep(2)
# 滚动左右滚动条---向左滚动到最左端
browser.execute_script("document.documentElement.scrollLeft=0")
time.sleep(2)

"""水平滚动 - 慢慢滚动"""
# 慢慢的滚动到右端
for i in range(1, 10):
    # 滚动框分10份，一次滚动十分之一
    browser.execute_script(f'document.documentElement.scrollLeft=document.documentElement.scrollWidth * {i/10}')
    time.sleep(random.randint(100, 300)/1000)
# 慢慢的滚动到左端
# 滚动框分10份，一次滚动十分之一
i = 10
while i:
    # 第一次从右端滚动到十分之九，最后滚到左端退出循环
    i -= 1
    browser.execute_script(f'document.documentElement.scrollLeft=document.documentElement.scrollWidth * {i/10}')
    time.sleep(random.randint(100, 300)/1000)

"""垂直滚动 - 一次性滚动"""
# 拖动到滚动条底部---向下滚动到底部
browser.execute_script("document.documentElement.scrollTop=document.documentElement.scrollHeight")
time.sleep(2)
# 拖动到滚动条底部---向上滚动到顶部
browser.execute_script("document.documentElement.scrollTop=0")
time.sleep(2)

"""垂直滚动 - 慢慢滚动"""
# 慢慢的滚动到底部
for i in range(1, 10):
    # 滚动框分10份，一次滚动十分之一
    browser.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight * {i/10}')
    time.sleep(random.randint(100, 300)/1000)
# 慢慢的滚动到顶部
# 滚动框分10份，一次滚动十分之一
i = 10
while i:
    # 第一次从底部滚动到十分之九，最后滚到顶部退出循环
    i -= 1
    browser.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight * {i/10}')
    time.sleep(random.randint(100, 300)/1000)
```

这里就利用 execute_script() 方法将进度条下拉到最底部，然后弹出 alert 提示框。

所以说有了这个方法，基本上 API 没有提供的所有功能都可以用执行 JavaScript 的方式来实现了。



### 11. 获取节点信息

通过 **page_source 属性可以获取网页的源代码**，接着就可以使用解析库（如正则表达式、Beautiful Soup、pyquery 等）来提取信息了。

不过，既然 Selenium 已经提供了选择节点的方法，并且返回的是 WebElement 类型，那么它也有相关的方法和属性来直接提取节点信息，如属性、文本等。这样的话，我们就可以不用通过解析源代码来提取信息了，非常方便。

接下来，我们就来看看可以通过怎样的方式来获取节点信息吧。

|                方法                |      说明      |
| :--------------------------------: | :------------: |
| WebElement.get_attribute('属性名') | 获取节点的属性 |
|          WebElement.text           |    获取文本    |
|           WebElement.id            |     获取id     |
|        WebElement.location         |    获取位置    |
|        WebElement.tag_name         |   获取标签名   |
|          WebElement.size           | 获取大小(宽高) |
|      save_screenshot('命名')       |  当前页面截图  |

#### 获取属性、文本值

我们可以使用 **get_attribute() 方法来获取节点的属性**，但是其前提是先选中这个节点，**通过 get_attribute() 方法，然后传入想要获取的属性名，就可以得到它的值了**。

每个 WebElement 节点都有 text 属性，**直接调用text属性**就可以得到节点内部的文本信息，**相当于 pyquery 的 text 方法**。

```python
import time
from selenium import webdriver   # 驱动
from selenium.webdriver.common.by import By  # 定位

# 创建Edge实例，启动
browser = webdriver.Edge()
# 跳转进入接口
browser.get('https://pic.netbian.com/')
# 定位 全部a标签的WebElement对象
# find_elements定位页面上多个相同的元素坐标。
# find_element定位页面上一个元素坐标。
a_title = browser.find_elements(By.XPATH, "//div[@class='classify clearfix']/a")
# a_title = browser.find_elements(By.CSS_SELECTOR, '.classify.clearfix>a')  # css_selector中.class #id >下一级
# 获取属性
for h in a_title:
    # 一个a标签WebElement对象
    print(h)
    # .get_attribute('属性名')方法获取href属性
    href = h.get_attribute('href')
    # .text方法获取text属性
    txt = h.text
    print(href, txt)


# 2秒等待后退出
time.sleep(2)
browser.quit()
```

#### 获取 ID、位置、标签名、大小

另外，WebElement 节点还有一些其他属性，比如 **id 属性获取节点 id，location 属性获取该节点在页面中的相对位置，tag_name 属性获取标签名称，size 属性获取节点的大小(宽高)**，这些属性有时候还是很有用的。示例如下：

示例一：

```python
import time
from selenium import webdriver   # 驱动
from selenium.webdriver.common.by import By  # 定位

# 创建Edge实例，启动
browser = webdriver.Edge()
# 跳转进入接口
browser.get('https://pic.netbian.com/')
# 定位 全部的img标签WebElement对象
# img_title = browser.find_elements(By.XPATH, "//div[@class='clearfix']/li/a/span/img")
img_title = browser.find_elements(By.CSS_SELECTOR, '.clearfix li a span img')
# 获取属性
for img in img_title:
    # 一个img标签WebElement对象
    print(img)
    # 获取id
    img_id = img.id
    # 获取位置
    img_location = img.location
    # 获取标签名
    img_tag_name = img.tag_name
    # 获取大小(宽高)
    img_size = img.size
    print(img_txt, ':', 'id:', img_id, 'location:', img_location, 'tag_name:', img_tag_name, 'size:', img_size)

# 2秒等待后退出
time.sleep(2)
browser.quit()
```

#### 获取截图

- 截图并保存的两种使用方法：`save_screenshot(filename)`，`get_screenshot_as_file(filename)`

- 截图处理的唯一使用方法：`get_screenshot_as_png()`，截图但不保存，用于处理图片，对截图二次截取

**窗口截图并保存save_screenshot(filename)**

```python
from selenium import webdriver   # 驱动

browser = webdriver.Edge()
browser.maximize_window()  # 窗口最大化 # 通过设置窗口大小改变截图大小
browser.get('https://pic.netbian.com/')
 # 可设置截图保存路径  盘符:/../../..png   # 命名必须为png格式
browser.save_screenshot('窗口截图1.png')   # <class 'bool'>
```

**窗口截图并保存get_screenshot_as_file(filename)**

```python
from selenium import webdriver   # 驱动

browser = webdriver.Edge()
browser.maximize_window()  # 窗口最大化 # 通过设置窗口大小改变截图大小
browser.get('https://pic.netbian.com/')
 # 可设置截图保存路径 盘符:/../../..png  # 命名必须为png格式
browser.get_screenshot_as_file('窗口截图2.png')  #  <class 'bool'>
```

**截图但不保存get_screenshot_as_png()**

```python
from selenium import webdriver   # 驱动

browser = webdriver.Edge()
browser.maximize_window()  # 窗口最大化
browser.get('https://pic.netbian.com/')

browser.get_screenshot_as_png()  # 截图但不保存 <class 'bytes'>
```

**处理截图**

对截取的窗口进行处理，唯一使用方法`get_screenshot_as_png()`的原因：

- 通过`save_screenshot(filename)`，`get_screenshot_as_file(filename)`采取的截图方式会将图片进行保存，类型<class 'bool'>。

- 通过`get_screenshot_as_png()`采取的截图方式不进行保存，类型<class 'bytes'>

```python
# 安装模块
pip install pillow   # 图片处理
```

案例

 ```python
import time
from selenium import webdriver   # 驱动
from selenium.webdriver.common.by import By  # 定位
from io import BytesIO 
from PIL import Image  #图片处理

# 创建Edge实例，启动
browser = webdriver.Edge()
# 最大化窗口
browser.maximize_window()
# 跳转进入接口
browser.get('https://pic.netbian.com/')

# 定位 # 一个img标签WebElement对象
img_title = browser.find_element(By.XPATH, "//ul[@class='clearfix']/li/a/span/img")

# 获取位置
location = img_title.location    # {'x': 74, 'y': 474}
print(location)
# 获取大小(宽高)
size = img_title.size  # {'height': 249, 'width': 390}
print(size)
# 定位img位置 （左，上，右，下）
left, top, right, bottom = location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']
# print(left, top, right, bottom)

# 窗口截图 要求类型为bytes # png截图不保存 类型为bytes  # save_screenshot、file截图保存 类型为bool
screenshot = browser.get_screenshot_as_png()
# # 打开BytesIO截图
screen = Image.open(BytesIO(screenshot))
# # 从截图中按位置截取图片
cap = screen.crop((left, top, right, bottom))
cap.save('1.png')


# 2秒等待后退出
time.sleep(2)
browser.quit()
 ```




### 12. 延时等待

在 Selenium 中，get() 方法会在网页框架加载结束后结束执行，此时如果获取 page_source，可能并不是浏览器完全加载完成的页面，如果某些页面有额外的 Ajax 请求，我们在网页源代码中也不一定能成功获取到。所以，这里**需要延时等待一定时间，确保节点已经加载出来**。

这里等待的方式有两种：一种是**隐式等待(不常用)**，一种是**显式等待(常用)**。

`显示waits`: **明确的行为表现** 在本地的selenium运行(你选择的编程语言) **可以在任何你能想到的条件下工作**返回成功或者超时 **可以定义元素的缺失为条件**可以定制重试间隔，可以忽略某些异常。

`隐式waits`: **不明确的行为表现**，同一个问题依赖于不同的操作系统，不同的浏览器，不同的selenium版本会有各种不同的表现 在远程的selenium上运行(控制浏览器的那部分). **只能在寻找元素的函数上工作**返回找到元素或者（在超时以后）没有找到 **如果检查元素缺失那么总是会等待到超时** 除了时间啥都不能指定。

#### 隐式等待

隐式等待方法：**只规定了一个固定时间**，而页面的加载时间会受到网络条件的影响（效果不好）。

隐式的`waits`会让WebDriver试图定位元素的时候对DOM进行指定次数的轮询。

当使用隐式等待执行测试的时候，如果 Selenium 没有在 DOM 中找到节点，将继续等待，超出设定时间后，则抛出找不到节点的异常。换句话说，当我们要找一个或者一些不能立即可用的元素的时候，隐式`waits`会告诉WebDriver轮询DOM指定的次数，默认设置是0次。一旦设定，WebDriver对象实例的整个生命周期的隐式调用也就设定好了。

- ` implicitly_wait(time_to_wait)`：参数time_to_wait为固定时间。

示例如下：

```python
import time
from selenium import webdriver

browser = webdriver.Chrome() 
s = time.time()
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
try:
    input = browser.find_element_by_class_name('zu-top-add-question')
finally:
    print(time.time() - s)
```



#### 显式等待

显式等待方法：**指定要查找的节点，再指定一个最长等待时间**。如果**在规定时间内加载出来了这个节点，就返回查找的节点**；如果到了规定时间依然没有加载出该节点，则抛出超时异常。

显式的`waits`会让WebDriver在更深一步的执行前等待一个确定的条件触发

- 设置等待：`WebDriverWait(driver, timeout)`，参数driver为浏览器对象，参数timeout为最长等待时间。
- 定位器：`expected_conditions`，可重命名为`EC`方便使用。定位器是一个`元组()`。

示例如下：


```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 等待
# from selenium.webdriver.support.wait import WebDriverWait  # 等待
from selenium.webdriver.support import expected_conditions as EC  # 定位器

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
# 设置等待时长
wait = WebDriverWait(browser, 10)
# 定位器定位 结合等待命令，只要定位到则继续执行，否则等待直到等待时间结束
input = wait.until(EC.presence_of_element_located((By.ID, 'q'))) # 定位器是一个元组()。
# 定位到节点立即点击
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)
```

这里首先引入 WebDriverWait 这个对象，指定最长等待时间，然后调用它的 until() 方法，传入要等待条件 expected_conditions。比如，这里传入了 presence_of_element_located 这个条件，代表节点出现，其参数是节点的定位元组，也就是 ID 为 q 的节点搜索框。

这样做的效果就是，在 10 秒内如果 ID 为 q 的节点（即搜索框）成功加载出来，就返回该节点；如果超过 10 秒还没有加载出来，就抛出异常。

对于按钮，可以更改一下等待条件，比如改为 element_to_be_clickable，也就是可点击，所以查找按钮时查找 CSS 选择器为.btn-search 的按钮，如果 10 秒内它是可点击的，也就是成功加载出来了，就返回这个按钮节点；如果超过 10 秒还不可点击，也就是没有加载出来，就抛出异常。

现在我们运行代码，它在网速较佳的情况下是可以成功加载出来的。

控制台的输出如下：

```powershell
<selenium.webdriver.remote.webelement.WebElement 
(session="07dd2fbc2d5b1ce40e82b9754aba8fa8", 
element="0.5642646294074107-1")>
<selenium.webdriver.remote.webelement.WebElement 
(session="07dd2fbc2d5b1ce40e82b9754aba8fa8", 
element="0.5642646294074107-2")>
```

可以看到，控制台成功输出了两个节点，它们都是 WebElement 类型。

如果网络有问题，10 秒内没有成功加载，那就抛出 TimeoutException 异常，此时控制台的输出如下：

```powershell
TimeoutException Traceback (most recent call last) 
<ipython-input-4-f3d73973b223> in <module>()
      7 browser.get('https://www.taobao.com/')
      8 wait = WebDriverWait(browser, 10) 
----> 9 input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
```

关于等待条件，其实还有很多，比如判断标题内容，判断某个节点内是否出现了某文字等。下表我列出了所有的等待条件。

表　等待条件及其含义


| 等待条件 | 含义 |
| :----: | :--: |
| title_is | 标题是某内容 |
| title_contains | 标题包含某内容 |
| presence_of_element_located | **节点加载出，传入定位元组，如 (By.ID, 'p')** |
| visibility_of_element_located | 节点可见，传入定位元组 |
| visibility_of | 可见，传入节点对象 |
| presence_of_all_elements_located | **所有节点加载出** |
| text_to_be_present_in_element | 某个节点文本包含某文字 |
| text_to_be_present_in_element_value | 某个节点值包含某文字 |
| frame_to_be_available_and_switch_to_it frame | 加载并切换 |
| invisibility_of_element_located | 节点不可见 |
| element_to_be_clickable | **节点可点击** |
| staleness_of | 判断一个节点是否仍在 DOM，可判断页面是否已经刷新 |
| element_to_be_selected | 节点可选择，传节点对象 |
| element_located_to_be_selected | 节点可选择，传入定位元组 |
| element_selection_state_to_be | 传入节点对象以及状态，相等返回 True，否则返回 False |
| element_located_selection_state_to_be | 传入定位元组以及状态，相等返回 True，否则返回 False |
| alert_is_present | 是否出现 Alert |

更多详细的等待条件的参数及用法介绍可以参考官方文档。

### 13. 前进后退

平常使用浏览器时都有前进和后退功能，Selenium 也可以完成这个操作，它使用 back() 方法后退，使用 forward() 方法前进。示例如下：


```python
import time
from selenium import webdriver

browser = webdriver.Chrome()
# 一个标签跳转三个平台
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')  # 当前窗口显示python平台
browser.back()  # 模拟后退  # 跳转taobao平台
time.sleep(1)
browser.forward() # 模拟前进  # 跳转到python平台
browser.close()
```

这里我们连续访问 3 个页面，然后调用 back() 方法回到第二个页面，接下来再调用 forward() 方法又可以前进到第三个页面。

### 14. Cookies

使用 Selenium，还可以方便地对 Cookies 进行操作，例如获取、添加、删除 Cookies 等。

WebDriver操作cookie的方法:

|               方法                |                             说明                             |
| :-------------------------------: | :----------------------------------------------------------: |
|           get_cookies()           |                      获得所有cookie信息                      |
|         get_cookie(name)          |              返回字典的key为“name”的cookie信息               |
|      add_cookie(cookie_dict)      |  添加cookie。“cookie_dict”指字典对象，必须有name 和value 值  |
| delete_cookie(name,optionsString) | 删除cookie信息。“name”是要删除的cookie的名称，“optionsString”是该cookie的选项，目前支持的选项包括“路径”，“域” |
|       delete_all_cookies()        |                      删除所有cookie信息                      |

示例如下：

```python
from selenium import webdriver

browser = webdriver.Edge()
browser.get('https://www.zhihu.com/explore')
# 获得所有cookie信息
print('原cookies：\n', browser.get_cookies())
# 返回cookies字典key为“name”的cookie信息
print('key为name的cookie：\n', browser.get_cookie('name'))
# 添加cookie  {字典:键值对}形式添加
browser.add_cookie({'name': 'ethan', 'domain': 'www.zhihu.com', 'value': 'germey'})
print('添加cookie后的cookies：\n', browser.get_cookies())
# 删除cookie信息
browser.delete_cookie('name')
print('删除name的cookie后的cookies：\n', browser.get_cookies())
# 删除所有cookie信息
browser.delete_all_cookies()
print('删除所有cookies后的cookies：\n', browser.get_cookies())
```

首先，我们访问知乎，加载完成后，浏览器实际上已经生成 Cookies 了。接着，调用 get_cookies 方法获取所有的 Cookies。然后，我们再添加一个 Cookie，这里传入一个字典，有 name、domain 和 value 等内容。接下来，再次获取所有的 Cookies，可以发现，结果会多出这一项新加的 Cookie。最后，调用 delete_all_cookies 方法删除所有的 Cookies。再重新获取，发现结果就为空了。 




### 15. 异常处理

在使用 Selenium 的过程中，难免会遇到一些异常，例如超时、节点未找到等错误，一旦出现此类错误，程序便不会继续运行了。这里我们可以使用 try except 语句来捕获各种异常。

首先，演示一下节点未找到的异常，示例如下：

```powershell
from selenium import webdriver 
browser = webdriver.Chrome() 
browser.get('https://www.baidu.com') 
browser.find_element_by_id('hello')
```

这里我们首先打开百度页面，然后尝试选择一个并不存在的节点，此时就会遇到异常。

运行之后控制台的输出如下：

```powershell
NoSuchElementException Traceback (most recent call last) 
<ipython-input-23-978945848a1b> in <module>()
     3 browser = webdriver.Chrome()
     4 browser.get ('https://www.baidu.com')
----> 5 browser.find_element_by_id('hello')
```

可以看到，这里抛出了 NoSuchElementException 异常，通常代表节点未找到。为了防止程序遇到异常而中断，我们需要捕获这些异常，示例如下：

```python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
# 超时异常
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
# 缺少当前查看的元素
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
```

这里我们使用 try except 来捕获各类异常。比如，我们对 find_element_by_id() 查找节点的方法捕获 NoSuchElementException 异常，这样一旦出现这样的错误，就进行异常处理，程序也不会中断了。

控制台的输出如下：

```python
No Element
```

关于更多的异常类，可以参考官方文档：http://selenium-python.readthedocs.io/api.html#module-selenium.common.exceptions。

## 启动配置参数

[selenium启动Chrome配置参数问题 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/60852696)

每次当selenium启动chrome浏览器的时候，chrome浏览器很干净，没有插件、没有收藏、没有历史记录，这是因为selenium在启动chrome时为了保证最快的运行效率，启动了一个裸浏览器，这就是为什么需要配置参数的原因，但是有些时候我们需要的不仅是一个裸浏览器。

**selenium启动配置参数接收是ChromeOptions类**，创建方式如下：

```python
from selenium import webdriver
# 启动配置参数接收
option = webdriver.ChromeOptions()
# 接收 option.
# 启用配置参数
driver=webdriver.Chrome(chrome_option=chrome_option)
```

创建了ChromeOptions类之后就是添加参数，添加参数有几个特定的方法，分别对应添加不同类型的配置项目。

**设置 chrome 二进制文件位置 (binary_location)**

```python
from selenium import webdriver
option = webdriver.ChromeOptions()

# 添加启动参数
option.add_argument()

# 添加扩展应用 
option.add_extension()
option.add_encoded_extension()

# 添加实验性质的设置参数 
option.add_experimental_option()

# 设置调试器地址
option.debugger_address()
```

### 常用配置参数

```python
from selenium import webdriver
option = webdriver.ChromeOptions()

# 加载无窗口浏览器 linux下如果系统不支持可视化不加这条会启动失败
option.add_argument('--headless')
# 隐藏"Chrome正在受到自动软件的控制"
option.add_argument('disable-infobars')
# 告诉chrome去掉了webdriver痕迹
option.add_argument('--disable-blink-features=AutomationControlled')
# 屏蔽谷歌浏览器正在接收自动化软件控制提示
# 设置开发者模式启动，该模式下webdriver属性为正常值
option.add_experimental_option("excludeSwitches", ['enable-automation'])
# 反屏蔽https://bot.sannysoft.com/查看webdriver被检测(红色)的指纹
browser.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument', {
        'source': """
        Object.defineProperty(navigator, "webdriver", {
        get: () => undefined
        })
        """
})
# 使用代理IP
option.add_argument('--proxy--server=112.84.55.122:9999')
# 添加UA
option.add_argument('user-agent=MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
# 指定浏览器分辨率
option.add_argument('window-size=1920x3000') 
# 谷歌文档提到需要加上这个属性来规避bug
option.add_argument('--disable-gpu') 
# 隐藏滚动条, 应对一些特殊页面
option.add_argument('--hide-scrollbars')
# 使用硬盘来存储获取的内容，而不是使用内存，所以会稍稍降低分布式爬取时爬虫的速率。
option.add_argument('--disable-dev-shm-usage')
# 不加载图片, 提升速度
option.add_argument('blink-settings=imagesEnabled=false') 
# 以最高权限运行,使用-no-sandbox标记重新运行Chrome，禁止沙箱启动
option.add_argument('--no-sandbox')
# 手动指定使用的浏览器位置
option.binary_location = r"chrome.exe路径" 
#添加crx插件
option.add_extension('d:\crx\AdBlock_v2.17.crx') 
# 禁用JavaScript
option.add_argument("--disable-javascript") 
# 禁用浏览器弹窗
option.add_experimental_option(
    'prefs', prefs={
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
)

# 将参数启用
driver=webdriver.Chrome(chrome_option=chrome_option)
```

### 浏览器地址栏参数

在浏览器地址栏输入下列命令得到相应的信息

```python
about:version - 显示当前版本

about:memory - 显示本机浏览器内存使用状况

about:plugins - 显示已安装插件

about:histograms - 显示历史记录

about:dns - 显示DNS状态

about:cache - 显示缓存页面

about:gpu -是否有硬件加速

chrome://extensions/ - 查看已经安装的扩展
```

![](https://pic1.zhimg.com/80/v2-f6da4ed452d158a27204b99942a49610_720w.jpg)

### 其他配置项目参数

```python
# 指定用户文件夹User Data路径，可以把书签这样的用户数据保存在系统分区以外的分区
–user-data-dir=”[PATH]” 

# 指定缓存Cache路径
–disk-cache-dir=”[PATH]“ 

# 指定Cache大小，单位Byte
–disk-cache-size= 

# 重置到初始状态，第一次运行
–first run 

# 隐身模式启动
–incognito 
# 启动进入隐身模式
--incognito

# 无头浏览器
--headless

# 使用硬盘来存储获取的内容，而不是使用内存，所以会稍稍降低分布式爬取时爬虫的速率。
--disable-dev-shm-usage

# 禁用Javascript，如果觉得速度慢在加上这个
–disable-javascript 

# 将地址栏弹出的提示菜单数量改为num个
--omnibox-popup-count="num" 

# 修改HTTP请求头部的Agent字符串，可以通过about:version页面查看修改效果
--user-agent="xxxxxxxx" 

# 禁止加载所有插件，可以增加速度。可以通过about:plugins页面查看效果
--disable-plugins 

# 禁用java
--disable-java 

# 启动就最大化
--start-maximized 

# 取消沙盒模式
--no-sandbox 

# 单进程运行
--single-process 

# 每个标签使用单独进程
--process-per-tab 

# 每个站点使用单独进程
--process-per-site 

# 插件不启用单独进程
--in-process-plugins 

# 禁用弹出拦截
--disable-popup-blocking 

# 禁用插件
--disable-plugins 

# 禁用图像
--disable-images 

# 启用账户切换菜单
--enable-udd-profiles 

# 使用pac代理 [via 1/2]
--proxy-pac-url 

# 设置语言为简体中文
--lang=zh-CN 

# 自定义缓存目录
--disk-cache-dir 

# 自定义缓存最大值（单位byte）
--disk-cache-size 

# 自定义多媒体缓存最大值（单位byte）
--media-cache-size 

# 在工具 栏增加一个书签按钮
--bookmark-menu 

# 启用书签同步
--enable-sync 
```



### 反屏蔽

**网站https://bot.sannysoft.com/可以用来查看webdriver被检测的指纹有哪些，红色为被检测的。**

![](https://img-blog.csdnimg.cn/img_convert/7b056663e6cb6d7fca3526d718662189.png)

现在很多网站都加上了对 Selenium 的检测，来防止一些爬虫的恶意爬取。即如果检测到有人在使用 Selenium 打开浏览器，那就直接屏蔽。

其大多数情况下，**检测基本原理是检测当前浏览器窗口下的 window.navigator 对象是否包含 webdriver 这个属性**。因为在正常使用浏览器的情况下，这个属性是 undefined，然而一旦我们使用了 Selenium，Selenium 会给 window.navigator 设置 webdriver 属性。很多网站就通过 JavaScript 判断如果 webdriver 属性存在，那就直接屏蔽。

这边有一个典型的案例网站：https://antispider1.scrape.cuiqingcai.com/，这个网站就是使用了上述原理实现了 WebDriver 的检测，如果使用 Selenium 直接爬取的话，那就会返回如下页面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200818134925305.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
这时候我们可能想到直接使用 JavaScript 直接把这个 webdriver 属性置空，比如通过调用 execute_script 方法来执行如下代码：

```powershell
execute_script(Object.defineProperty(navigator, "webdriver", {get: () => undefined}))
```

这行 JavaScript 的确是可以把 webdriver 属性置空，但是 execute_script 调用这行 JavaScript 语句实际上是在页面加载完毕之后才执行的，执行太晚了，网站早在最初页面渲染之前就已经对 webdriver 属性进行了检测，所以用上述方法并不能达到效果。

在 Selenium 中，我们可以使用 CDP（即 Chrome Devtools-Protocol，Chrome 开发工具协议）来解决这个问题，通过 CDP 我们可以实现在每个页面刚加载的时候执行 JavaScript 代码，执行的 CDP 方法叫作 **Page.addScriptToEvaluateOnNewDocument**，然后传入上文的 JavaScript 代码即可，这样我们就可以在每次页面加载之前将 webdriver 属性置空了。另外我们还可以加入几个选项来隐藏 WebDriver 提示条和自动化扩展信息，代码实现如下：

```python
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
# 设置开发者模式启动，该模式下webdriver属性为正常值
option.add_experimental_option('excludeSwitches', ['enable-automation'])

option.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.cuiqingcai.com/')
```

这样整个页面就能被加载出来了：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200818135202355.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
对于大多数的情况，以上的方法均可以实现 Selenium 反屏蔽。但对于一些特殊的网站，如果其有更多的 WebDriver 特征检测，可能需要具体排查。

### 无头模式

上面的案例在运行的时候，我们可以观察到其总会弹出一个浏览器窗口，虽然有助于观察页面爬取状况，但在有些时候窗口弹来弹去也会形成一些干扰。

Chrome 浏览器从 60 版本已经支持了无头模式，即 Headless。无头模式在运行的时候不会再弹出浏览器窗口，减少了干扰，而且它减少了一些资源的加载，如图片等资源，所以也在一定程度上节省了资源加载时间和网络带宽。

我们可以借助于 ChromeOptions 来开启 Chrome Headless 模式，代码实现如下：

```powershell
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
browser.set_window_size(1366, 768)
browser.get('https://www.baidu.com')
browser.get_screenshot_as_file('preview.png')
```

这里我们通过 ChromeOptions 的 add_argument 方法添加了一个参数 --headless，开启了无头模式。在无头模式下，我们最好需要设置下窗口的大小，接着打开页面，最后我们调用 get_screenshot_as_file 方法输出了页面的截图。

运行代码之后，我们发现 Chrome 窗口就不会再弹出来了，代码依然正常运行，最后输出了页面截图如图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200818135420725.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODgxOTg4OQ==,size_16,color_FFFFFF,t_70#pic_center)
这样我们就在无头模式下完成了页面的抓取和截图操作。

现在，我们基本对 Selenium 的常规用法有了大体的了解。使用 Selenium，处理 JavaScript 渲染的页面不再是难事。

本节代码：https://github.com/Python3WebSpider/SeleniumTest

### 配置操作

拿google驱动举例

```python
from selenium import webdriver
options = webdriver.ChromeOptions()

# 禁止图片
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# 无头模式
option.add_argument("-headless")

# 通过设置user-agent
user_ag='MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; '+
'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
options.add_argument('user-agent=%s'%user_ag)

#隐藏"Chrome正在受到自动软件的控制"
options.add_argument('disable-infobars')

#设置代理
options.add_argument('proxy-server=' + '192.168.0.28:808')

#将浏览器最大化显示
browser.maximize_window() 

# 设置宽高
browser.set_window_size(480, 800)


# 通过js新打开一个窗口
driver.execute_script('window.open("https://www.baidu.com");')
browser = webdriver.Chrome(chrome_options=options)

```



### 绕过检测

**检测：**

```python
# 无处理
browser.get('https://bot.sannysoft.com/')
```

![selenium-绕过检测1](imgs\selenium-绕过检测1.png)

```python
# 设置 禁止检测特性=自动化控制
options.add_argument('--disable-blink-features=AutomationControlled')
```

![selenium-绕过检测2](imgs\selenium-绕过检测2.png)



```python
# 反屏蔽https://bot.sannysoft.com/查看webdriver被检测(红色)的指纹
browser.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument', {
        'source': """
        Object.defineProperty(navigator, "webdriver", {
        get: () => undefined
        })
        """
})
```

![selenium-绕过检测3](imgs\selenium-绕过检测3.png)





# selenium获取chrome控制台信息

```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# enable browser logging
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(desired_capabilities=d)

# load the desired webpage
driver.get('http://foo.com')

# print messages
for entry in driver.get_log('browser'):
    print(entry)
```

entry格式：

```
{'level': 'SEVERE', 'message': 'https://open.ccod.com/WARTC/cphoneRTC/verto-min.js 2086:28 "INVALID METHOD OR NON-EXISTANT CALL REFERENCE IGNORED" "verto.clientReady"', 'source': 'console-api', 'timestamp': 1626147049481}
```

其中source：

- console-api 控制台日志
- network 网络日志



## selenium教学案例

采集义务购商品网站

```
http://www.yiwugo.com/
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
from pymongo import MongoClient

class YWShop():

    def __init__(self, name, gather):
        # 禁止检测自动化控制
        options = webdriver.ChromeOptions()
        options.add_argument('disable-blink-features=AutomationControlled')
        # chrome_options已弃用被options替换
        self.browser = webdriver.Chrome(options=options)
        # 链接数据库
        # self.db = MongoClient()['python']['义乌购']
        self.db = MongoClient()[name][gather]

    def search(self, search_commodity):
        # 进入义乌购
        self.browser.get('http://www.yiwugo.com/')
        # 定位搜索框
        input_box = self.browser.find_element(By.ID, 'inputkey')
        # 输入需要查询的商品
        input_box.send_keys(search_commodity)
        # 点击搜索
        self.browser.find_element(By.XPATH, '//div[@class="search-index"]/span[@class="search-button"]').click()
        # input_box.send_keys(Keys.ENTER)  #导入Keys包

    def parse(self):
        # 滚到滚动条
        self.slide()
        # 定位商品
        li = self.browser.find_elements(By.XPATH, '//div[@class="pro_list_product_img2"]/ul')
        for i in li:
            # 标题
            title = i.find_element(By.XPATH, './/li[@class="titheight font_tit"]/a[@class="productloc"]')
            # 价格
            price = i.find_element(By.XPATH, './/li[@class="mt5px search13_price"]/span[@class="pri-left"]')
            # 销量
            sale = i.find_element(By.XPATH, './/li[@class="mt5px search13_price"]/span[@class="pri-right"]')
            # 厂家
            manufacturers = i.find_element(By.XPATH, './/li/font[@class="fontblue wid140"]/a')
            # 地址
            address = i.find_element(By.XPATH, './/li[@class="shshopname"]')
            items = {
                '标题': title.text,
                '价格': price.text,
                '销量': sale.text,
                '厂家': manufacturers.text,
                '地址': address.text,
            }
            self.save(items)
        # 翻页解析
        self.page()

    def slide(self):
        # 滚动页面
        for i in range(1, 10):
            self.browser.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{i/10}')
            time.sleep(random.randint(200, 500)/1000)

    def page(self):
        try:
            # 点击下一页 进行翻页
            next_page = self.browser.find_element(By.XPATH, '//div[@class="page_right"]/ul/a[@class="page_next_yes"]')
            # 存在下一页，点击进入并解析
            if next_page:
                next_page.click()
                self.parse()
            # 不存在下一页，退出
            else:
                self.browser.close()
        # 存在异常抛出异常信息
        except Exception as e:
            print(e)

    def save(self, data):
        # 储存数据
        if isinstance(data, dict):
            self.db.insert_one(data)
        else:
            print(data, '数据异常：Not dictionary format.')

    def run(self, search_commodity):
        self.search(search_commodity)
        # 等待数据加载
        time.sleep(2)
        self.parse()


if __name__ == '__main__':
    database_name = input('请输入存储数据的库名：')
    database_gather = input('请输入存储数据的集合名：')
    search_commodity = input('请输入要查询的商品：')
    # 将数据库名 集合名 传入属性
    yw = YWShop(database_name, database_gather)
    # 将搜索内容传入 '搜索'方法
    yw.run(search_commodity)
```



## 附录：

总结

```python
from selenium import webdriver
import unittest
import time


class GloryRoad(unittest.TestCase):
    # 测试前的初始化工作
    # @classmethod
    # def setUpClass(cls):
    # # cls.driver=webdriver.Chrome()
    # options = webdriver.ChromeOptions()
    # options.add_argument(’–headless’)
    # cls.driver = webdriver.Chrome(options=options)
    # # 1.访问网站1,添加断言
    # def test_visiturl(self):
    # visiturl = ‘http://www.baidu.com’
    # self.driver.get(visiturl)
    # # assert '百度0’in self.driver.page_source
    # # 断言
    # assert self.driver.title.find('百度') >= 0, ‘页面标题不包含：百度’

    # 2打开两个网站前进或者后退
    def test_visitur2(self):
        visiturl = 'http://www.baidu.com'
        visitur2 = 'http://www.so.com'
        self.driver.get(visiturl)
        self.driver.get(visitur2)
        self.driver.back()
        self.driver.forward()

    # 3刷新当前页面
    def test_visitur3(self):
        visitur3 = 'http://www.sogou.com'
        self.driver.get(visitur3)
        self.driver.refresh()

    # 4浏览器窗口最大化
    def test_visitur4(self):
        visitur4 = 'http://www.sogou.com'
        self.driver.get(visitur4)
        self.driver.maximize_window()

    # 5获取并设置当前窗口在屏幕上位置
    def test_visitur5(self):
        visitur5 = 'http://www.sogou.com'
        self.driver.get(visitur5)
        # 获取当前窗口在屏幕上位置
        position = self.driver.get_window_position()
        print('横坐标：', position['x'])
        print('纵坐标：', position['y'])
        # 设置当前窗口在屏幕上位置
        self.driver.set_window_position(x=400, y=200)
        print(self.driver.get_window_position())
    # 6获取浏览器窗口大小，返回字典类型数据
    def test_visitur6(self):
        visitur6 = 'http://www.sogou.com'
        self.driver.get(visitur6)
        # 获取当前窗口在屏幕上位置
        size_Dict = self.driver.get_window_size()
        print('当前浏览器的宽：', size_Dict['width'])
        print('当前浏览器的高：', size_Dict['height'])
        # 设置浏览器窗口的大小
        self.driver.set_window_size(width=400, height=200,windowHandle='current')
        print(self.driver.get_window_size())
    # 7获取页面的title属性值
    def test_visitur7(self):
        visitur7 = 'http://www.baidu.com'
        self.driver.get(visitur7)
        current_web_title = self.driver.title
        print('当前网页的title属性值为：', current_web_title)
        #断言页面的title属性是否是“百度一下，你就知道”
        self.assertEqual(current_web_title,"百度一下，你就知道","页面title属性错误！")
    #8获取页面HTML源代码
    def test_visitur8(self):
        visitur8 = 'http://www.baidu.com'
        self.driver.get(visitur8)
        pagesource = self.driver.page_source
        # print('当前网页的源码为：', pagesource)
        #断言页面源码是否是包含“新闻”关键字，以此判断页面内容正确性
        self.assertTrue("新闻" in pagesource,"页面源码未找到'新闻'关键字")
    #9获取当前页面的URL地址
    def test_visitur9(self):
        visitur9 = 'http://www.baidu.com'
        self.driver.get(visitur9)
        currentpageurl = self.driver.current_url
        print('当前网页的URL为：', currentpageurl)
        #断言当前页面网址是否为https://www.baidu.com/
        self.assertEqual(currentpageurl, "https://www.baidu.com/", "当前网址非预期网址!")

    # 10获取当前页面的元素基本信息
    def test_visitur10(self):
        visitur10 = 'http://www.baidu.com'
        self.driver.get(visitur10)
        # 查找百度首页上的"新闻"链接元素
        newsElement = self.driver.find_element_by_xpath("//a[text()='新闻']")
        # 获取査找到的"新闻”链接元素的基本信息
        print("元素的标签名：", newsElement.tag_name)
        print("元素的 size:", newsElement.size)
    # 11获取当前页面的元素文本内容
    def test_visitur11(self):
        visitur11 = 'http://www.baidu.com'
        self.driver.get(visitur11)
        import time
        time.sleep(3)
        # 通过xpath定位方式找到id属性值为"ul"的div元素下的第一个链接元素
        aElement = self.driver.find_element_by_xpath("//*[@class='mnav'][1]")
        # 通过找到的链接元素对象的text属性获取到链接元素的文本内容
        a_text = aElement.text
        self.assertEqual(a_text, "新闻")
    #12判断页面元素是否可见
    def test_getWebElementIsDisplayed12(self):
        import os
        url12 = 'file:///' + os.path.abspath('A_12.html')
        # 访问自定义的HTML网页
        self.driver.get(url12)
        # 通过"div2"找到第二个div元素
        div2 = self.driver.find_element_by_id("div2")
        # 判断第二个div元素是否在页面上可见
        print(div2.is_displayed())
        # 单击第一个切换div按钮，将第二个div显示在页面上
        self.driver.find_element_by_id("button1").click()
        # 再次判断第二个div元素是否可见
        print(div2.is_displayed())
        # 通过id="div4"找到第四个div元素
        div4 = self.driver.find_element_by_id("div4")
        # 判断第四个div元素是否在页面上可见
        print(div4.is_displayed())
        # 单击第二个切换div按钮，将第四个div显示在页面上
        self.driver.find_element_by_id("button2").click()
        # 再次判断第四个div元素是否可见
        print(div4.is_displayed())
    #13判断页面元素是否可操作
    def test_getWebElementIsEnablec13(self):
        import os
        url13 = 'file:///' + os.path.abspath('A_13.html')
        # 访问自定义的HTML网页
        self.driver.get(url13)
        # 通过id找到第一个input元素
        input1 = self.driver.find_element_by_id("input1")
        # 判断第一个input元素是否可操作
        print(input1.is_enabled())
        # 通过id找到第二个:input元素
        input2 = self.driver.find_element_by_id("input2")
        # 判断第二个input元素是否可操作
        print(input2.is_enabled())
        # 通过id找到第三个input元素
        input3 = self.driver.find_element_by_id("input3")
        # 判断第三个input元素是否可操作
        print(input3.is_enabled())
    #14获取页面元素的属性
    def test_getWebElementAttribute14(self):
        url = "http://www.sogou.com"
        # 访问sogou首页
        self.driver.get(url)
        # 找到搜索输入框元素
        searchBox = self.driver.find_element_by_id("query")
        # 获取搜索输入框页面元素的name属性值
        print(searchBox.get_attribute("name"))
        # 向搜索输入框中输入"Selinum3"内容
        searchBox.send_keys("Selinum3")
        # 获取页面搜索框的value属性值(即搜索输入框的文字内容)
        print(searchBox.get_attribute("value"))
    #15获取页面元素的CSS属性值
    def test_getWebElementAttribute15(self):
        url = "http://www.baidu.com"
        # 访问百度首页
        self.driver.get(url)
        # 找到搜索输入框元素
        searchBox = self.driver.find_element_by_id("kw")
        # 使用页面元素对象的value_of_css_property()方法获取元素的CSS属性值
        print("搜索输入框的高度是：", searchBox.value_of_css_property("height"))
        print("搜索输入框的宽度是：", searchBox.value_of_css_property("width"))
        font = searchBox.value_of_css_property("font-family")
        print("搜索输入框的字体是：", font)
        # 断言搜索输入框的字体是否是arial字体
        self.assertEqual(font, "arial")
    #16.清空输入框中的内容
    def test_clearInputBoxText16(self):
        url = "http://www.baidu.com"
        # 访问百度网页
        self.driver.get(url)
        # 获取输入框页面对象
        input = self.driver.find_element_by_id("kw")
        input.send_keys("selenium")
        import time
        time.sleep(3)
        # 清除输人框中默认内容
        input.clear()
        # 等待3秒，主要看清空输入框内容后的效果
        time.sleep(3)
    #17在输入框中输入指定内容
    def test_sendTextToInputBoxText17(self):
        import os
        # url = "d:\\test.html"
        url = 'file:///' + os.path.abspath('a_17.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 获取输入框页面对象
        input = self.driver.find_element_by_id("text")
        # 清除输入框中默认内容
        input.clear()
        input.send_keys(u"我是输入的文本内容")
        # 导入time包
        import time
        # 等待3秒，主要看清空输入框内容后的效果
        time.sleep(3)
    # 18单击按钮
    def test_clickButton18(self):
        import os
        # url = "d:\\test.html"
        url = 'file:///' + os.path.abspath('A_18.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 获取按钮页面对象
        button = self.driver.find_element_by_id("button")
        # 模拟鼠标左键单击操作
        button.click()
        import time
        time.sleep(3)
    #19双击某个元素
    def test_doubleClick19(self):
        import os
        # url = "d:\\test.html"
        url = 'file:///' + os.path.abspath('A_19.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 获取页面输入元素
        inputBox = self.driver.find_element_by_id("inputBox")
        # 导入支持双击操作的模块
        from selenium.webdriver import ActionChains
        # 开始模拟鼠标双击操作
        action_chains = ActionChains(self.driver)
        action_chains.double_click(inputBox).perform()
        import time
        time.sleep(3)
        # 执行后双击input框，背景颜色将变为红色
    # 20操作单选下拉列表
    def test_printSelectText20(self):
        import os
        url = 'file:///' + os.path.abspath('A_20.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 使用name属性找到页面上name属性为"fruit”的下拉列表元素
        select = self.driver.find_element_by_name("fruit")
        all_options = select.find_elements_by_tag_name("option")
        for option in all_options:
            print("选项显示的文本：", option.text)
            print("选项值为：", option.get_attribute("value"))
            option.click()
            time.sleep(1)
        #20操作单选下拉列表（2）
        from selenium.webdriver.common.action_chains import ActionChains
        self.driver.get('http://www.baidu.com')
        setting = self.driver.find_element_by_link_text('设置')
        ActionChains(self.driver).move_to_element(setting).perform()  # 需要加.perform() 执行一下
        self.driver.find_element_by_link_text('高级搜索').click()
        self.driver.find_elements_by_class_name('c-input')
        time.sleep(2)
        # 导入Select包
        from selenium.webdriver.support.ui import Select
        ft = self.driver.find_element_by_name('ft')
        # 实例化一个select对象
        ft_list = Select(ft)
        print(type(ft), type(ft_list))
        ft_list.select_by_value('rtf')  # 通过value选择
        ft_list.select_by_index(1)  # 通过索引选择
        ft_list.select_by_visible_text('所有格式')  # 文本
    #21断言单选列表选项值
    def test_visitURL21(self):
        import os
        url='file:///'+os.path.abspath('A_20.html')
        self.driver.get(url)
        #导入select模块
        from selenium.webdriver.support.ui import Select
        select_element=Select(self.driver.find_element_by_xpath('/html/body/select'))
        #获取所有选项的页面元素对象
        actual_options=select_element.options
        except_optionslist=['桃子','西瓜','橘子','猕猴桃','山楂','荔枝']
        actual_options_list=list(map(lambda option:option.text,actual_options))
        self.assertListEqual(except_optionslist,actual_options_list)
    #22操作多选的选择列表
    def test_operateMultipleOptionDropList22(self):
        import os
        url = 'file:///' + os.path.abspath('A_22.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 导入Select模块
        from selenium.webdriver.support.ui import Select
        import time
        # 使用xpath定位方式获取select页面元素对象
        select_element = Select(self.driver.find_element_by_xpath("//select"))
        # 通过序号选择第一个元素
        select_element.select_by_index(0)
        # 通过选项的文本选择"山楂"选项
        select_element.select_by_visible_text("山楂")
        # 通过选项的value属性值选择value = "mihoutao"的选项
        select_element.select_by_value("mihoutao")
        # 打印所有的选中项文本
        for option in select_element.all_selected_options:
            print(option.text)
        # 取消所有已选中项
        select_element.deselect_all()
        time.sleep(2)
        print("------再次选中3个选项------")
        #用索引定位元素
        select_element.select_by_index(1)
        # 用文本定位元素
        select_element.select_by_visible_text("荔枝")
        #用value值定位元素
        select_element.select_by_value("juzi")
        # 通过选项文本取消已选中的文本为"荔枝"选项
        select_element.deselect_by_visible_text("荔枝")
        # 通过序号取消已选中的序号为1的选项
        select_element.deselect_by_index(1)
        # 通过选项的value属性值取消已选中的value = "juzi"的选项
        select_element.deselect_by_value("juzi")
    # 23操作可以输入的下拉列表（输入的同时模拟按键）
    def test_operateMultipleOptionDropList23(self):
        import os
        url = 'file:///' + os.path.abspath('A_23.html')
        self.driver.get(url)
        # 导入模拟键盘模块
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element_by_id("select").clear()
        import time
        time.sleep(1)
        # 输入的同时按下箭头键
        self.driver.find_element_by_id("select").send_keys("c", Keys.ARROW_DOWN)
        self.driver.find_element_by_id("select").send_keys(Keys.ARROW_DOWN)
        self.driver.find_element_by_id("select").send_keys(Keys.ENTER)
        time.sleep(3)
    #24操作单选框,is_selected判断元素是否被选中
    def test_operateRadio24(self):
        import os
        url = 'file:///' + os.path.abspath('A_24.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 使用xpath定位获取value属性值为’berry’的input元素对象，也就是"草莓"选项
        berryRadio = self.driver.find_element_by_xpath("//input[@value = 'berry']")
        # 单击选择"草莓"选项
        berryRadio.click()
        # 断言"草莓”单选框被成功选中
        self.assertTrue(berryRadio.is_selected(), "草莓单选框未被选中！")
        if berryRadio.is_selected():
            # 如果"草莓"单选框被成功选中，重新选择n西瓜"选项
            watermelonRadio = self.driver.find_element_by_xpath("//input[@value ='watermelon']")
            watermelonRadio.click()
            # 选择"西瓜"选项以后，断言"草莓"选项处于未被选中状态
            self.assertFalse(berryRadio.is_selected())
        # 査找所有name属性值为"fruit"的单选框元素对象，并存放在radioList列表中
        radioList = self.driver.find_elements_by_xpath("//input[ @narae='fruit']")
        '''
        循环遍历radioList中的每个单选按钮，查找value属性值为"orange"的单选框,
        如果找到此单选框以后，发现未处于选中状态，则调用click方法选中该选项.'''
        for radio in radioList:
            if radio.get_attribute("value") == "orange":
                if not radio.is_selected():
                    radio.click()
                    self.assertEqual(radio.get_attribute("value"), "orange")
    #25.操作复选框
    def test_operateCheckBox25(self):
        import os
        url = 'file:///' + os.path.abspath('A_25.html')
        self.driver.get(url)
        # 使用xpath定位获取value属性值为'berry'的input元素对象，也就是"草莓"选项
        berryCheckBox = self.driver.find_element_by_xpath("//input[@value = 'berry' ]")
        # 单击选择"草莓"选项
        berryCheckBox.click()
        # 断言"草莓"复选框被成功选中
        self.assertTrue(berryCheckBox.is_selected(), u"草莓复选框未被选中！")
        if berryCheckBox.is_selected():
            # 如果"草莓"复选框被成功选中，再次单击取消选中
            berryCheckBox.click()
            # 断言"草莓"复选框处于未选中状态
            self.assertFalse(berryCheckBox.is_selected())
        # 査找所有name属性值为"fruit"的复选框元素对象，并存放在checkBoxList列表中
        checkBoxList = self.driver.find_elements_by_xpath("//input[@name = 'fruit']")
        # 遍历checkBoUst列表中的所有复选框元素，让全部复选框处于被选中状态
        for box in checkBoxList:
            if not box.is_selected():
                box.click()
    # 26.断言页面源码中的关键字
    def test_assertKeyWord26(self):
        url = "http://www.baidu.com"
        # 访问百度首页
        self.driver.get(url)
        self.driver.find_element_by_id("kw").send_keys(u"selenium")
        self.driver.find_element_by_id("su").click()
        import time
        time.sleep(4)
        # 通过断言页面是否存在某些关键字来确定页面按照预期加载
        assert "selenium" in self.driver.page_source, u"页面源码中不存在该关键字！"
    #27对当前浏览器窗口截屏
    def test_captureScreenInCurrentWindow27(self):
        url = "http://www.sogou.com"
        # 访问搜狗首页
        self.driver.get(url)
        try:
            '''
            调用get_screenshot_as_f ile(filename)方法，对浏览器当前打开页面
            进行截图，并保为C盘下的screenPicture.png文件
            '''
            result = self.driver.get_screenshot_as_file(r"C:\Users\Administrator\PycharmProjects\untitled58\screenPicture.png")
            print(result)
        except IOError as e:
            print(e)
    #28.模拟键盘单个按键操作
    def test_simulateASingleKeys28(self):
        from selenium.webdriver.common.keys import Keys
        url = "http://www.sogou.com"
        self.driver.get(url)
        query = self.driver.find_element_by_id("query")
        query.send_keys(Keys.F12)
        time.sleep(3)
        query.send_keys(Keys.F12)
        query.send_keys("selenium3")
        query.send_keys(Keys.ENTER)
        time.sleep(3)
    # 29.模拟组合按键操作
    def test_simulationCombinationKeys29(self):
        url = "http://www.baidu.com"
        # 访问百度首页
        self.driver.get(url)
        # 将焦点切换到搜索输人框中
        input = self.driver.find_element_by_id("kw")
        input.click()
        input.send_keys(u"Selenium3")
        time.sleep(2)
        from selenium.webdriver import ActionChains
        from selenium.webdriver.common.keys import Keys
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a'). \
            key_up(Keys.CONTROL).perform()
        time.sleep(2)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('x'). \
            key_up(Keys.CONTROL).perform()
        self.driver.get(url)
        self.driver.find_element_by_id("kw").click()
        # 模拟Ctrl + V组合键,将从剪贴板中获取到的内容粘贴到搜索输入框中
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v'). \
            key_up(Keys.CONTROL).perform()
        # 单击"百度一下"搜索按钮
        self.driver.find_element_by_id("su").click()
        time.sleep(3)
    # #30.模拟鼠标右键
    # from selenium.webdriver import ActionChains
    # from selenium.webdriver.common.keys import Keys
    # import time
    # import win32clipboard as w
    # import win32con
    # def setText(aString):
    #     w.OpenClipboard()
    #     w.EmptyClipboard()
    #     w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    #     w.CloseClipboard()
    # def test_rigthClickMouse(self):
    #     url = "http://www.sogou.com"
    #     # 访问搜狗首页
    #     self.driver.get(url)
    #     # 找到搜索输人框
    #     searchBox = self.driver.find_element_by_id("query")
    #     # 将焦点切换到搜索输入框
    #     searchBox.click()
    #     time.sleep(2)
    #     # 在搜索输入框上执行一个鼠标右键单击操作
    #     ActionChains(self.driver).context_click(searchBox).perform()
    #     # 将"gloryroad"数据设置到剪贴板中，相当于执行了复制操作
    #     setText(u'gloryroad')
    #     # 发送一个粘贴命令，字符P指代粘贴操作
    #     ActionChains(self.driver).send_keys('P').perform()
    #     # 单击搜索按钮
    #     self.driver.find_element_by_id('stb').click()
    #     time.sleep(2)
    # 31模拟鼠标左键按下与释放
    def test_simulationLeftClickMouseOfProcess31(self):
        import os
        url = 'file:///' + os.path.abspath('A_31.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        div = self.driver.find_element_by_id("div1")
        from selenium.webdriver import ActionChains
        import time
        # 在id属性值为"div1"的元素上执行按下鼠标左键，并保持
        ActionChains(self.driver).click_and_hold(div).perform()
        time.sleep(2)
        # 在id属性值为”div1”的元素上释放一直按下的鼠标左键
        ActionChains(self.driver).release(div).perform()
        time.sleep(2)
        ActionChains(self.driver).click_and_hold(div).perform()
        time.sleep(2)
        ActionChains(self.driver).release(div).perform()
    # 32保持鼠标悬停在某个元素上
    def test_roverOnElement32(self):
        import os
        url = 'file:///' + os.path.abspath('A_32.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        # 找到页面上第一个链接元素
        link1 = self.driver.find_element_by_partial_link_text(u"鼠标指过来1")
        # 找到页面上第二个链接元素
        link2 = self.driver.find_element_by_partial_link_text(u"鼠标指过来2")
        # 找到页面上的p元素
        p = self.driver.find_element_by_xpath("//p")
        print(link1.text, link2.text)
        # 导入需要的Python包
        from selenium.webdriver import ActionChains
        import time
        # 将鼠标悬浮到第一个链接元素上
        ActionChains(self.driver).move_to_element(link1).perform()
        time.sleep(2)
        # 将鼠标从第一个链接元素移动到P元素上
        ActionChains(self.driver).move_to_element(p).perform()
        time.sleep(2)
        # 将鼠标悬浮到第二个链接元素上
        ActionChains(self.driver).move_to_element(link2).perform()
        time.sleep(2)
        # 将鼠标从第二个链接元素移动到P元素上
        ActionChains(self.driver).move_to_element(p).perform()
        time.sleep(2)
    # 33.判断页面元素是否存在
    def isElementPresent(self, by, value):
        # 从 selenium.common.exceptions 模块导入 NoSuchElementException 异常类
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            # 打印异常信息
            print(e)
            # 发生了 NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    def test_isElementPresent33(self):
        url = "http://www.sogou.com"
        # 访问sogou首页
        self.driver.get(url)
        # 判断页面元素id属性值为"query"的页面元素是否存在
        res = self.isElementPresent("id", "query")
        if res is True:
            print(u"所查找的元素存在于页面上！")
        else:
            print(u"页面中未找到所需要的页面元素！")
    # 34 隐式等待implicitly_wait()
    def test_iraplictWait34(self):
        # 导入异常类
        from selenium.common.exceptions import NoSuchElementException, TimeoutException
        # 导入堆栈类
        import traceback
        url = "http://www.sogou.com"
        # 访问sogou首页
        self.driver.get(url)
        # 通过driver对象impUcitly_wait()方法来设置隐式等待时间，最长等待10秒
        self.driver.implicitly_wait(10)
        try:
            # 査找sogou首页的搜索输人框页面元素
            searchBox = self.driver.find_element_by_id("query")
            # 在搜索输人框中输入"selenium3"
            searchBox.send_keys(u"selenium3")
            # 査找sogou首页搜索按钮页面元素
            click = self.driver.find_element_by_id("stb")
            # 单击搜索按钮
            click.click()
        except (NoSuchElementException, TimeoutException) as e:
            # 打印异常的堆栈信息
            traceback.print_exc()
    # 35显示等待WebDriverWait()
    def test_explicitWait35(self):
        # 导入堆栈类
        import traceback
        # 导入By类
        from selenium.webdriver.common.by import By
        # 导入显式等待类
        from selenium.webdriver.support.ui import WebDriverWait
        # 导入期望场景类
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        import os
        url = 'file:///' + os.path.abspath('A_35.html')
        # 访问自定义的HTML网页
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 10, 0.2)
            wait.until(EC.title_is(u"你喜欢的水果"))
            print(u"网页标题是'你喜欢的水果'")
            # 等待10秒,直到要找的按钮出现
            element = WebDriverWait(self.driver, 10).until \
                (lambda x: x.find_element_by_xpath \
                    ("//input[@value = 'Display alert box']"))
            element.click()
            # 等待alert框出现
            alert = wait.until(EC.alert_is_present())
            # 打印alert框体消息
            print(alert.text)
            # 确认警告信息
            alert.accept()
            # 获取id属性值为"peach"的页面元素
            peach = self.driver.find_element_by_id("peach")
            # 判断id属性值为"peach"的页面元素是否能被选中
            peachElement = wait.until(EC.element_to_be_selected(peach))
            print(u"下拉列表的选项'桃子'目前处于选中状态")
            # 判断复选框是否可见并且能被单击
            wait.until(EC.element_to_be_clickable((By.ID, 'check')))
            print("复选框可见并且能被单击")
        except TimeoutException as e:
            # 捕获 TimeoutException 异常
            print(traceback.print_exc())
        except NoSuchElementException as e:
            # 捕获 NoSuchElementException 异常
            print(traceback.print_exc())
        except Exception as e:
            # 捕获其他异常
            print(traceback.print_exc())


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
```

