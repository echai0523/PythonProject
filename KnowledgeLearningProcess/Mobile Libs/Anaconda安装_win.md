# 1 Anaconda下载
- 已下载好的Anaconda工具

  网盘链接: https://pan.baidu.com/s/1UTwvyPIAtho1triOxzmiyA
  提取码：ynim

- 也可通过下载Anaconda，一个是官网，另一个是国内镜像网站（建议选择这个）。

  可参考：https://blog.csdn.net/fan18317517352/article/details/123035625

# 2 Anaconda安装
**说明**：其实要是装Anaconda的话，就不用再单独装Python了。已经装好了Python也不影响你安装今天的Anaconda，但需要注意环境变量冲突的问题，需要手动配置Anaconda的环境变量。
- 直接找到刚才下载好的文件双击打开。选择Next。
- 跳了一个阅读协议，选择“I agree”。
- 两个选项，默认Just Me，选择All Users，然后next。
- **安装路径建议大家空间充裕还是装在C盘，避免使用过程中某些错误。如果想装在其他盘，建立一个新的件夹，D:\Anaconda，注意这个文件夹不要使用中文或者空格、特殊字符。选择对应安装目录，点next。**
- **在Advanced Installation Options中的Advanced Options高级选项：不要勾选**"Add Anaconda to my PATH environment variable"，**选择第二个选择**"Register Anaconda3 as the system Python 3.8"后续手动配置环境变量，避免与python环境变量冲突。点击Install。
- 等待安装完成。然后就是next ，再就是 finish，到这里就是安装结束。

# 3 手动配置环境变量
> 此电脑 > 属性 > 高级系统设置 > 环境变量 > 系统变量 > path > 编辑 > 新建
> > 根据自己实际安装目录，将路径添加进path。C:\ProgramData\Anaconda3\Scripts  # 若添加其他的可能造成python冲突

# 4 测试是否配置成功
- 输入 python，看是否有python环境。
  - 查看python版本后，要按下ctrl+z，再输入conda --version。
- 输入 conda --version；输入conda info也行，查询conda信息，看conda version版本号有无。
