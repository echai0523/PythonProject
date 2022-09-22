# osgeo安装

### 问题
- 安装：pip3 install osgeo
- 报错ERROR: Failed building wheel for osgeo

### 解决方法
[下载whl](https://www.lfd.uci.edu/~gohlke/pythonlibs)

根据python版本，下载对应的GDAL安装文件，如：python3.7下载`GDAL‑3.4.2‑cp37‑cp37m‑win_amd64.whl`
- cp37：python3.7 版本
- win_amd65：window64位
> pip install GDAL‑3.4.2‑cp37‑cp37m‑win_amd64.whl
- 注：anaconda也可以`conda install gdal`进行安装
