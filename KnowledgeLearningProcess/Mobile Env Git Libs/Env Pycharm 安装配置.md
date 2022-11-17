# Pycharm安装

1、进入官网PyCharm的下载地址：链接: http://www.jetbrains.com/pycharm/download/#section=windows.

![Pycharm安装1](.\imgs\Pycharm安装1.png)

2、professional表示专业版，community是社区版，推荐安装社区版，因为是免费使用的，我选择的是社区版，下载文件的储存位置出现pycharm-community-版本号。

![Pycharm安装2](.\imgs\Pycharm安装2.png)

3、点击安装，修改安装路径，建议安装C盘以外位置，修改好以后，点击Next。

![Pycharm安装3](.\imgs\Pycharm安装3.png)

4、建议不选择.py选项，这是关联文件，如果打钩了，以后电脑双击.java文件就会用它打开。

![Pycharm安装4](.\imgs\Pycharm安装4.png)

5、接下来点击Install，出现安装界面。

![Pycharm安装5](.\imgs\Pycharm安装5.png)

# 配置PyCharm环境

在创建项目之前，需要确认是否添加环境变量，也就是bin文件路径是否添加到系统环境变量中，如果没有添加，可能会导致创建项目时选择不了Python解释器。(选择性使用，如果可以使用可以跳过！！！)
1、右键我的电脑，点击属性，弹出如下界面

![Pycharm配置环境1](.\imgs\Pycharm配置环境1.png)

2、点击“高级系统设置”，点击“环境变量”。

![Pycharm配置环境2](.\imgs\Pycharm配置环境2.png)

3、找到系统变量里面的Path，双击编辑，点击新建，将pycharm程序路径（桌面右键图标-打开文件的所在位置）复制，点击“确定”。

![Pycharm配置环境3](.\imgs\Pycharm配置环境3.png)

![Pycharm配置环境4](.\imgs\Pycharm配置环境4.png)

# 使用PyCharm

1、双击图标，如下图依次点击。

![Pycharm使用1](.\imgs\Pycharm使用1.png)

![Pycharm使用2](.\imgs\Pycharm使用2.png)

![Pycharm使用7](.\imgs\Pycharm使用7.png)

2、选择“Evaluate for free”免费评估 “Evaluate” 。 【进行永久激活】

![Pycharm使用3](.\imgs\Pycharm使用3.png)

3、第一次使用，选择创建新项目“New Project”。

![Pycharm使用4](.\imgs\Pycharm使用4.png)

4、修改项目存放目录，建议**C盘以外**，其它默认即可，“learnpython”是我定义的项目名称。

![Pycharm使用5](.\imgs片\Pycharm使用5.png)

![Pycharm使用6](.\imgs\Pycharm使用6.png)

# Pycharm永久激活

> 【智小鱼】公众号 发送“激活码”
>
> 永久激活2089激活：支持2020.1.1；2019 / 2018 / 2017所有版本
>
> 补丁下载地址：https://pan.baidu.com/s/1BfcbT-UWDCj3MNsb62zSDQ
>
> 提取码：tm65
>
> 激活补丁【jetbrains-agent-latest.zip】
>
> ![Pycharm激活1](.\imgs\Pycharm激活1.png)
>
> 此教程适合2017 2018 2019 2020.1.1以下版本
>
> 因为版本较多，亲测2019 2.3和2020.1.1
>
> 激活教程大家可以参考：https://mp.weixin.qq.com/s/Qmnh7ou1OVgQ9iNRwAu1Mw

1、进入软件后，把激活补丁【jetbrains-agent-latest.zip】拖入到软件中的下图区域

![Pycharm激活2](.\imgs\Pycharm激活2.png)

2、然后点restart

![Pycharm激活3](.\imgs\Pycharm激活3.png)

3、软件自动重启后点为Pycharm安装【安装目录默认，不确定更改后是否还能用】

![Pycharm激活4](.\imgs\Pycharm激活4.png)

![Pycharm激活5](.\imgs\Pycharm激活5.png)

4、然后点help-register就可以看到已经激活成功了

![Pycharm激活6](.\imgs\Pycharm激活6.png)

![Pycharm激活7](.\imgs\Pycharm激活7.png)

# Pycharm项目解释器

![Pycharm项目解释器1](.\imgs\Pycharm项目解释器1.png)

![Pycharm项目解释器2](.\imgs\Pycharm项目解释器2.png)

![Pycharm项目解释器3](.\imgs\Pycharm项目解释器3.png)

# Python配置国内镜像源

python国内镜像源地址：
清华：https://pypi.tuna.tsinghua.edu.cn/simple
豆瓣：http://pypi.douban.com/simple/
阿里云：http://mirrors.aliyun.com/pypi/simple/
中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
华中理工大学：http://pypi.hustunique.com/
山东理工大学：http://pypi.sdutlinux.org/

![Pycharm镜像源1](.\imgs\Pycharm镜像源1.png)

![Pycharm镜像源2](.\imgs\Pycharm镜像源2.png)



永久修改：
windows下，直接在user目录中创建一个pip目录，如：C:\Users\Administrator\AppData\Roaming\pip，新建pip.txt文本，填写内容如下：

#### 配置一个镜像源

> [global]
> index-url = https://pypi.tuna.tsinghua.edu.cn/simple

#### 配置多个镜像源

> 

保存内容，将pip.txt文本重命名为pip.ini配置设置文件



# Pycharm汉化版配置

将汉化包文件【resources_zh_CN_IntelliJIDEA_2019.1_r1.jar】复制到pycharm安装路径下的lib文件夹内，如：D:\software\PyCharm 2019.3.5\lib ，重新启动Pycharm即可。

# Pycharm主题配置

在http://www.themesmap.com/theme.html上选择自己喜欢的主题点进去后进行下载。

![Pycharm主题配置1](.\imgs\Pycharm主题配置1.png)

【文件】 > 【设置】 > 【编辑器】 > 【常规】 > 【方案设置】 > 【导入方案】 > 【确定】

![Pycharm主题配置2](.\imgs\Pycharm主题配置2.png)



# Pycharm新建文件头部模板

[官方文档](https://www.jetbrains.com/help/pycharm/settings-file-and-code-templates.html#toolbar)

Pytharm 中可以自定义代码文件模板。
设置位置：

Settings(设置) >> Editor(编辑器) >> File and Code Templates(文件和代码模板) >> Python Script

然后在里面添加，可选的预设变量有：

```
${PROJECT_NAME} - 当前的项目名    【PythonProject】
${NAME} - 在文件创建过程中，新文件对话框的命名  【文件名】无文件后缀
${USER} - 当前的登录用户 
${DATE} - 现在的系统日期      【年/月/日】
${TIME} - 现在的系统时间      【时：分】
${YEAR} - 当前年份           【年】
${MONTH} - 当前月份          【月】
${DAY} - 当前月份中的第几日    【日】
${HOUR} - 现在的小时         【时】
${MINUTE} - 现在的分钟       【分】
${PRODUCT_NAME} - IDE创建文件的名称    【PyCharm】
${MONTH_NAME_SHORT} - 月份的前三个字母缩写   # 两个变量不是英文的月份，都是中文的月份
${MONTH_NAME_FULL} - 完整的月份名        # 两个变量不是英文的月份，都是中文的月份

#[[$END$]]#  -  光标定位
```

模板范例：

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: ${DATE} ${TIME}

input: 

output: 

Short Description: 

Change History:

Nymph Bless:
                    .::::.                          
                  .::::::::.                           
                 :::::::::::                         
              ..:::::::::::'                                      
           '::::::::::::'                                 
             .::::::::::                                 
        '::::::::::::::..                                    
             ..::::::::::::.                                 
           ``::::::::::::::::                                 
            ::::``:::::::::'        .:::.                   
           ::::'   ':::::'       .::::::::.                 
         .::::'      ::::     .:::::::'::::.                 
        .:::'       :::::  .:::::::::' ':::::.           
       .::'        :::::.:::::::::'      ':::::.        
      .::'         ::::::::::::::'         ``::::.        
  ...:::           ::::::::::::'              ``::.        
 ```` ':.          ':::::::::'                  ::::..     
                    '.:::::'                    ':'````..      
"""

#[[$END$]]#


```

# Pycharm设置编码

报错问题：

```
UnicodeEncodeError: 'gbk' codec can't encode character '\ue13b' in position 25: illegal multibyte se
```

虽然设置了encoding=‘utf-8’，但是在打印 print(sys.stdout.encoding)会发现结果是GBK

解决办法：Python使用terminal的编码规则去解码并print



# Pycharm插件

## AI结对程序员

- `GitHub Copilot` 下载后点击重启并应用。重启后右下角弹出登录Github授权Copilot插件。通过给的码粘贴到登录链接成功授权。



