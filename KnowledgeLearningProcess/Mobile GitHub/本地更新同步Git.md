# GitHub

## 常用命令

### 本地更新同步GitHub脚本

相关链接：https://www.cnblogs.com/delav/p/11118555.html

1. 本地代码未修改，只有master分支，直接更新 

```python
git pull  # 必须是本地的代码没更改过
```

2. 本地代码有修改，多分支。

```python
# 切换到master分支
git checkout master

# 更新master分支
git pull

# 切换到自己的分支isso
git checkout isso

# 把master分支合并到自己分支
git merger master
```

3. 本地代码有修改，只有master分支，直接覆盖本地代码 

```python
# 重置索引和工作目录
git reset --hard  # 强制更新自己本地的代码，直接覆盖，本地的任何修改都不会保留
git pull
```