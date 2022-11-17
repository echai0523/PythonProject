# Re
在线工具，注意是js实现的 每个语言可能对正则实现是不一样的
https://tool.lu/regex

# 元字符
`metacharacter`

## 常见符号

> `.`：表示匹配任意单个字符，除了换行符，当re.S标记被指定时，则可以匹配包括换行符的任意字符
>
> `\`：转义后面的一个字符
>
> `[` 和 `]`：表示字符集合，如果单独表示本身需要转义 [Ar]、[0-9]、[A-Za-z]
>
> `-`：英文连字符。仅在上面的字符集合中使用，在集合外代表本身。
>
> `[^]`：[后面紧跟着^代表排除集合内元素
>
> 
>
> `^`在开头表示开始，`$`在末尾表示结尾。
>
> ***注意：***在[]内的字符不一定代表符号外的含义。
>
> 如：`+`在外面表示1或多次，在[]代表`+`这个符号，在()外如果要匹配`+`得使用`\+`，在()内元字符会默认转义，`[]`、`-`、`\`除外。


```python
# 最后一位为\可以通过 `\\`或`\x5C`转义
a = '字符串内\\'
# b = r'字符串内\'  # EOL  # \不能出现在最后一位，加r也不行
print(re.match(r"\x5C", r"\我"))
# 这个情况如果不加r会报错，因为\x5c会先被转成斜杆

print(re.match(r"[aj\x5Cc]+", r"aj\\c"))  # 后面的其实有两个\
print(re.match(r"[aj\\c]+", r"aj\\c"))
# 1. \不能作为集合中最后一个.或者
# 2. []内会对一些特殊字符进行默认转移义，也就是[\+]和[+]其实是一样的，两种写法都可以
# 3. 以上的除外情况是 \ - [] 另外^在开头表示除外

print(re.match("[\/]+", r"/"))
# 许多正则表达式/是不需要转义的，但是有些解析器要求必须这么做
```

## 常见转义

> \w	匹配字母数字及下划线
> \W	匹配非字母数字及下划线
> \s	匹配任意空白字符，等价于[ \t\n\r\f\v]。
> \S	匹配任意非空字符
> \d	匹配任意数字，等价于 [0-9].
> \D	匹配任意非数字
> \b	匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。
> \B	匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。
> \n, \t, 等.	匹配一个换行符。匹配一个制表符。等
>
> 
>
> \A	匹配字符串开始
> \Z	匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。
> \z	匹配字符串结束
> \G	匹配最后匹配完成的位置。

# 匹配机制
## 16进制

```python
print(re.match(".*\x0A.*", '''abd 
def'''))  # abd \ndef
# "\x0A" 在这里等价\n

print(re.match("\x0A", "\n"))  # \n
```
## 8进制

```python
# \0来表示匹配8进制
print(re.match("\011", '''\t'''))  # \t

r = re.match(".*", "i am abc")
print(r)  # i am abc

# r = re.match("[a-z\.]\.a","..a") # .在集合中转不转都是一样的 如果出现转义符，转义符不能出现在最后
print(r)  # ..a 
```

## 重复匹配

```python
print(re.match("^[\w.]+@[\w.]+\.\w+$", "abc@gmail.com.cn"))  # abc@gmail.com.cn
print(re.match("#[A-Fa-f0-9]{6}","#000000"))
print(re.match("#[A-Fa-f0-9]{6}","#ffffff"))
```

## 贪婪匹配
```python
re.match("<a>.*</a>","<a>one</a> <a>tow</a>")
re.match("(<a>.*?</a>)","<a>one</a> <a>tow</a>") # 在+ * {n,} {n,m}后加上?防止贪婪匹配
```

# 单词边界
```python
# 用边界的好处是，边界可以是开始 结束 或者空格或者tab等
re.match(r"\bcat\b","cat scattered his food all over the room.")  # cat

re.match(r"\bcat\b","catscattered his food all over the room.")  # 没有单独的cat 故不满足
re.match(r"\bcat\b","cat	scattered his food all over the room.") # cat 左右的边界符 也可以算做边界

re.findall(r"\b-\b","catscattered his fo - od all over the room.")
### 这个例子中匹配结果为空是因为-不在\w内  \w 定义是[A-Za-z0-9_]

# \B和 \b相反 匹配非边界是非单词的边界
re.findall(r"\Bcat\B","cat scattered his food all over the room.") # ['cat'] 找到的是中间单词中的cat
```
# 子表达式
```python
re.findall(r"&nbsp;{2,}",r"&nbsp;&nbsp;&nbsp;&nbsp;;;;;")
# ['&nbsp;;;;;'] 只能匹配到最后一个，因为正则表达式将;视为重复的元素
re.findall(r"(&nbsp;){2,}?",r"&nbsp;&nbsp;&nbsp;&nbsp;;;;;")
# ['&nbsp;', '&nbsp;'] 这里用括号讲前面的作为子表达式
#子表达式允许嵌套
#?:加在子表达式最前面用于不捕获分组
re.match(r"(?:\d+) (\w+) efg \1","12 abc efg abc")  # 12 abc efg abc
#groups() # ('abc',)
# 当表达式比较复杂时候，可以根据需要用子表达式进行归类分组，从而使表达式更清晰
```

# 或
```python
re.match("abc|efg","abc")  # 'abc'
re.match("abc|efg","efg")  # 'efg'
```

# 子表达值+或
```python
re.match("(19|20)\d{2}","2021")
re.match("(19|20)\d{2}","1901")  # '1901'
```

# 反向引用
```python
# 匹配html h标签 <h1> head1 </h1>   <h2> head2 </h2> ...
re.findall("<[hH][1-6]>.*?</[hH][1-6]>","<h1> head1 </h1> <h2> head2 </h2>  <h3> WRONG HEAD </h4> ")
# 这里会匹配到错误的标签   # ['<h1> head1 </h1>', '<h2> head2 </h2>', '<h3> WRONG HEAD </h4>']
#例子2 检查连续出现的单词
re.findall(r"[ ]+(\w+)[ ]+\1","this is a block of of abc efg abc is ok ok end")  # ['of', 'ok']
# 这里的子表达式并不是用来匹配重复的，而是对模式分组，将其标识以备后用，\1 最小是从1开始 \0不太常用，可用来表示整个表达式

for x in re.finditer(r"<[hH]([1-6])>.*?</[hH]\1>","<h1> head1 </h1> <h2> head2 </h2>  <h3> WRONG HEAD </h4> "):
    print(dir(x))
    break

for x in re.finditer(r"<[hH]([1-6])>.*?</[hH]\1>","<h1> head1 </h1> <h2> head2 </h2>  <h3> WRONG HEAD </h4> "):
    print(x.group(),"======", x.groups())
# <h1> head1 </h1> ====== ('1',)
# <h2> head2 </h2> ====== ('2',)
```

# 替换文本
```python
re.sub(r"(\w+[\w\.]*@[\w\w]+\.\w+)", r"<a href='mailto:\1'>\1</a>", "hello, my email is henry@gmail.com ,thanks.", count=0, flags=0)
# js中repl中用$1代替\1  # "hello, my email is <a href='mailto:henry@gmail.com'>henry@gmail.com</a> ,thanks."
```
# 替换的同时改变大小写
```python
# 替换h1中间的字都改成
re.sub(r"(<[hH]1>)(.*?)(</[hH]1>)",r"\1\2\3","<h1> head1 </h1> <h2> head2 </h2><h3> WRONG HEAD </h4> ", count=0, flags=0)
#   '<h1> head1 </h1> <h2> head2 </h2><h3> WRONG HEAD </h4> '
```

# 环视
## lookahead
```python
re.findall(r".+(?=:)",'''https://xx1
https://xx2
http://xx3
''')  # ['https', 'https', 'http']
# (?=:)是告诉匹配:只是为了往前查看,匹配的结果不包含这个子表达式内容

re.match(r".+(:)","https://") #  子表达式，匹配的内容包含:
# re.match(r".+(:)","https://").group()  # 'https:'
# re.match(r".+(:)","https://").groups()  #(':',)

re.findall(r"(?=://).+",'''https://xx1
https://xx2
http://xx3
''')   # ['://xx1', '://xx2', '://xx3']
```

## lookbehind
```python
re.findall(r"(?<=:).+",'''https://xx1
https://xx2
http://xx3
''')  # ['//xx1', '//xx2', '//xx3']
re.findall(r"(?<=://).+",'''https://xx1
https://xx2
http://xx3
''')  # ['xx1', 'xx2', 'xx3']
``` 

# 结合向前向后
```python
re.findall(r"(?<=<title>).*?(?=</title>)",r"<title>123abc</title>  <title>456efg</title>")  # ['123abc', '456efg']
```
# 否定式环视
```python
#只查找数量，不查找价格
re.findall(r"\b(?<!\$)\d+\b","i paid $30 for 100 apples, 50 oranges,I saved $5 on this order.")  # ['100', '50']

#只查找数量，不查找价格
re.findall(r"(?<!\$)\d+","i paid $30 for 100 apples, 50 oranges,I saved $5 on this order.")  # ['0', '100', '50']
# 如果不加\b 那么就会把 $30后面的0匹配进来 
```

# 嵌入条件
```python
for i in re.finditer("\(?\d{3}\)?-?\d{3}-\d{4}",'''
123-456-7890
(123)456-7890
(123)-456-7890
'''):
    print(i.group())
# 123-456-7890
# (123)456-7890
# (123)-456-7890
```

# 根据反向引用进行条件处理
```python
(?(back_ref)true_pattern) #没有else的pattern
(?(back_ref)true_pattern|false_pattern) #注意这里用到了两个括号，
# 其中? 代表的是条件
# back_ref_pattern代表的是反响引用
# 仅当反向引用出现时匹配true_pattern 否则 匹配false pattern

for i in re.finditer(r"(\()?\d{3}(?(1)\)|-)\d{3}-\d{4}",'''
123-456-7890
(123)456-7890
(123)-456-7890
'''):
    print(i.group())
# 123-456-7890
# (123)456-7890
```



# 根据环视进行条件处理
```python
for i in re.finditer(r"\d{5}(-\d{4})?",'''
12345
12345-1234
12345-
'''):
    print(i)
# 第三行也被匹配了
# <re.Match object; span=(1, 6), match='12345'>
# <re.Match object; span=(7, 17), match='12345-1234'>
# <re.Match object; span=(18, 23), match='12345'>

for i in re.finditer(r"\d{5}(?(?=-)-\d{4})",'''
12345
12345-1234
12345-
'''):
    print(i)
# 第三行也被匹配了
# error: bad character in group name '?=-' at position 8
```
 
# Python中的函数
## re.match    
```python
m = re.match("a\wc","abc efg abc")
m.group()  # 默认m.group(0) 匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组 相当于从groups()中提取对应 不过index从1开始。
m.groups() # 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
#match模式下只会有一个group

m2 = re.match( r'(.*) are (.*?) .*', "Cats are smarter than dogs", re.M|re.I)
m2.group()  # 返回整个字符串
m2.groups() # ('Cats', 'smarter')  # ('Cats', 'smarter')
```

## re.search
## re.sub
## re.compile
## findall
```python
# 返回每个匹配结果的groups
re.findall( r'(\w+) are (\w+)', "Cats are smarter then dog,Dog are bigger then cat.", re.M|re.I)
# [('Cats', 'smarter'), ('Dog', 'bigger')]
```

## re.finditer
```python
m2 = re.finditer( r'(\w+) are (\w+)', "Cats are smarter then dog,Dog are bigger then cat.", re.M|re.I)
for i in m2:
    print(i.group(0),i.groups(),i.start(),i.end(),i.span()) # group 正则匹配到的文本， groups 子表达式匹配到的文本
# Cats are smarter ('Cats', 'smarter') 0 16 (0, 16)
# Dog are bigger ('Dog', 'bigger') 26 40 (26, 40)
```

## re.split
