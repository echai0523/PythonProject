# Windows pip 安装 TensorFlow2
## [使用 pip 安装 TensorFlow](https://tensorflow.google.cn/install/pip#system-install)
- TensorFlow 2 软件包现已推出
  - tensorflow：支持 CPU 和 GPU 的最新稳定版（适用于 Ubuntu 和 Windows）
  - tf-nightly：预览 build（不稳定）。Ubuntu 和 Windows 均包含 GPU 支持。
- 旧版 TensorFlow
  - 对于 TensorFlow 1.x，CPU 和 GPU 软件包是分开的：
    - tensorflow==1.15：仅支持 CPU 的版本
    - tensorflow-gpu==1.15：支持 GPU 的版本（适用于 Ubuntu 和 Windows）
- 系统要求
  - Python 3.6–3.9
    - 若要支持 Python 3.9，需要使用 TensorFlow 2.5 或更高版本。
    - 若要支持 Python 3.8，需要使用 TensorFlow 2.2 或更高版本。
  - pip 19.0 或更高版本（需要 manylinux2010 支持）
  - Ubuntu 16.04 或更高版本（64 位）
  - macOS 10.12.6 (Sierra) 或更高版本（64 位）（不支持 GPU）
    - macOS 要求使用 pip 20.3 或更高版本
  - Windows 7 或更高版本（64 位）
    - 适用于 Visual Studio 2015、2017 和 2019 的 Microsoft Visual C++ 可再发行软件包
  - GPU 支持需要使用支持 CUDA® 的卡（适用于 Ubuntu 和 Windows）
  **注意**：必须使用最新版本的 pip，才能安装 TensorFlow 2。

### 1. 在系统上安装 Python 开发环境
- 检查是否已配置 Python 环境：
  - 需要使用 Python 3.6-3.9 和 pip 19.0 及更高版本
    - python3 --version
    - pip3 --version

### 2. 安装 TensorFlow pip 软件包
1. 进入`https://pypi.org/search/?q=tensorflow`
2. 选择 tensorflow 2.9.1 如图
![选择 tensorflow 2.9.1](https://img2022.cnblogs.com/blog/2939899/202208/2939899-20220806104701847-161304536.jpg)
3. 进入终端(需要配置好python环境变量，否则需要进入到python安装目录下的Script文件夹，在路径位置输入cmd进入终端)，粘贴命令`pip install tensorflow`
![进入终端输入命令pip install tensorflow](https://img2022.cnblogs.com/blog/2939899/202208/2939899-20220806105131421-1842958356.jpg)
4. 完成tensorflow 2.9.1的安装

## 安装完成使用时出现的Error
由于版本不同，旧版本部分模块位置被移动，导致2.版本跑不通代码。
Error类型1：
  - AttributeError: module 'tensorflow' has no attribute 'Session'
  - AttributeError: module 'tensorflow' has no attribute 'placeholder'
  - 解决方式：
    - 1.版本导库方式：import tensorflow as tf
    - 2.版本导库方式：import tensorflow.compat.v1 as tf
Error类型2：
  - RuntimeError: tf.placeholder() is not compatible with eager execution.
  - 解决方式：
    - 2.版本需要添加：tf.compat.v1.disable_eager_execution()

## 版本1. -> 版本2. 案例
[1.版本eg](https://github.com/MorvanZhou/train-robot-arm-from-scratch/tree/master/part5)
需要修改的文件：https://github.com/MorvanZhou/train-robot-arm-from-scratch/blob/master/part5/rl.py
将：
> import tensorflow as tf

替换为：
> import tensorflow.compat.v1 as tf
> tf.compat.v1.disable_eager_execution()
