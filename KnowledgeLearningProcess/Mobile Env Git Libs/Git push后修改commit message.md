# 修改commit message
[已经git push的commit如何修改message](https://www.jianshu.com/p/ec45ce13289f)

### 命令
- 以下修复方式中，总共涉及这些命令
  - git log
  - git rebase -i HEAD~5
  - git commit --amend
  - git rebase --continue
  - git push -f
  
  注：在修复历史commit message的时候，请确保当前分支是最新代码，且已经提交了所有本地修改。

### 步骤
##### 查看历史记录
> git log
> 提交记录会按时间倒序展示

##### 确定要修改哪些commit
> git rebase -i HEAD~5
> 其中，HEAD~5表示最近的5个，后面的5可以改成其他数字。本例中我们只显示最近的5个。

- 左边第一列表示命令（command），中间一列表示commit id，最右边一列是我们之前提交的message
- 假设我们需要修改第2条和第4条commit的message，则需要将它们的命令（command），由pick改为edit，其它地方保持不变（此时还不用修改message）。
- 修改完成之后，保存修改。
```text
pick 1d316b0 1
edit f429786 2  <- 注意本行第一列的pick改为edit了
pick 880cfbc 3
edit c55cf56 4  <- 注意本行第一列的pick改为edit了
pick d10fd07 5
```
##### 修改每个edit的commit
- 轮流使用git commit --amend和git rebase --continue
  - git commit --amend
  - 此时弹出一个文本框，就可以修改message了，修改最上面的内容
  - 对修改进行保存
  - git rebase --continue
- 全部修改完成后，会提示
  - Successfully rebased and updated refs/heads/master.

##### 强制更新远程服务器
- git push -f
  - 切记一定要加-f，否则我们edit的commit会添加到commit后面，而不是更新原commit。
