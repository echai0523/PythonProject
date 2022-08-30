# Numpy

NumPy是Python中科学计算的基础包（核心库）。NumPy来源于 *Numerical* 和 *Python* 两个单词。它是一个Python库，提供了一个高性能的多维数组对象ndarray，各种派生对象（如掩码数组和矩阵），以及用于数组快速操作的各种API，有包括数学、逻辑、形状操作、排序、选择、输入输出、离散傅立叶变换、基本线性代数，基本统计运算和随机模拟等等大量的库函数和操作，可以帮助程序员轻松地进行数值计算，广泛应用于机器学习模型、图像处理和计算机图形学、数学任务等领域。

1.  科学计算扩展程序库
    
    1.1 一个强大的N维数组对象 ndarray
    1.2 比较成熟(广播)的函数库
    1.3 用于整合C/C++/Fortran 代码的工具
    1.4 线性代数  傅力叶变换  随机数生成 矩阵  scipy(统计学)等功能
    
    
    
2.  高级的数值编程工具

    2.1 矩阵数据类型-> 小数 整数 字符串 布尔 复数.... (8 32 64 ...)
    2.2 运算库  矢量处理

**NumPy包的核心是 *ndarray* 对象。**

**NumPy的大部分功能的基础：矢量化和广播。**



## 1 数组ndarray

NumPy 最重要的一个特点是其 N 维数组对象 ndarray，它是一系列同类型数据的集合，以 0 下标为开始进行集合中元素的索引。

ndarray 对象是用于存放同类型元素的多维数组。

ndarray 中的每个元素在内存中都有相同存储大小的区域。

ndarray 内部由以下内容组成：

- 一个指向数据（内存或内存映射文件中的一块数据）的指针。
- 数据类型或 dtype，描述在数组中的固定大小值的格子。
- 一个表示数组形状（shape）的元组，表示各维度大小的元组。
- 一个跨度元组（stride），其中的整数指的是为了前进到当前维度下一个元素需要"跨过"的字节数。

ndarray 的内部结构:

![img](https://www.runoob.com/wp-content/uploads/2018/10/ndarray.png)

跨度可以是负数，这样会使数组在内存中后向移动，切片中 **obj[::-1]** 或 **obj[:,::-1]** 就是如此。



### 1、对象

```python
import numpy as np  # numpy模块

np.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
```

|  参数  | 描述                                                         |
| :----: | :----------------------------------------------------------- |
| object | 任何暴露数组接口方法的对象                                   |
| dtype  | 数据类型：int，float，complex(复数)                          |
|  copy  | 如果为 True，则 object 对象被复制，否则，只有当`__array__`返回副本，object 是嵌套序列，或者需要副本来满足任何其他要求（dtype，order等）时，才会生成副本。 |
| order  | 指定阵列的内存布局。 如果 object 不是数组，则新创建的数组将按行排列（C），如果指定了（F），则按列排列。 如果 object 是一个数组，则以下成立。C（按行）、F（按列）、A（原顺序）、K（元素在内存中的出现顺序） |
| subok  | 默认情况下，返回的数组被强制为基类数组。 如果为 True，则返回子类。 |
| ndmin  | 返回数组的最小维数                                           |



- **object实例**

**list中元素或嵌套列表以逗号( ',' )分割；数组中元素以空格( ' ' )分割，多维数组以换行( '\n' )分割。**

```python
import numpy as np

a = [1, 2, 3]   # 列表a
print(a)        # [1, 2, 3] 列表输出为列表(元素以','隔开)
# object=a
A = np.array(a) # 列表a转为一维数组
print(A)        # [1 2 3]  数组输出为数组(元素以' '隔开)

# object=b
b = [[1, 2, 3], [4, 5, 6]]  # 嵌套列表b
B = np.array(b)  # 嵌套列表b转为二维数组
print(b)  # [[1, 2, 3], [4, 5, 6]]
print(B)  # [[1 2 3]
          #  [4 5 6]]
```



- **dtype实例**

numpy 支持的数据类型比 Python 内置的类型要多很多，基本上可以和 C 语言的数据类型对应上，其中部分类型对应为 Python 内置的类型。下表列举了常用 NumPy 基本类型。

参考：https://www.runoob.com/numpy/numpy-dtype.html

**也可参考：数据类型部分**



- **float64三种写法:** dtype=np.float64、dtype=np.float_、dtype=float

- **float错误写法**：dtype=np.float(不是64，不存在该写法)、dtype=float16、dtype=float32···(除了64 其他都要加np.)

- **int32 三种写法：**dtype=np.int32、dtype=np.int_、dtype = int

- **int错误的写法：**dtype=np.int(不是32，不存在该写法)、dtype=int0、dtype=int8···(除了32 其他都要加np.)

```python
import numpy as np

a = [1, 2, 3]

A = np.array(a, dtype=np.float_)
# 或者
A_ = np.array(a, dtype=float)   

print(A)  # [1. 2. 3.]
print(A.dtype)  # float64
print(A_.dtype) # float64
print(type(A[0]))  # <class 'numpy.float64'>

A1 = np.array(a, dtype=np.float16)
print(A1)  # [1. 2. 3.] 
print(A1.dtype)  # float16
print(type(A1[0]))  # <class 'numpy.float16'>


b = [4, 5, 6]

B = np.array(b, dtype=np.int_) 
# 或者
B_ = np.array(b, dtype=int)

print(B)  # [4 5 6]
print(B.dtype)   # int32
print(B_.dtype)  # int32
print(type(B[0]))  # <class 'numpy.int32'>
```



- **copy实例**

copy类似深浅拷贝原则，copy默认为True

- True：拷贝object对象a生成副本b,a与b为**不同的对象**,后续**对a的处理不影响b**；

- False：不拷贝object对象a生成副本b,而是a与b为**同一个对象**,后续**对a的处理也影响b**。

```python
a = np.array([1, 2, 3])
# copy=True,对object对象a进行拷贝生成副本b,a与b为不同的对象,后续对a的处理不影响b
b = np.array(a, copy=True)
a[0] = 0

print(a) # [0 2 3]
print(b) # [1 2 3]

a = np.array([1, 2, 3])
# copy=False,不拷贝a生成副本b,而是a与b为同一个对象,后续对a的处理也影响b
b = np.array(a, copy=False)
a[0] = 0
print(a) # [0 2 3]
print(b) # [0 2 3]
```



- **order实例**

```python
# 顺序可选：['K'， 'A'， 'C'， 'F']
# 指定数组的内存布局。
# 如果object不是一个数组，新创建的数组将按C顺序(以行为主)，
# 除非指定了'F'，在这种情况下，它将按Fortran顺序(以列为主)。
# 如果object是一个数组，则以下内容保持不变。

# ===== ========= ===================================================
# order  no copy                     copy=True
# ===== ========= ===================================================
# 'K'   不变       F & C顺序保留，否则最相似的顺序
# 'A'   不变       如果输入是F而不是C，就是F阶，否则就是C阶
# 'C'   C order    C order
# 'F'   F order    F order
# ===== ========= ===================================================

# 当'copy=False'并且由于其他原因进行了复制时，结果与'copy=True'相同，但'A'有一些例外，请参阅Notes部分。 默认顺序是'K'。 
```



- **subok实例**

subok默认为False

- True：不转换类型
- False：转为ndarray类型

其中 `matrix` 是矩阵，将在之后的内容中介绍。

```python
a = np.matrix('1 2 7; 3 4 8; 5 6 9')
print(type(a))  # class 'numpy.matrix'>
print(a)  # [[1 2 7]
          #  [3 4 8]
          #  [5 6 9]]
at = np.array(a, subok=True)
af = np.array(a, subok=False)
aw = np.array(a) # 使用默认subok
print(type(at))  # <class 'numpy.matrix'>
print(type(af))  # <class 'numpy.ndarray'>
print(type(aw))  # <class 'numpy.ndarray'>

b = np.array([[1, 2, 7], [3, 4, 8], [5, 6, 9]])
print(type(b)) # <class 'numpy.ndarray'>
print(b)  # [[1 2 7]
          #  [3 4 8]
          #  [5 6 9]]
at = np.array(b, subok=True)
af = np.array(b, subok=False)
print(type(at))  # <class 'numpy.ndarray'>
print(type(af))  # <class 'numpy.ndarray'>
```



- **ndmin实例**

```python
a = [1, 2, 3]
A = np.array(a, ndmin=1)  # 一维
AA = np.array(a, ndmin=2) # 二维

print(A)  # [1 2 3]
print(AA) # [[1 2 3]]
```



### 2、属性

*NumPy* **数组的维度（又称维数）称为秩（*rank*），秩就是轴的数量，即数组的维度，**一维数组的秩为 1，二维数组的秩为 2，以此类推。

*NumPy* 中，每一个线性的数组称为是一个轴（*axis*）。

比如说，二维数组相当于是两个一维数组，其中第一个一维数组中每个元素又是一个一维数组。所以一维数组就是NumPy中的轴（axes），第一个轴相当于是底层数组，第二个轴是底层数组里的数组。而轴的数量——秩，就是数组的维数。

可以声明 axis。**axis=0，表示沿着第 0 轴进行操作，即对每一列进行操作；axis=1，表示沿着第1轴进行操作，即对每一行进行操作。**

参考：https://www.runoob.com/numpy/numpy-array-attributes.html

| 属性             | 说明                                                         |
| :--------------- | :----------------------------------------------------------- |
| ndarray.ndim     | 秩，即轴的数量或维度的数量                                   |
| ndarray.shape    | 数组的维度，对于矩阵，n 行 m 列                              |
| ndarray.size     | 数组元素的总个数，相当于 .shape 中 n*m 的值                  |
| ndarray.dtype    | ndarray 对象的元素类型                                       |
| ndarray.itemsize | ndarray 对象中每个元素的大小，以字节为单位                   |
| ndarray.flags    | ndarray 对象的内存信息                                       |
| ndarray.real     | ndarray 元素的实部（复数的实部）                             |
| ndarray.imag     | ndarray 元素的虚部（复数的虚部）                             |
| ndarray.data     | 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。 |



以下实例均以该A、B为基础演示。

```python
import numpy as np

a = [1, 2, 3]   # 列表a
A = np.array(a) # 列表a转为一维数组
print(A)        # [1 2 3]  数组输出为数组(元素以' '隔开)

b = [[1, 2, 3], [4, 5, 6]]  # 嵌套列表b
B = np.array(b)  # 嵌套列表b转为二维数组
print(B)  # [[1 2 3]
          #  [4 5 6]]
```

- **ndim实例**

返回数组的维度（秩）。

```python
# ndim查看数组维度
print(A.ndim)  # 1
print(B.ndim)  # 2

a = np.arange(24)
print(a) # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23]
print(a.ndim) # 1

# 现在调整其大小
# reshape的使用查看shape实例
b = a.reshape(2, 4, 3)
print(b)
# [[[ 0  1  2]
#   [ 3  4  5]
#   [ 6  7  8]
#   [ 9 10 11]]
# 
#  [[12 13 14]
#   [15 16 17]
#   [18 19 20]
#   [21 22 23]]]
print(b.ndim) # 3
```



- **shape实例**

返回一个包含数组维度的元组，对于矩阵，n 行 m 列，它也可以用于调整数组维度。

*NumPy* 也提供了`reshape()` 函数来调整数组维度。只是 `reshape()` 返回调整维度后的副本，而不改变原 *ndarray*。

```python
# shape查看数组形状（行，列），前行后列
print(A.shape) # (3,) 一维数组(列,)
print(B.shape) # (2, 3)
# B.shape = (3, 2)  # 改变了B
# print(B) # [[1 2] [3 4] [5 6]]
# NumPy 也提供了reshape() 函数来调整数组维度。只是 reshape() 返回调整维度后的副本，而不改变原 ndarray。
C = B.reshape(3, 2) # 拷贝B生成副本再进行处理生成C
print(C) # [[1 2] [3 4] [5 6]]
print(B) # B 没变 [[1 2 3] [4 5 6]]
```

- **size实例**

```python
# size查看数组元素个数
print(A.size)  # 3
print(B.size)  # 6
```

- **dtype实例**

```python
# dtype查看数组元素类型
print(A.dtype) # dtype('int32')
print(B.dtype) # dtype('int32')
```

- **itemsize实例**

ndarray.itemsize 以字节的形式返回数组中每一个元素的大小。

例如，一个元素类型为 float64 的数组 itemsize 属性值为 8(float64 占用 64 个 bits，每个字节长度为 8，所以 64/8，占用 8 个字节），又如，一个元素类型为 complex32 的数组 item 属性为 4（32/8）。

```python
# itemsize查看数组中每个元素的大小，以字节为单位
print(A.itemsize) # 4  # 1个int为4个字节
print(B.itemsize) # 4  # 1个int为4个字节
```

- **flags实例**

查看数组的内存信息：属性及其描述如下表

| 属性            | 描述                                                         |
| :-------------- | :----------------------------------------------------------- |
| C_CONTIGUOUS    | 数据是在一个单一的C风格的连续段中                            |
| F_CONTIGUOUS    | 数据是在一个单一的Fortran风格的连续段中                      |
| OWNDATA         | 数组拥有它所使用的内存或从另一个对象中借用它                 |
| WRITEABLE       | 数据区域可以被写入，将该值设置为 False，则数据为只读         |
| ALIGNED         | 数据和所有元素都适当地对齐到硬件上                           |
| WRITEBACKIFCOPY | UPDATEIFCOPY 已弃用，由 WRITEBACKIFCOPY 取代;                |
| UPDATEIFCOPY    | 这个数组是其它数组的一个副本，当这个数组被释放时，原数组的内容将被更新 |

```python
# flags查看数组的内存信息
print(A.flags) # C_CONTIGUOUS : True
               # F_CONTIGUOUS : True
               # OWNDATA : True
               # WRITEABLE : True
               # ALIGNED : True
               # WRITEBACKIFCOPY : False
               # UPDATEIFCOPY : False
print(B.flags) # C_CONTIGUOUS : True
               # F_CONTIGUOUS : False
               # OWNDATA : True
               # WRITEABLE : True
               # ALIGNED : True
               # WRITEBACKIFCOPY : False
               # UPDATEIFCOPY : False
```



- **real实例**

```python
# real查看数组元素的实部（复数的实部）
print(A.real) # [1 2 3]
print(B.real) # [[1 2 3]
              #  [4 5 6]]
```

- **imag实例**

```python
# imag查看数组元素的虚部（复数的虚部）
print(A.imag) # [0 0 0]
print(B.imag) # [[0 0 0]
              #  [0 0 0]]
```

- **data实例**

```python
# data包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。
print(A.data) # <memory at 0x000002382577E880>
print(B.data) # <memory at 0x000002381CC0E2B0>
# 通过索引获取数组中元素，数组索引方式同列表索引方式
print(A[1])    # 2 一维数组
print(B[1][1]) # 5
```

## 2 数据类型

*NumPy* 支持比 *Python* 更多种类的数值类型，下表所列的数据类型都是 *NumPy* 内置的数据类型，为了区别于 *Python* 原生的数据类型，`bool`、`int`、`float`、`complex`、`str` 等类型名称末尾都加了 `_`。

> `print(numpy.dtype)` 所显示的都是 *NumPy* 中的数据类型，而非 *Python*原生数据类型。
>
> numpy 的数值类型实际上是 dtype 对象的实例，并对应唯一的字符，包括 np.bool_，np.int32，np.float32，等等。
>
> - **float64三种写法:** dtype=np.float64、dtype=np.float_、dtype=float
>
> - **float错误写法**：dtype=np.float(不是64，不存在该写法)、dtype=float16、dtype=float32···(除了64 其他都要加np.)
>
> - **int32 三种写法：**dtype=np.int32、dtype=np.int_、dtype = int
>
> - **int错误的写法：**dtype=np.int(不是32，不存在该写法)、dtype=int0、dtype=int8···(除了32 其他都要加np.)



| 数据类型   | 描述                                                         |
| :--------- | :----------------------------------------------------------- |
| bool_      | 布尔型数据类型（True 或者 False）                            |
| int_       | 默认的整数类型（类似于 C 语言中的 long，int32 或 int64）     |
| intc       | 与 C 的 int 类型一样，一般是 int32 或 int 64                 |
| intp       | 用于索引的整数类型（类似于 C 的 ssize_t，一般情况下仍然是 int32 或 int64） |
| int8       | 字节（-128 to 127）                                          |
| int16      | 整数（-32768 to 32767）                                      |
| int32      | 整数（-2147483648 to 2147483647）                            |
| int64      | 整数（-9223372036854775808 to 9223372036854775807）          |
| uint8      | 无符号整数（0 to 255）                                       |
| uint16     | 无符号整数（0 to 65535）                                     |
| uint32     | 无符号整数（0 to 4294967295）                                |
| uint64     | 无符号整数（0 to 18446744073709551615）                      |
| float_     | float64 类型的简写                                           |
| float16    | 半精度浮点数，包括：1 个符号位，5 个指数位，10 个尾数位      |
| float32    | 单精度浮点数，包括：1 个符号位，8 个指数位，23 个尾数位      |
| float64    | 双精度浮点数，包括：1 个符号位，11 个指数位，52 个尾数位     |
| complex_   | complex128 类型的简写，即 128 位复数                         |
| complex64  | 复数，表示双 32 位浮点数（实数部分和虚数部分）               |
| complex128 | 复数，表示双 64 位浮点数（实数部分和虚数部分）               |

**归类**

| 类型名称                                                     | 描述                                                     |
| :----------------------------------------------------------- | :------------------------------------------------------- |
| bool_                                                        | 布尔类型                                                 |
| unicode_ / unicode / str_ / str0（零非字母O）                | Unicode 字符串                                           |
| int8 / byte                                                  | 字节（-128 to 127）                                      |
| int16 / short                                                | 整数（-32768 to 32767）                                  |
| int32 / intc / int_ / long                                   | 整数（-2147483648 to 2147483647）                        |
| int64 / longlong / intp / int0（零非字母O）                  | 整数（-9223372036854775808 to 9223372036854775807）      |
| uint8 / ubyte                                                | 无符号整数（0 to 255）                                   |
| uint16 / ushort                                              | 无符号整数（0 to 65535）                                 |
| uint32 / uintc                                               | 无符号整数（0 to 4294967295）                            |
| uint64 / ulonglong / uintp / uint0（零非字母O）              | 无符号整数（0 to 18446744073709551615）                  |
| float16 / half                                               | 半精度浮点数，包括：1 个符号位，5 个指数位，10 个尾数位  |
| float32 / single                                             | 单精度浮点数，包括：1 个符号位，8 个指数位，23 个尾数位  |
| float64 / float_ / double                                    | 双精度浮点数，包括：1 个符号位，11 个指数位，52 个尾数位 |
| complex64 / singlecomplex                                    | 复数，表示双 32 位浮点数（实数部分和虚数部分）           |
| complex128 / complex_ / cfloat / cdouble / longcomplex / clongfloat / clongdouble | 复数，表示双 64 位浮点数（实数部分和虚数部分）           |
| datetime64                                                   | NumPy 1.7 开始支持的日期时间类型                         |
| timedelta64                                                  | 表示两个时间之间的间隔                                   |

### 1、数据类型对象dtype

数据类型对象（numpy.dtype 类的实例）用来描述与数组对应的内存区域是如何使用，它描述了数据的以下几个方面：

- 数据的类型（整数，浮点数或者 Python 对象）
- 数据的大小（例如， 整数使用多少个字节存储）
- 数据的字节顺序（小端法"<"或大端法">"，大端法高字节在前低字节在后，小端法低字节在前高字节在后）
- 在结构化类型的情况下，字段的名称、每个字段的数据类型和每个字段所取的内存块的部分
- 如果数据类型是子数组，它的形状和数据类型字节顺序是通过对数据类型预先设定"<"或">"来决定的。

字节顺序是通过对数据类型预先设定 **<** 或 **>** 来决定的。 **<** 意味着小端法(最小值存储在最小的地址，即低位组放在最前面)。**>** 意味着大端法(最重要的字节存储在最小的地址，即高位组放在最前面)。

**字符串替换数据类型**

> int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替。
>
> 字节顺序标注'<i4' == int32

**复数的概念**

> 我们把形如 z=a+bi（a, b均为实数）的数称为复数，其中 a 称为实部，b 称为虚部，i 称为虚数单位。
> 当虚部 b=0 时，复数 z 是实数；
> 当虚部 b!=0 时，复数 z 是虚数；
> 当虚部 b!=0，且实部 a=0 时，复数 z 是纯虚数。

#### 实例化dtype对象

**dtype 对象构造语法：**

```
numpy.dtype(object, align, copy)
```

- object - 要转换为的数据类型对象
- align - 如果为 true，填充字段使其类似 C 的结构体。
- copy - 复制 dtype 对象 ，如果为 false，则是对内置数据类型对象的引用

**实例1**

输出结果为`int32`的三种方式：

```python
import numpy as np
# 使用标量类型
dt = np.dtype(np.int32)
print(dt)
# int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替（见字符代码）
dt = np.dtype('i4')
print(dt)
# 字节顺序标注
dt = np.dtype('<i4')
print(dt)
```

**实例2**

展示结构化数据类型的使用，类型字段和对应的实际类型将被创建。

```python
import numpy as np

# 首先创建结构化数据类型
dt = np.dtype([('age',np.int8)]) 
print(dt) # [('age', 'i1')]

# 将数据类型应用于 ndarray 对象
dt = np.dtype([('age',np.int8)]) 
a = np.array([(10,),(20,),(30,)], dtype = dt) 
print(a) # [(10,) (20,) (30,)]

# 类型字段名可以用于存取实际的 age 列
dt = np.dtype([('age',np.int8)]) 
a = np.array([(10,),(20,),(30,)], dtype = dt) 
print(a['age'])  # [10 20 30]
```



**实例3**

定义一个结构化数据类型 student，包含字符串字段 name，整数字段 age，及浮点字段 marks，并将这个 dtype 应用到 ndarray 对象。

```python
import numpy as np

student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')]) 
print(student) # [('name', 'S20'), ('age', 'i1'), ('marks', 'f4')]

student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')]) 
a = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype = student) 
print(a)  # [('abc', 21, 50.0), ('xyz', 18, 75.0)]
```

### 2、字符代码

| 字符代码     | 对应类型                                                     |
| :----------- | :----------------------------------------------------------- |
| b            | 布尔型                                                       |
| i            | 有符号整型，'i1', 'i2', 'i4', 'i8' 对应 int8, int16, int32, int64 |
| u            | 无符号整型，'u1', 'u2', 'u4', 'u8' 对应 uint8, uint16, uint32, uint64 |
| f            | 浮点型，'f2', 'f4', 'f8' 对应 float16, float32, float64      |
| c            | 复数，'c8', 'c16' 对应 complex64, complex128                 |
| m            | timedelta64（时间间隔），本质上是个 int64                    |
| M（大写）    | datetime64（日期时间）                                       |
| O（大写）    | Python 对象                                                  |
| S（大写）/ a | (byte-)字符串，只能包含 ASCII 码字符，S 或 a 后带数字表示字符串长度，超出部分将被截断，例如 S20、a10 |
| U（大写）    | Unicode 字符串，U 后带数字表示字符串长度，超出部分将被截断，例如 U20 |
| V（大写）    | bytes 数组，V 后带数字表示数组长度，超出部分将被截断，不足则补零 |

这里主要讲下 M 和 V 的使用，其他都比较简单好理解，可以看上面的例子。

**字符代码 M 的使用示例：**

```python
import numpy as np

# 这里必须写成 M8[单位]，不加单位报异常：Cannot cast NumPy timedelta64 scalar from metadata [D] to according to the rule 'same_kind'。
student = np.dtype([('name', 'S4'), ('age', 'M8[D]')])
print(student) # [('name', 'S4'), ('age', '<M8[D]')]

a = np.array([('tom', '2011-01-01'), ('Jerry', np.datetime64('2012-05-17'))], dtype=student)
print(a) # [(b'tom', '2011-01-01') (b'Jerr', '2012-05-17')]
print(a['age'].dtype) # datetime64[D]
```



**字符代码 V 的使用示例：**

```python
import numpy as np

student = np.dtype([('name', 'V8'), ('age', 'i1')])
print(student) # [('name', 'V8'), ('age', 'i1')]

a = np.array([(b'tom', 21), (b'Jerry', 18)], dtype=student)
print(a)
# [(b'\x74\x6F\x6D\x00\x00\x00\x00\x00', 21)
#  (b'\x4A\x65\x72\x72\x79\x00\x00\x00', 18)]
print(a['name'].dtype) # |V8
```

### 3、datetime64 的使用

#### 1 简单示例

```python
import numpy as np

a = np.datetime64('2019-03-01')
print(a) # 2019-03-01
# 可以仅显示到“月
b = np.datetime64('2019-03')
print(b) # 2019-03
```



#### 2 单位使用

*datetime64* 可以指定使用的单位，单位包括年（'Y'），月（'M'），周（'W'）和天（'D'），而时间单位是小时（'h'），分钟（'m'） ），秒（'s'），毫秒（'ms'），微秒（'us'），纳秒（'ns'），皮秒（'ps'），飞秒（'fs'），阿托秒（'as'）。

周（'W'）是一个比较奇怪的单位，如果是周四，则显示当前，如果不是，则显示上一个周四。后来我想，**大概是因为 1970-01-01 是周四**。

```python
import numpy as np

a = np.datetime64('2019-03-07', 'W')
b = np.datetime64('2019-03-08', 'W')
# （2019-03-07 是周四）
print(a, b) # 2019-03-07 2019-03-07
```



从字符串创建 *datetime64* 类型时，默认情况下，*NumPy* 会根据字符串自动选择对应的单位。

```python
import numpy as np

a = np.datetime64('2019-03-08 20:00')
print(a.dtype) # datetime64[m]
```



也可以强制指定使用的单位。

```python
import numpy as np

a = np.datetime64('2019-03', 'D')
print(a) # 2019-03-01
```



由上例可以看出，`2019-03` 和 `2019-03-01` 所表示的其实是同一个时间。
事实上，如果两个 *datetime64* 对象具有不同的单位，它们可能仍然代表相同的时刻。并且从较大的单位（如月份）转换为较小的单位（如天数）是安全的。

```python
import numpy as np

print(np.datetime64('2019-03') == np.datetime64('2019-03-01')) # True
```



从字符串创建日期时间数组时，如果单位不统一，则一律转化成其中最小的单位。

```python
import numpy as np

a = np.array(['2019-03', '2019-03-08', '2019-03-08 20:00'], dtype='datetime64')
print(a) # ['2019-03-01T00:00' '2019-03-08T00:00' '2019-03-08T20:00']
print(a.dtype) # datetime64[m]
```



#### 3 配合 arange 函数使用

一个月的所有天数

```python
import numpy as np

a = np.arange('2019-02', '2019-03', dtype='datetime64[D]')
print(a)
"""
['2019-02-01' '2019-02-02' '2019-02-03' '2019-02-04' '2019-02-05'
 '2019-02-06' '2019-02-07' '2019-02-08' '2019-02-09' '2019-02-10'
 '2019-02-11' '2019-02-12' '2019-02-13' '2019-02-14' '2019-02-15'
 '2019-02-16' '2019-02-17' '2019-02-18' '2019-02-19' '2019-02-20'
 '2019-02-21' '2019-02-22' '2019-02-23' '2019-02-24' '2019-02-25'
 '2019-02-26' '2019-02-27' '2019-02-28']
"""
```



间隔也可以是 3 天（'3D'）这种形式哦。

```python
import numpy as np

a = np.arange('2019-02', '2019-03', dtype='datetime64[3D]')
print(a)
""" 发现没有，这里少了 2019-02-28。我认为是个 BUG，没道理去掉的。
['2019-02-01' '2019-02-04' '2019-02-07' '2019-02-10' '2019-02-13'
 '2019-02-16' '2019-02-19' '2019-02-22' '2019-02-25']
"""
```



#### 4 Datetime64 和 Timedelta64 运算

*timedelta64* 表示两个 *Datetime64* 之间的差。*timedelta64* 也是带单位的，并且和相减运算中的两个 *Datetime64* 中的较小的单位保持一致。

```python
import numpy as np

a = np.datetime64('2019-03-08') - np.datetime64('2019-03-07')
b = np.datetime64('2019-03-08') - np.datetime64('2019-03-07 08:00')
c = np.datetime64('2019-03-08') - np.datetime64('2019-03-07 23:00', 'D')

# 看c的表达式，因为强制限定了单位，所以np.datetime64('2019-03-07 23:00', 'D')所表示的时间其实是 `2019-03-07`，那么结果是 1 也就好理解了。
print(a, a.dtype) # 1 days timedelta64[D]
print(b, b.dtype) # 960 minutes timedelta64[m]
print(c, c.dtype) # 1 days timedelta64[D]


d = np.datetime64('2019-03') + np.timedelta64(20, 'D')
print(d) # 2019-03-21
```

#### 5 Timedelta64 单独的运算

生成 *Timedelta64*

```python
import numpy as np

a = np.timedelta64(1, 'Y')    # 方式一
b = np.timedelta64(a, 'M')    # 方式二
print(a) # 1 years
print(b) # 12 months
```

加减乘除

```python
import numpy as np

a = np.timedelta64(1, 'Y')
b = np.timedelta64(6, 'M')

print(a + b) # 18 months
print(a - b) # 6 months
print(2 * a) # 2 years
print(a / b) # 2.0

# 但是，年（'Y'）和月（'M'）这两个单位是经过特殊处理的，它们无法和其他单位进行运算，一年有几天？一个月有几个小时？这些都是不确定的。
a = np.timedelta64(1, 'M')
b = np.timedelta64(a, 'D')
# TypeError: Cannot cast NumPy timedelta64 scalar from metadata [M] to [D] according to the rule 'same_kind'
```



#### 6 numpy.datetime64 与 datetime.datetime 相互转换

```python
import numpy as np
import datetime

dt = datetime.datetime(2018, 9, 1)
dt64 = np.datetime64(dt, 'D')
print(dt64, dt64.dtype) # 2018-09-01 datetime64[D]

dt2 = dt64.astype(datetime.datetime)
print(dt2) # 2018-09-01
```

#### 7 工作日功能（busday）

*busday* 默认周一至周五是工作日。该实现基于一个 *weekmask*，包含 7 个布尔标志，用于工作日。

##### 1 busday_offset

busday_offset 将指定的偏移量应用于工作日，单位天（'D'）。例如计算下一个工作日：

```python
import numpy as np

a = np.busday_offset('2019-03-08', 1)
print(a) # 2019-03-11
```



如果当前日期为非工作日，则默认是报错的。

```python
import numpy as np

a = np.busday_offset('2019-03-09', 1)
print(a) # ValueError: Non-business day date in busday_offset
```



可以指定 *forward* 或 *backward* 规则来避免报错。

```python
import numpy as np

a = np.busday_offset('2019-03-09', 1, roll='forward')
b = np.busday_offset('2019-03-09', 1, roll='backward')
print(a) # 2019-03-12
print(b) # 2019-03-11

c = np.busday_offset('2019-03-09', 0, roll='forward')
d = np.busday_offset('2019-03-09', 0, roll='backward')
print(c) # 2019-03-11
print(d) # 2019-03-08
```

可以指定偏移量为 0 来获取当前日期向前或向后最近的工作日，当然，如果当前日期本身就是工作日，则直接返回当前日期。

```python
import numpy as np

a = np.busday_offset('2019-05', 1, roll='forward', weekmask='Sun')
print(a) # 2019-05-12
```



母亲节是 5 月的第二个星期日，本例就可以用于返回母亲节具体的日期。来解释一下：`weekmask` 参数在这里可以传星期的英文简写（注意是简写 Mon、Tue、Wed、Thu、Fri、Sat、Sun，全拼报错的），指定向前或向后到星期几。上面代码的含义就是：前进道 2019-05-01 后的第二个（不要忘了下标从 0 开始的）星期日。

> 这个功能对老美来说也许有用，但是在中国，谁来给我求个端午节是几月几号？

##### 2 is_busday

is_busday返回指定日期是否是工作日。

```python
import numpy as np

a = np.is_busday(np.datetime64('2019-03-08'))
b = np.is_busday('2019-03-09')
print(a) # True
print(b) # False
```

##### 3 busday_count

busday_count返回两个日期之间的工作日数量。

```python
import numpy as np

a = np.busday_count(np.datetime64('2019-03-01'), np.datetime64('2019-03-10'))
b = np.busday_count('2019-03-10', '2019-03-01')
print(a) # 6
print(b) # -6
```

##### 4 count_nonzero

count_nonzero统计一个 datetime64['D'] 数组中的工作日天数。

```python
import numpy as np

c = np.arange('2019-03-01', '2019-03-10', dtype='datetime64')
d = np.count_nonzero(np.is_busday(c))
print(d) # 6
```



自定义周掩码值，即指定一周中哪些星期是工作日。

```python
import numpy as np

a = np.is_busday('2019-03-08', weekmask=[1, 1, 1, 1, 0, 1, 0])
b = np.is_busday('2019-03-09', weekmask='1111010')
print(a) # False
print(b) # True
```

周掩码值还可以直接用星期单词缩写列出所有的工作日，下面所示的周掩码表示的工作日是：周一周二周三周四周六周日，周五为休息日。

```ini
weekmask='Mon Tue Wed Thu Sat Sun'
```



#### 8 numpy.datetime_data

**语法：**

```scss
numpy.datetime_data(dtype, /)
```

**参数：**只能是 *datetime64* 或 *timedelta64* 类型
**返回值：**返回一个元组 ('单位', 步长)

**例一：**

```python
import numpy as np

dt_25s = np.dtype('timedelta64[25s]')
print(np.datetime_data(dt_25s))
```

**输出：**

```bash
('s', 25)
```

**例二：**

```python
import numpy as np

dt_25s = np.dtype('timedelta64[25s]')
b = np.array([1, 2, 3, 4, 5], dt_25s).astype('timedelta64[s]')
print(b)
print(b.dtype)
```

**输出：**

```css
[ 25  50  75 100 125]
timedelta64[s]
```

本例中，`b` 是一个 *narray*，数据类型从 `timedelta64[25s]` 转成了 `timedelta64[s]`，所以数组中每个数都要乘以 25。

#### 9 numpy.datetime_as_string

将日期时间数组转换为字符串数组。

**语法：**

```python
numpy.datetime_as_string(arr, unit=None, timezone='naive', casting='same_kind')
```

| 参数     | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| arr      | datetimes64 数组                                             |
| unit     | 'auto' 或者 datetime64 单位。                                |
| timezone | 时区                                                         |
| casting  | 在日期时间单位之间进行更改时允许进行转换。有以下可选值：'no', 'equiv', 'safe', 'same_kind', 'unsafe'。 |

**例一：**

```python
import numpy as np

dt_array = np.arange('2019-03-01', '2019-03-10', dtype='datetime64[D]')
str_array = np.datetime_as_string(dt_array)

print(str_array)
print(str_array.dtype)
```

**输出：**

```bash
['2019-03-01' '2019-03-02' '2019-03-03' '2019-03-04' '2019-03-05'
 '2019-03-06' '2019-03-07' '2019-03-08' '2019-03-09']
<U28
```

**例二：**unit的使用示例
默认情况下，`unit=None`，如果数组中的 datetime64 元素单位不一致，则会统一转化为其中最小的单位形式输出，如果 `unit='auto'` 则会保持原样输出。当然，如果指定了单位，则按指定的单位格式输出。

```python
import numpy as np

dt_array = np.array(['2019-03', '2019-03-08', '2019-03-08 20:00'], dtype='datetime64')

str_array1 = np.datetime_as_string(dt_array)
str_array2 = np.datetime_as_string(dt_array, unit='auto')
str_array3 = np.datetime_as_string(dt_array, unit='D')
print(str_array1)
print(str_array2)
print(str_array3)
```

**输出：**

```bash
['2019-03-01T00:00' '2019-03-08T00:00' '2019-03-08T20:00']
['2019-03-01' '2019-03-08' '2019-03-08T20:00']
['2019-03-01' '2019-03-08' '2019-03-08']
```



## 3 常数

参考：https://www.cnblogs.com/gl1573/p/10531421.html

- 正无穷：Inf = inf = infty = Infinity = PINF
- 负无穷：NINF
- 正零：PZERO
- 负零：NZERO
- 非数值：nan = NaN = NAN
- 自然数e：e
- π：pi
- 伽马：euler_gamma
- None 的别名：newaxis

**示例：**

```python
print(np.inf)
print(np.NINF)
print(np.PZERO)
print(np.NZERO)
print(np.nan)
print(np.e)
print(np.pi)
print(np.euler_gamma)
print(np.newaxis)
```

**输出：**

```python
inf
-inf
0.0
-0.0
nan
2.718281828459045
3.141592653589793
0.5772156649015329
None
```



## 4 创建数组

参考：https://www.runoob.com/numpy/numpy-array-creation.html

ndarray 数组除了可以使用底层 ndarray 构造器来创建外，也可以通过以下几种方式来创建。

### 1、未初始化数组

#### numpy.empty

此方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组：

```python
numpy.empty(shape, dtype = float, order = 'C')
```

| 参数  | 描述                                                         |
| :---- | :----------------------------------------------------------- |
| shape | 数组形状                                                     |
| dtype | 数据类型，可选                                               |
| order | 有"C（行优先）"和"F（列优先）"两个选项，在计算机内存中的存储元素的顺序。默认 'C' |

**注意**： **因为未初始化，数组元素为随机值**。`empty()` 方法和 `zeros()` 方法不同，不会将数组值设置为零，因此可能会略微加快。另一方面，它**要求用户手动设置数组中的所有值**，并应谨慎使用。

```python
import numpy as np 
x = np.empty([3,2], dtype = int) 
print(x)
```

输出结果为：

```python
[[ 6917529027641081856  5764616291768666155]
 [ 6917529027641081859 -5764598754299804209]
 [          4497473538      844429428932120]]
```



### 2、以0填充的数组

#### numpy.zeros

创建指定大小的数组，数组元素以 0 来填充：

```
numpy.zeros(shape, dtype = float, order = 'C')
```

参数说明：

| 参数  | 描述                                                         |
| :---- | :----------------------------------------------------------- |
| shape | 数组形状，二维以上需要用元组(行，列)或者字典[行，列]，且输入参数为整数 |
| dtype | 数据类型，可选，默认numpy.float64                            |
| order | 是否在存储器中以C或Fortran连续（按行或列方式）存储多维数据；'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组。 |

```python
import numpy as np

# 默认为浮点数
x = np.zeros(5) # 一维
# 或者
# x = np.zeros((5,))
print(x)

# 设置类型为整数
y = np.zeros((5,), dtype=np.int32)
print(y)

# 自定义类型
z = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')])
# 或者
# z = np.zeros([2, 2], dtype=[('x', 'i4'), ('y', 'i4')])
print(z)
```

输出结果为：

```python
[0. 0. 0. 0. 0.]
[0 0 0 0 0]
[[(0, 0) (0, 0)]
 [(0, 0) (0, 0)]]
```

### 3、以1填充的数组

#### numpy.ones

创建指定形状的数组，数组元素以 1 来填充：

```
numpy.ones(shape, dtype = None, order = 'C')
```

参数说明：

| 参数  | 描述                                                |
| :---- | :-------------------------------------------------- |
| shape | 数组形状，元组(行，列)或者字典[行，列]              |
| dtype | 数据类型，可选                                      |
| order | 'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组 |

```python
import numpy as np
 
# 默认为浮点数
x = np.ones(5)
# 或者
# x = np.ones((5,))
print(x)

# 自定义类型
x = np.ones((2, 2), dtype=int)
# 或者
# x = np.ones([2, 2], dtype=int)
print(x)
```

输出结果为：

```python
[1. 1. 1. 1. 1.]
[[1 1]
 [1 1]]
```

### 4、给定填充值的数组

#### numpy.full

返回给定维度和类型的新数组，填充 fill_value。

```python
numpy.full(shape, fill_value, dtype=None, order='C')
```

| 参数       | 描述                                                         |
| :--------- | :----------------------------------------------------------- |
| shape      | 返回数组的维度                                               |
| fill_value | 填充值                                                       |
| dtype      | 返回数组的数据类型，默认值 None 指：`np.array(fill_value).dtype`，即填充值的数据类型。 |
| order      | 在计算机内存中的存储元素的顺序，只支持 'C'（按行）、'F'（按列），默认 'C' |

**示例：**

```python
import numpy as np

a = np.full((2, 3), 9)
print(a)
print(np.array(9).dtype)
```

**输出：**

```json
[[9 9 9]
 [9 9 9]]
int32
```



### 5、创建N*N数组

#### numpy.eye()

创建一个正方的N*N的单位矩阵，对角线值为1，其余为0

```
eye(n)
```

```python
import numpy as np

a = np.eye(5)
print(a)

[[ 1.  0.  0.  0.  0.]
 [ 0.  1.  0.  0.  0.]
 [ 0.  0.  1.  0.  0.]
 [ 0.  0.  0.  1.  0.]
 [ 0.  0.  0.  0.  1.]]
```



### 6、从数值范围创建数组

#### 1 numpy.arange

该函数等效于 *Python* 内置 `range` 函数，在给定间隔内返回均匀间隔的值，但返回的是 *ndarray* 而不是列表。

```python
# 固定步长 等差
arange([start,] stop[, step,], dtype=None)  
```

> [ ] 括起来的表示可选参数。

| 参数  | 描述                                                         |
| :---- | :----------------------------------------------------------- |
| start | 起始值，默认为 0                                             |
| stop  | 终止值（不包含）                                             |
| step  | 步长，默认为1                                                |
| dtype | 创建的 ndarray 的数据类型，如果没有提供，则会使用输入数据的类型。 |

**示例：**

```python
import numpy as np

a = np.arange(5)
b = np.arange(10, 20, 2)
print(a) # [0 1 2 3 4]
print(b) # [10 12 14 16 18]
```



#### 2 numpy.linspace

返回在间隔[开始，停止]上计算的num个均匀间隔的样本。

`linspace`创建一个一维等差数列的数组，与 `arange` 函数不同，`arange` 是固定步长，而 `linspace` 则是固定元素数量。

```python
# 固定元素数量 等差
linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
```

| 参数     | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| start    | 序列的起始值                                                 |
| stop     | 序列的终止值，如果 endpoint 为 True，则该值包含于数列中      |
| num      | 要生成的等步长的样本数量，默认为 50                          |
| endpoint | 数列取值范围中包含 stop 值，默认为 True包含，反之False不包含。 |
| retstep  | 生成的数组中是否显示步长(间距)，默认为False显示，反之True不显示。 |
| dtype    | ndarray 的数据类型                                           |

**例一：endpoint 参数的用法**
 `endpoint=True`取值包含终止值stop，`endpoint=False` 取值去掉终止值，endpoint默认为True。

```python
import numpy as np

# endpoint的使用：endpoint默认为True，取值范围含stop，若为False，则取值范围不含stop。
a = np.linspace(0, 5, 4, endpoint=False) # 不含4
b = np.linspace(0, 5, 4, endpoint=True) # 含4
c = np.linspace(0, 5, 4) # 含4
print(a) # [0.   1.25 2.5  3.75]
print(b) # [0.         1.66666667 3.33333333 5.        ]
print(c) # [0.         1.66666667 3.33333333 5.        ]
```



**例二：retstep 参数的用法**
返回一个元组，第一个元素是 *numpy.ndarray*，第二个元素是步长(间距)。

```python
import numpy as np

# retstep的使用：retstep默认为False，生成的数组中不会显示间距，若为True，则生成的数组中会显示间距。
aa = np.linspace(0, 10, 5)
bb = np.linspace(0, 10, 5, retstep=True)
cc = np.linspace(0, 10, 5, retstep=False)
print(aa) # [ 0.   2.5  5.   7.5 10. ]
print(bb) # (array([ 0. ,  2.5,  5. ,  7.5, 10. ]), 2.5)
print(cc) # [ 0.   2.5  5.   7.5 10. ]
```



**例三：dtype 参数**
*dtype* 参数指定后会将结果强制转换成 *dtype* 指定的类型，如果是 float 转 int，最终值就可能不是等差的了。

```python
import numpy as np

a = np.linspace(0, 10, 5, dtype=int)
print(a) # [ 0  2  5  7 10]
```



#### 3 numpy.logspace

`logspace` 函数用于创建一个等比数列。

```sql
# 等比
logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
```

| 参数     | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| start    | 序列的起始值为：`base ** start` （幂运算）                   |
| stop     | 序列的终止值为：`base ** stop`。若 endpoint 为 True，含于数列中 |
| num      | 要生成的等步长的样本数量，默认为50                           |
| endpoint | 该值为 Ture 时，数列中中包含 stop 值，反之不包含，默认是 True。 |
| base     | 对数 log 的底数。                                            |
| dtype    | ndarray 的数据类型                                           |

**示例：**
主要是注意 start 参数的值并非是真正的起始值。

```python
import numpy as np

a = np.logspace(1, 4, num=4)
print(a)
```

**输出：**

```json
[   10.   100.  1000. 10000.]
```

#### 4 numpy.geomspace

`geomspace`创建一个一维等比数列。

```sql
numpy.geomspace(start, stop, num=50, endpoint=True, dtype=None, axis=0)
```

| 参数     | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| start    | 序列的起始值                                                 |
| stop     | 序列的终止值，如果 endpoint 为 True，该值包含于数列中        |
| num      | 要生成的样本数量，默认为 50                                  |
| endpoint | 该值为 Ture 时，数列中中包含 stop 值，反之不包含，默认是 True。 |
| dtype    | ndarray 的数据类型                                           |
| axis     | `int`, 可选。结果中的轴用于存储样本。 仅当start或stop类似于数组时才相关。 默认为0，样本将沿着在开始处插入的新轴。 使用`-1`来获得轴的末端。 |

**示例：**

```python
import numpy as np

a = np.geomspace(1, 8, num=4)
b = np.geomspace(1, 8, num=4, axis=0)
c = np.geomspace(1, 8, num=4, axis=1)
print(a) # [1. 2. 4. 8.]
print(b) # [1. 2. 4. 8.]
```

**输出：**

```json
[1. 2. 4. 8.]
```



### 7、从已有数组创建数组

#### 1 numpy.asarray

`numpy.asarray` **类似 `numpy.array`**，但 `numpy.asarray` 的参数只有三个。

```python
numpy.asarray(a, dtype=None, order=None)
```

| 参数  | 描述                                                         |
| :---- | :----------------------------------------------------------- |
| a     | 输入数据，可以转换为数组的任何形式。 这包括列表，元组列表，元组，元组元组，列表元组和 ndarray。 |
| dtype | 数据类型                                                     |
| order | 在计算机内存中的存储元素的顺序，只支持 'C'（按行）、'F'（按列），默认 'C' |

**示例：**

```python
import numpy as np

x = [(1,2,3),(4,5,6)]
a = np.asarray(x)  
print(a) # [[1 2 3]
         #  [4 5 6]]
b = np.array(x)
print(b) # [[1 2 3]
         #  [4 5 6]]
```



#### 2 numpy.frombuffer

`numpy.frombuffer` 用于**实现动态数组**。`numpy.frombuffer` 接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象。

```bash
numpy.frombuffer(buffer, dtype=float, count=-1, offset=0)
```

| 参数   | 描述                                                         |
| :----- | :----------------------------------------------------------- |
| buffer | 需要一个bytes-like object，实现了 `__buffer__` 方法的对象，（绝对不是菜鸟教程上说的任意对象都可以），不可以为`str` |
| dtype  | 返回数组的数据类型                                           |
| count  | 读取的数据数量，默认为 -1，读取所有数据。                    |
| offset | 读取的起始位置，默认为 0。                                   |

**例一：**

```python
import numpy as np

# a = np.frombuffer('Hello World', dtype='S1') # 异常：a bytes-like object is required, not 'str'
# buffer 是字符串的时候，Python3 默认 str 是 Unicode 类型，所以要转成 bytestring 在原 str 前加上 b。
b = np.frombuffer(b'Hello World', dtype='S1')
print(b) # [b'H' b'e' b'l' b'l' b'o' b' ' b'W' b'o' b'r' b'l' b'd']
```

**例二：**
看了上面的例子，似乎对“实现动态数组”没啥感觉，那么我们来看这个例子。

`array.array` 创建的数组对象内存是连续的（这里不能用 list，会报：AttributeError: 'list' object has no attribute '**buffer**'），`numpy.frombuffer` 从 `array.array` 的内存中创建数组，从上例中可以看出，改变 `array.array` 的值，`numpy.frombuffer` 的值也会跟着改变，由此可见。

```python
import numpy as np
import array

a = array.array('i', [1, 2, 3, 4])
print(a) # array('i', [1, 2, 3, 4])
na = np.frombuffer(a, dtype=np.int_)
print(na) # [1 2 3 4]

a[0] = 10
print(a) # array('i', [10, 2, 3, 4])
print(na) # [10, 2, 3, 4]
```



**例三：**
`array.array` 数组中的值改变是可以的，但是如果是添加值，那就不行了。

```python
import numpy as np
import array

# array.array数组中的值改变是可以的，不可以是添加值。
a = array.array("i", [1, 2, 3, 4])
na = np.frombuffer(a, dtype=int)
print(na) # [1 2 3 4]

a.append(5)
print(na) # [-1186710512         656           3           4]
```



#### 3 numpy.fromiter

`numpy.fromiter` 方法**从可迭代对象中建立 ndarray 对象，返回一维数组**。

```php
numpy.fromiter(iterable, dtype, count=-1)
```

| 参数     | 描述                                    |
| :------- | :-------------------------------------- |
| iterable | 可迭代对象                              |
| dtype    | 返回数组的数据类型                      |
| count    | 读取的数据数量，默认为 -1，读取所有数据 |

看起来有点像 `numpy.array`，`array` 方法需要传入的是一个 list，而 `fromiter` 可以传入可迭代对象。

```python
import numpy as np

# 可迭代对象
iterable = (x * x for x in range(5))
# fromiter
a = np.fromiter(iterable, int)
print(a) # [ 0  1  4  9 16]
# 换成 array 试试看。
aa = np.array(iterable)
print(aa) # <generator object <genexpr> at 0x000000001442DD00>
```



#### 4 empty_like

返回一个与给定数组**具有相同维度和类型**的**未初始化的**新数组。

```python
numpy.empty_like(prototype, dtype=None, order='K', subok=True)
```

| 参数      | 描述                                                         |
| :-------- | :----------------------------------------------------------- |
| prototype | 给定的数组                                                   |
| dtype     | 覆盖结果的数据类型，版本1.6.0中的新功能。                    |
| order     | 指定阵列的内存布局。C（按行）、F（按列）、A（原顺序）、K（元素在内存中的出现顺序） |
| subok     | 默认情况下，返回的数组被强制为基类数组。 如果为 True，则返回子类。 |

**示例：**

```python
import numpy as np
a = np.empty_like([[1, 2, 3], [4, 5, 6]])
print(a)
```

**输出：**

```json
[[1 2 3]
 [4 5 6]]
```

#### 5 zeros_like

```python
numpy.zeros_like(a, dtype=None, order='K', subok=True)
```

参数同上。

**示例：**

```python
import numpy as np
a = np.zeros_like([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(a)
```

**输出：**

```json
[[0. 0. 0.]
 [0. 0. 0.]]
```

#### 6 ones_like

```python
numpy.ones_like(a, dtype=None, order='K', subok=True)
```

参数同上。

**示例：**

```python
import numpy as np
a = np.ones_like([[1, 2, 3], [4, 5, 6]])
print(a)
```

**输出：**

```json
[[1 1 1]
 [1 1 1]]
```

#### 7 numpy.full_like

返回与给定数组具有相同维度和类型的并以 fill_value 填充的数组。

```python
numpy.full_like(a, fill_value, dtype=None, order='K', subok=True)
```

| 参数       | 描述                                                         |
| :--------- | :----------------------------------------------------------- |
| a          | 给定的数组                                                   |
| fill_value | 填充值                                                       |
| dtype      | 返回数组的数据类型，默认值 None，则使用给定数组的类型        |
| order      | 指定阵列的内存布局。C（按行）、F（按列）、A（原顺序）、K（元素在内存中的出现顺序） |
| subok      | 默认情况下，返回的数组被强制为基类数组。 如果为 True，则返回子类。 |

zeros_like、ones_like 其实都是此方法的特例。

**示例：**

```python
import numpy as np

x = np.arange(6, dtype=int)
print(x)  # 类型 int32
print('-------------------')
a = np.full_like(x, 1)
b = np.full_like(x, 0.1)  # dtype默认原来的类型 int32
c = np.full_like(x, 0.1, dtype=np.double)

print(a)
print(b)
print(c)
```

**输出：**

```python
[0 1 2 3 4 5]
-------------------
[1 1 1 1 1 1]
[0 0 0 0 0 0]
[0.1 0.1 0.1 0.1 0.1 0.1]
```





## 5 Numpy通用函数

### 1、改变形状

```python
# 数组形状：.T/.reshape()/.resize()
# 注意：.T/.reshape()/.resize()都是生成新的数组！！！
```

#### 1 T方法转置

```python
# .T方法：转置，例如原shape为(3,4)或(2,3,4)，转置结果为(4,3)或(4,3,2) → 所以一维数组转置后结果不变
ar1 = np.arange(10)
ar2 = np.ones((5,2))
print(ar1,'\n',ar1.T)  # 一维数组转置后结果不变
print(ar2,'\n',ar2.T)  # 多维数组转置后结果(5,2)转为(2,5)，行变列，列变行 
"""
[0 1 2 3 4 5 6 7 8 9] 
 [0 1 2 3 4 5 6 7 8 9]
[[ 1.  1.]
 [ 1.  1.]
 [ 1.  1.]
 [ 1.  1.]
 [ 1.  1.]] 
 [[ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]]
"""
```

#### 2 reshape

```python
# numpy.reshape(a, newshape, order='C')：为数组提供新形状，而不更改其数据，所以元素数量需要一致！！
ar3 = ar1.reshape(2,5)     # 用法1：直接将已有数组改变形状             
ar4 = np.zeros((4,6)).reshape(3,8)   # 用法2：生成数组后直接改变形状
ar5 = np.reshape(np.arange(12),(3,4))   # 用法3：参数内添加数组，目标形状
print(ar1,'\n',ar3)
print(ar4)
print(ar5)
"""
[0 1 2 3 4 5 6 7 8 9] 
 [[0 1 2 3 4]
 [5 6 7 8 9]]
[[ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]]
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
"""
```

#### 3 resize

```python
# numpy.resize(a, new_shape)：返回具有指定形状的新数组，如有必要可重复填充所需数量的元素。
ar6 = np.resize(np.arange(5),(3,4))
print(ar6)
"""
[[0 1 2 3]
 [4 0 1 2]
 [3 4 0 1]]
"""
```

### 2、数组的复制

#### 1 赋值

```python
# 回忆python的赋值逻辑：指向内存中生成的一个值 → 这里ar1和ar2指向同一个值，所以ar1改变，ar2一起改变
ar1 = np.arange(10)
ar2 = ar1
print(ar2 is ar1) # True
ar1[2] = 9
print(ar1,ar2) # [0 1 9 3 4 5 6 7 8 9] [0 1 9 3 4 5 6 7 8 9]
```

#### 2 copy

```python
# copy方法生成数组及其数据的完整拷贝
# 再次提醒：.T/.reshape()/.resize()都是生成新的数组！！！
ar3 = ar1.copy()
print(ar3 is ar1) # False
ar1[0] = 9
print(ar1,ar3) # [9 1 9 3 4 5 6 7 8 9] [0 1 9 3 4 5 6 7 8 9]
```

### 3、数组类型转换astype

```python
# 可以在参数位置设置数组类型
ar1 = np.arange(10,dtype=float)
print(ar1, ar1.dtype) # [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9.] float64

# 数组类型转换：.astype()

# a.astype()：转换数组类型
# 注意：养成好习惯，数组类型用np.int32，而不是直接int32
ar2 = ar1.astype(np.int32)
print(ar2,ar2.dtype) # [0 1 2 3 4 5 6 7 8 9] int32
print(ar1,ar1.dtype) # [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9.] float64
```



### 4、数组堆叠

#### 1 hstack水平堆叠

```python
# numpy.hstack(tup)：水平（按行顺序）堆叠数组

a = np.arange(5)    # a为一维数组，5个元素
b = np.arange(5,9) # b为一维数组,4个元素
# 一维数组形状可以不一样！！！
ar1 = np.hstack((a,b))  # 注意:((a,b))，这里形状可以不一样
print(a,a.shape)  # [0 1 2 3 4] (5,)
print(b,b.shape)  # [5 6 7 8] (4,)
print(ar1,ar1.shape)  # [0 1 2 3 4 5 6 7 8] (9,)

# 多维数组形状必须一样！！！
a = np.array([[1],[2],[3]])   # a为二维数组，3行1列
b = np.array([['a'],['b'],['c']])  # b为二维数组，3行1列
ar2 = np.hstack((a,b))  # 注意:((a,b))，这里形状必须一样
print(a,a.shape)
"""
[[1]
 [2]
 [3]] (3, 1)
"""
print(b,b.shape)
"""
[['a']
 ['b']
 ['c']] (3, 1)
"""
print(ar2,ar2.shape)
"""
[['1' 'a']
 ['2' 'b']
 ['3' 'c']] (3, 2)
"""
```

#### 2 vstack垂直堆叠

```python
# numpy.vstack(tup)：垂直（按列顺序）堆叠数组
a = np.arange(5)    
b = np.arange(5,10)
ar1 = np.vstack((a,b))
print(a,a.shape) # [0 1 2 3 4] (5,)
print(b,b.shape) # [5 6 7 8 9] (5,)
print(ar1,ar1.shape)
"""
[[0 1 2 3 4]
 [5 6 7 8 9]] (2, 5)
"""

a = np.array([[1],[2],[3]])   
b = np.array([['a'],['b'],['c'],['d']])   
ar2 = np.vstack((a,b))  # 这里形状可以不一样
print(a,a.shape)
"""
[[1]
 [2]
 [3]] (3, 1)
"""
print(b,b.shape)
"""
[['a']
 ['b']
 ['c']
 ['d']] (4, 1)
"""
print(ar2,ar2.shape)
"""
[['1']
 ['2']
 ['3']
 ['a']
 ['b']
 ['c']
 ['d']] (7, 1)
"""
```

#### 3 stack沿轴连接

```python
# numpy.stack(arrays, axis=0)：沿着新轴连接数组的序列，形状必须一样！
# 重点解释axis参数的意思，假设两个数组[1 2 3]和[4 5 6]，shape均为(3,0)
# axis=0：[[1 2 3] [4 5 6]]，shape为(2,3)
# axis=1：[[1 4] [2 5] [3 6]]，shape为(3,2)
a = np.arange(5)    
b = np.arange(5,10)
ar1 = np.stack((a,b))  # 默认axis为0
ar2 = np.stack((a,b),axis=1)
print(a,a.shape) # [0 1 2 3 4] (5,)
print(b,b.shape) # [5 6 7 8 9] (5,)
print(ar1,ar1.shape)
"""
[[0 1 2 3 4]
 [5 6 7 8 9]] (2, 5)
"""
print(ar2,ar2.shape)
"""
[[0 5]
 [1 6]
 [2 7]
 [3 8]
 [4 9]] (5, 2)
"""
```

### 5、数组拆分

#### 1 hsplit水平拆分

```python
# numpy.hsplit(ary, indices_or_sections)：将数组水平（逐列）拆分为多个子数组 → 按列拆分
# 输出结果为列表，列表中元素为数组
ar = np.arange(16).reshape(4,4)
ar1 = np.hsplit(ar,2)
print(ar)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]]
"""
print(ar1,type(ar1))
"""
[array([[ 0,  1],
       [ 4,  5],
       [ 8,  9],
       [12, 13]]),
 array([[ 2,  3],
       [ 6,  7],
       [10, 11],
       [14, 15]])] <class 'list'>
"""
```

#### 2 vsplit垂直拆分

```python
# numpy.vsplit(ary, indices_or_sections)：:将数组垂直（行方向）拆分为多个子数组 → 按行拆
ar2 = np.vsplit(ar,4)
print(ar)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]]
"""
print(ar2,type(ar2))
"""
[array([[ 0,  1,  2,  3]]), 
 array([[ 4,  5,  6,  7]]),
 array([[ 8,  9, 10, 11]]),
 array([[12, 13, 14, 15]])] <class 'list'>
"""
```



### 6、运算

#### 1 加减乘除幂

```python
# 数组简单运算
ar = np.arange(6).reshape(2,3)
# 加法
print(ar + 10)
"""
[[10 11 12]
 [13 14 15]]
"""
# 乘法
print(ar * 2)
"""
[[ 0  2  4]
 [ 6  8 10]]
"""
# 除法
print(1 / (ar+1)) 
"""
[[ 1.          0.5         0.33333333]
 [ 0.25        0.2         0.16666667]]
"""
# 幂
print(ar ** 0.5)  
"""
[[ 0.          1.          1.41421356]
 [ 1.73205081  2.          2.23606798]]
"""
```

#### 2 标量运算

```python
# 求平均值
print(ar.mean()) # 2.5 
# 求最大值
print(ar.max()) # 5 
# 求最小值
print(ar.min()) # 0
# 求标准差
print(ar.std()) #1.70782512766
# 求方差
print(ar.var())   # 2.91666666667
# 求和 np.sum() → axis为0，按列求和；axis为1，按行求和
print(ar.sum(), np.sum(ar,axis = 0))  # 15 [3 5 7]
# 排序
print(np.sort(np.array([1,4,3,2,5,6])))   # [1 2 3 4 5 6]
```



## 6 Numpy随机数

- numpy.random包含多种概率分布的随机样本，是数据分析辅助的重点工具之一

```python
# 随机数生成

samples = np.random.normal(size=(4,4))
print(samples)
# 生成一个标准正太分布的4*4样本值
[[ 0.17875618 -1.19367146 -1.29127688  1.11541622]
 [ 1.48126355 -0.81119863 -0.94187702 -0.13203948]
 [ 0.11418808 -2.34415548  0.17391121  1.4822019 ]
 [ 0.46157021  0.43227682  0.58489093  0.74553395]]
```

### 1、random.rand

```python
# numpy.random.rand(d0, d1, ..., dn)：生成一个[0,1)之间的随机浮点数或N维浮点数组 —— 均匀分布

# 生成一个随机浮点数
a = np.random.rand()
print(a,type(a))  

# 生成形状为4的一维数组
b = np.random.rand(4)
print(b,type(b))  

# 生成形状为2*3的二维数组，注意这里不是((2,3))
c = np.random.rand(2,3)
print(c,type(c))  



0.3671245126484347 <class 'float'>
[ 0.95365841  0.45627035  0.71528562  0.98488116] <class 'numpy.ndarray'>
[[ 0.82284657  0.95853197  0.87376954]
 [ 0.53341526  0.17313861  0.18831533]] <class 'numpy.ndarray'>
```

**结合matplotlib图表**

```python
import matplotlib.pyplot as plt  # 导入matplotlib模块，用于图表辅助分析

% matplotlib inline   # 魔法函数，每次运行自动生成图表

# 生成1000个均匀分布的样本值
samples1 = np.random.rand(1000)
samples2 = np.random.rand(1000)
plt.scatter(samples1,samples2)
# <matplotlib.collections.PathCollection at 0x7bb52e8>
```

![img](data:image/png;base64,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%0AERGRaP8HPyLaK+bpsZcAAAAASUVORK5CYII=)

### 2、random.randn

```python
# numpy.random.randn(d0, d1, ..., dn)：生成一个浮点数或N维浮点数组 —— 正态分布
# randn和rand的参数用法一样、

# 生成1000个正太的样本值
samples1 = np.random.randn(1000)
samples2 = np.random.randn(1000)
plt.scatter(samples1,samples2)
# <matplotlib.collections.PathCollection at 0x842ea90>
```

![img](data:image/png;base64,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%0ApwAAAABJRU5ErkJggg==)

### 3、random.randint

```python
# numpy.random.randint(low, high=None, size=None, dtype='l')：生成一个整数或N维整数数组
# 若high不为None时，取[low,high)之间随机整数，否则取值[0,low)之间随机整数，且high必须大于low 
# dtype参数：只能是int类型  

# low=2：生成1个[0,2)之间随机整数  
print(np.random.randint(2)) # 0

# low=2,size=5 ：生成5个[0,2)之间随机整数
print(np.random.randint(2,size=5)) # [0 1 1 0 1]

# low=2,high=6,size=5：生成5个[2,6)之间随机整数  
print(np.random.randint(2,6,size=5)) # [2 5 2 3 5]

# low=2,size=(2,3)：生成一个2x3整数数组,取数范围：[0,2)随机整数 
print(np.random.randint(2,size=(2,3)))
"""
[[0 1 1]
 [1 1 1]]
"""

# low=2,high=6,size=(2,3)：生成一个2*3整数数组,取值范围：[2,6)随机整数  
print(np.random.randint(2,6,(2,3)))
"""
[[4 4 3]
 [2 3 3]]
"""
```

## 7 Numpy数据的输入输出

- numpy读取/写入数组数据、文本数据

### 1、存储数组数据

```python
# 存储数组数据 .npy文件

import os
os.chdir('C:/Users/Hjx/Desktop/')
ar = np.random.rand(5,5)
print(ar)
np.save('arraydata.npy', ar)

# 也可以直接 np.save('C:/Users/Hjx/Desktop/arraydata.npy', ar)
[[ 0.57358458  0.71126411  0.22317828  0.69640773  0.97406015]
 [ 0.83007851  0.63460575  0.37424462  0.49711017  0.42822812]
 [ 0.51354459  0.96671598  0.21427951  0.91429226  0.00393325]
 [ 0.680534    0.31516091  0.79848663  0.35308657  0.21576843]
 [ 0.38634472  0.47153005  0.6457086   0.94983697  0.97670458]]
```

### 2、读取数组数据

```python
# 读取数组数据 .npy文件

import os
os.chdir('C:/Users/Hjx/Desktop/')
ar_load =np.load('arraydata.npy')
print(ar_load)

# 也可以直接 np.load('C:/Users/Hjx/Desktop/arraydata.npy')
[[ 0.57358458  0.71126411  0.22317828  0.69640773  0.97406015]
 [ 0.83007851  0.63460575  0.37424462  0.49711017  0.42822812]
 [ 0.51354459  0.96671598  0.21427951  0.91429226  0.00393325]
 [ 0.680534    0.31516091  0.79848663  0.35308657  0.21576843]
 [ 0.38634472  0.47153005  0.6457086   0.94983697  0.97670458]]
```



## 8 广播机制

广播(Broadcast)是 numpy **对不同形状(shape)的*数组进行数值计算*的方式**， 对数组的算术运算通常在相应的元素上进行。

当运算中的 2 个数组的形状不同时，numpy 将自动触发广播机制。如：

```python
import numpy as np 
 
a = np.array([[ 0, 0, 0],
           [10,10,10],
           [20,20,20],
           [30,30,30]])
b = np.array([1,2,3])
print(a + b)
"""
[[ 1  2  3]
 [11 12 13]
 [21 22 23]
 [31 32 33]]
"""
```

易懂参考：https://www.cnblogs.com/jiaxin359/p/9021726.html

菜鸟教程：https://www.runoob.com/numpy/numpy-broadcast.html

### 1、广播的规则

- 让所有输入数组都向其中形状最长的数组看齐，形状中不足的部分都通过在前面加 1 补齐。
- 输出数组的形状是输入数组形状的各个维度上的最大值。
- 如果输入数组的某个维度和输出数组的对应维度的长度相同或者其长度为 1 时，这个数组能够用来计算，否则出错。
- 当输入数组的某个维度的长度为 1 时，沿着此维度运算时都用此维度上的第一组值。

**简单理解：**对两个数组，分别比较他们的每一个维度（若其中一个数组没有当前维度则忽略），满足：

- 数组拥有相同形状。
- 当前维度的值相等。
- 当前维度的值有一个是 1。

若条件不满足，抛出 **"ValueError: frames are not aligned"** 异常。

#### 1 数组维度不同，后缘维度的轴长相符

 我们来看一个例子：

```python
import numpy as np

arr1 = np.array([[0, 0, 0],[1, 1, 1],[2, 2, 2], [3, 3, 3]])  #arr1.shape = (4,3)
arr2 = np.array([1, 2, 3])    #arr2.shape = (3,)
arr_sum = arr1 + arr2
print(arr_sum)

输入结果如下:
'''
[[1 2 3]
 [2 3 4]
[3 4 5]
[4 5 6]]
'''
```

 上例中arr1的shape为（4,3），arr2的shape为（3，）。可以说前者是二维的，而后者是一维的。但是它们的后缘维度相等，arr1的第二维长度为3，和arr2的维度相同。arr1和arr2的shape并不一样，但是它们可以执行相加操作，这就是通过广播完成的，在这个例子当中是将arr2沿着0轴进行扩展。

 上面程序当中的广播如下图所示：

![image](https://images2018.cnblogs.com/blog/890640/201805/890640-20180510210455543-2125343324.png)

同样的例子还有：

![image](https://images2018.cnblogs.com/blog/890640/201805/890640-20180510210457361-2084634558.png)

 从上面的图可以看到，（3,4,2）和（4,2）的维度是不相同的，前者为3维，后者为2维。但是它们后缘维度的轴长相同，都为（4,2），所以可以沿着0轴进行广播。

 同样，还有一些例子：（4,2,3）和（2,3）是兼容的，（4,2,3）还和（3）是兼容的，后者需要在两个轴上面进行扩展。

 

#### 2 数组维度相同，其中有个轴为1

 我们来看下面的例子：

```python
import numpy as np

arr1 = np.array([[0, 0, 0],[1, 1, 1],[2, 2, 2], [3, 3, 3]])  #arr1.shape = (4,3)
arr2 = np.array([[1],[2],[3],[4]])    #arr2.shape = (4, 1)

arr_sum = arr1 + arr2
print(arr_sum)

输出结果如下：
[[1 1 1]
 [3 3 3]
 [5 5 5]
 [7 7 7]]
```

  arr1的shape为（4,3），arr2的shape为（4,1），它们都是二维的，但是第二个数组在1轴上的长度为1，所以，可以在1轴上面进行广播，如下图所示：

 ![image](https://images2018.cnblogs.com/blog/890640/201805/890640-20180510210458819-1248164149.png)

在这种情况下，两个数组的维度要保证相等，其中有一个轴的长度为1，这样就会沿着长度为1的轴进行扩展。这样的例子还有：（4,6）和（1,6） 。（3,5,6）和（1,5,6）、（3,1,6）、（3,5,1），后面三个分别会沿着0轴，1轴，2轴进行广播。

 后话：还有上面两种结合的情况，如（3,5,6）和（1,6）是可以相加的。在TensorFlow当中计算张量的时候也是用广播机制，并且和numpy的广播机制是一样的。

### 2、运算

#### 1 tile沿横纵向复制

返回复制后的array(数组)。

```python
# np.tile(对象, (纵向，横向)) # 把数组沿横向、纵向复制。
b = np.array([[1, 2], [3, 4]])
np.tile(b, 2) #沿X轴复制2倍
# array([[1, 2, 1, 2],
#       [3, 4, 3, 4]])
np.tile(b, (2, 1))#沿X轴复制1倍（相当于没有复制），再沿Y轴复制2倍
# array([[1, 2],
#        [3, 4],
#        [1, 2],
#        [3, 4]])
```

#### 2 bincount统计次数

返回array(数组，数据类型)。

```python
# np.bincount(x) # 统计索引出现次数
# bin的数量比x中最大数据多1 例如:x最大为4  bin数量为5(index从0到4), bincount输出一个一维数组为5个数
x = np.array([1, 2, 3, 3, 0, 1, 4])
np.bincount(x) # array([1, 2, 1, 2, 1], dtype=int64)
# x中0出现1次，1出现2次，2出现1次，3出现2次，2出现1次

# weights添加权重
w = np.array([0.3, 0.5, 0.7, 0.6, 0.1, -0.9, 1])
np.bincount(x, weights=w) # array([ 0.1, -0.6,  0.5,  1.3,  1. ])
# w[4] = 0.1 -> x中0的索引值index=4，在w中访问index=4对应的权重值为0.1 
# w[0] + w[5] = -0.6 ->x中1出现两次的索引值index=0，index=5，在w中访问index对应的权重值分别为0.3和-0.9，相加为-0.6

# minlength设置长度， 不足以0补齐
np.bincount(x, weights=w, minlength=10) # array([ 0.1, -0.6,  0.5,  1.3,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ])
```

#### 3 argmax最大值索引

返回索引值。

```python
x = np.array([1, 2, 3, 3, 0, 1, 4])
# 表示返回沿轴axis元素最大值对应的索引值
np.argmax(x, axis=None, out=None)
# 6 -> x中元素4是最大值对应的索引值为6

# 若出现最大值有多个，则输出第一个索引值
x = np.array([1, 2, 2, 3, 4, 1, 4, 0])
np.argmax(x) # 4 -> x中元素4是最大值对应的索引值分别为4和6，只返回4
```

**bincount与argmax结合使用**

```求取精度
x = np.array([1, 2, 3, 3, 4, 0, 1])
# np.bincount(x) -> array([1, 2, 1, 2, 1], dtype=int64)
np.argmax(np.bincount(x)) # 1
# 0出现1次，1出现2次，2出现1次，3出现2次，4出现1次
# 出现次数最多是出现1次
```

#### 4 round与around求取精度

**round**

原则：对于浮点型数据，四舍六入

```python
# np.round(数据, decimal=保留的小数位数)
np.round(4.5, 0)  # 4.0
np.round(4.5, 1)  # 4.5
np.round(4.55, 1) # 4.6
np.round(4.55, 2) # 4.55
```

**around**

```python
# 当decimals为正数时表示小数点位个数(遵循四舍五入)
# 当decimals为负数时表示整数位个数(-1(个位向十位)、-2(十位向百位)···遵循四舍五入)
# 0是array([ -1.,   1.,   3.,  10.])
np.around([-0.6, 1.27689, 2.5678, 9.876], decimals=0)
# 1时array([-0.6,  1.3,  2.6,  9.9])
np.around([-0.6, 1.27689, 2.5678, 9.876], decimals=1)
# -1时array([-0.,  0.,  0., 10.])->个位0,1,2都是要舍去=0，个位9满5向十位进1=10
np.around([-0.6, 1.27689, 2.5678, 9.876], decimals=-1)
# -2时array([ -0.,   0.,   0.,   0.,   0., 200., 100.])
# ->前面几个数十位都是0要舍去=0，15的十位1也要舍去=0,190和60的十位满5向十位进1=10
np.around([-0.6, 1.27689, 2.5678, 9.876, 15, 190, 60], decimals=-2)
```

#### 5 diff横纵向差值

```python
x = np.arange(1, 16).reshape(3, 5)
"""
array([[ 1,  2,  3,  4,  5],
       [ 6,  7,  8,  9, 10],
       [11, 12, 13, 14, 15]])
"""

np.diff(x, axis=0) # 列向差值，(3, 5)—>(2, 5)
"""
array([[5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5]])
"""

np.diff(x, axis=1) # 行向差值，(3, 5)->(3, 4)
"""
array([[1, 1, 1, 1],
       [1, 1, 1, 1],
       [1, 1, 1, 1]])
"""
```

#### 6 floor取整

```python
np.floor([.5, .9, -0.1, 1.6, 1.3, -0.8])  # 取整  负数往左取，正数往右取
# array([ 0.,  0., -1.,  1.,  1., -1.])
```

#### 7 ceil取上限

```python
np.ceil([1.2, 1.5, -1.3, -0.3, 0.1]) # 上限  最大整数
# array([ 2.,  2., -1., -0.,  1.])
```

#### 8 where查找

```python
x = np.random.randint(10, 100, 100)
np.where(x>50, x, 1) # 查找显示x中大于50的元素，其余元素用1填充，填充可以任意设置

"""
array([[ 1, 62, 88, 69,  1,  1, 98, 57,  1, 77],
       [68, 63,  1,  1, 96, 92, 62,  1, 58,  1],
       [57, 91,  1,  1, 68, 78,  1,  1, 89,  1],
       [58,  1, 68, 82,  1,  1, 62,  1,  1, 56],
       [93, 95, 66,  1,  1,  1,  1,  1,  1,  1],
       [68, 86, 63, 86,  1,  1, 87,  1,  1,  1],
       [ 1, 52,  1, 62, 89, 79,  1,  1,  1, 52],
       [96, 84,  1, 75,  1,  1, 73, 64,  1, 56],
       [ 1,  1, 70,  1,  1,  1,  1, 98,  1, 51],
       [ 1, 83,  1,  1, 99, 80,  1, 57, 62,  1]])
"""
```

#### 9 运算函数

##### 加减乘除

```python
a = np.arange(9, dtype=np.float_).reshape(3, 3)
"""
array([[0., 1., 2.],
       [3., 4., 5.],
       [6., 7., 8.]])
"""
b = np.array([10, 10, 10]) # array([10, 10, 10])

# 相加
np.add(a, b)
"""
array([[10., 11., 12.],
       [13., 14., 15.],
       [16., 17., 18.]])
"""
# 相减
np.subtract(a, b)
"""
array([[-10.,  -9.,  -8.],
       [ -7.,  -6.,  -5.],
       [ -4.,  -3.,  -2.]])
"""
# 相乘
np.multiply(a, b)
"""
array([[ 0., 10., 20.],
       [30., 40., 50.],
       [60., 70., 80.]])
"""
# 相除
np.divide(a, b)
"""
array([[0. , 0.1, 0.2],
       [0.3, 0.4, 0.5],
       [0.6, 0.7, 0.8]])
"""
```

##### 倒数

```python
# 倒数
# 1 / 4 => 4 / 1
a = np.array([0.25, 1.33, 1, 100]) # [0.25, 1.33, 1, 100]
np.reciprocal(a) # array([4.       , 0.7518797, 1.       , 0.01     ])
```

##### 幂运算

```python
# 幂运算
# 将a数组中的元素为底数, 计算其2次方
a = np.array([10, 100, 1000])
np.power(a, 2) # array([    100,   10000, 1000000], dtype=int32)
```

##### 取余运算

```python
a = np.array([10, 20, 30])
b = np.array([3, 5, 7])
# a的元素/b的元素的余数
np.mod(a, b) # array([1, 0, 2], dtype=int32)
```

##### 统计函数

```python
# amin()  amax()  计算数组中的元素沿轴 最小值或最大值
a = np.array([[1, 3, 5], [8, 4, 1], [2, 4, 9]]) 
"""
array([[1, 3, 5],
       [8, 4, 1],
       [2, 4, 9]])
"""
# 列的最大值
np.amax(a, axis=0) # array([8, 4, 9])
# 行的最小值
np.amin(a, axis=1) # array([1, 1, 2])

# ptp统计最大元素与最小元素的差值
np.ptp(a) # 8 ->数组a中最大值9-数组a中最小值1=8
np.ptp(a, axis=0) # 数组每列的最大最小差值array([7, 1, 8])

# 百分位数
# 百分位数是统计中使用的度量，表示小于这个值的观察值的百分比。
a = np.array([[10, 7, 4], [3, 2, 1]])
# (a, q, axis) a 数组 q 百分位数(0 - 100之间) axis 轴
np.percentile(a, 50)  # 3.5  # 50%的分位数，就是a排序后的中位数 (4+3)/7=3.5
np.percentile(a, 100) # 10.0 # 100%的分位数，就是a中最大值
np.percentile(a, 50, axis=0) # array([6.5, 4.5, 2.5])
np.percentile(a, 100, axis=0) # array([10.,  7.,  4.])
np.percentile(a, 50, axis=1) # array([7., 2.])
np.percentile(a, 100, axis=1) # array([10.,  3.])

# 中位数
a = np.array([[10, 7, 4], [3, 2, 1]])
np.median(a)  # 3.5

# 方差与平方差
# 一组数据平均值分散程度的一种度量，标准差是方差算术平方根 
a = np.array([[10, 7, 4], [3, 2, 1]])
# 方差mean((x - x.mean()) ** 2)
np.var(a)  # 方差 将a代入方差var代替x 9.583333333333334
# np.mean((a - a.mean()) ** 2)  # 9.583333333333334

# 标准差std = sqrt(mean((x - x.mean()) ** 2))
np.std(a)  # 将a代入标准差std代替x 3.095695936834452
# std = np.sqrt(np.mean((a - a.mean()) ** 2))  # 3.095695936834452
```



## 9 切片和索引

### 1、一维数组切片索引

ndarray对象的内容可以通过索引或切片来访问和修改，与 Python 中 list 的切片操作一样。

```python
import numpy as np

# 通过list索引切片的操作进行索引切片
a = np.arange(20) # 形状1*1*1 ==> 1*行*列
print(a) # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]
print(a[4])  # 索引 4
print(a[3:6])  # 切片 [3 4 5]
```

ndarray 数组可以基于 0 - n 的下标进行索引，切片对象可以通过**内置的 slice 函数**，并设置 start, stop 及 step 参数进行，从原数组中切割出一个新数组。

```python
import numpy as np
 
# 通过内置的 slice 函数进行索引切片
a = np.arange(10) # [ 0  1  2  3  4  5  6  7  8  9]
s = slice(2,7,2)   # 从索引 2 开始到索引 7 停止，间隔为2
print (a[s]) # 通过slice函数切片 [2  4  6]
```



### 2、多维数组切片索引

- 索引：数组对象[维切片] [[行索引] [列索引]]

- 切片：数组对象[维切片, [行切片,  列切片]]

```python
# 多维数组索引及切片
ar = np.arange(16).reshape(4,4) # 1*4*4 ==> 1*行*列
# 4*4的二维数组
print(ar, '数组轴数为', ar.ndim)   
    # [[ 0  1  2  3]
    #  [ 4  5  6  7]
    #  [ 8  9 10 11]
    #  [12 13 14 15]] 数组轴数为2
# 一次索引，得到一维数组
print(ar[2],  '数组轴数为', ar[2].ndim) # [ 8  9 10 11] 数组轴数为1  
# 二次索引，得到一维数组中的一个元素
print(ar[2][1])  # 9
# 切片 两个一维数组组成的二维数组
print(ar[1:3],  '数组轴数为', ar[1:3].ndim)  
    # [[ 4  5  6  7]
    #  [ 8  9 10 11]] 数组轴数为2
# 切片 数组中的第三行第三列 → 10
print(ar[2,2]) # 10 
# 切片 数组中的1、2行的2、3、4列 → 二维数组
print(ar[:2,1:]) 
    # [[1 2 3]
    #  [5 6 7]]
# 切片还可以包括省略号 …，来使选择元组的长度与数组的维度相同。 如果在行位置使用省略号，它将返回包含行中元素的 ndarray。
print (ar[...,1])   # 第2列元素  # [ 1  5  9 13]
print (ar[1,...])   # 第2行元素  # [4 5 6 7]
print (ar[...,1:])  # 第2列及剩下的所有元素
    # [[ 1  2  3]
    #  [ 5  6  7]
    #  [ 9 10 11]
    #  [13 14 15]]

    
# 三维数组索引及切片
ar = np.arange(8).reshape(2,2,2)  # 2*2*2 ==> 2*行*列
# 2*2*2的数组
print(ar, '数组轴数为', ar.ndim)   
    # [[[0 1]
    #   [2 3]]

    #  [[4 5]
    #   [6 7]]]  数组轴数为 3
# 索引
# 三维数组的下一个维度的第一个数组 → 一个二维数组
print(ar[0],  '数组轴数为', ar[0].ndim) 
    # [[0 1]
    #  [2 3]] 数组轴数为 2
# 三维数组的下一个维度的第一个数组下的第一行 → 一个一维数组
print(ar[0][0],  '数组轴数为', ar[0][0].ndim)  # [0 1] 数组轴数为 1
# 三维数组的下一个维度的第一个数组下的第一行下的第二列 → 一个元素
print(ar[0][0][1],  '数组轴数为', ar[0][0][1].ndim)  # 1 数组轴数为0
# 切片
# 切取第一个维度的1、2行的1列 → 一维数组
print(ar[0][:2,:1])
    # [[0]
    #  [2]]
```

### 3、整数数组索引

```python
# 整数数组索引
import numpy as np 
 
x = np.array([[1,  2],  [3,  4],  [5,  6]]) 
# 获取数组中(0,0)，(1,1)和(2,0)位置处的元素。
y = x[[0,1,2], [0,1,0]]  
print(y) # [1  4  5]

# 获取了 4*3 数组中的四个角的元素。 行索引是 [0,0] 和 [3,3]，而列索引是 [0,2] 和 [0,2]。
x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])  
print('我们的数组是：' )
print(x)
    # 我们的数组是：
    # [[ 0  1  2]
    #  [ 3  4  5]
    #  [ 6  7  8]
    #  [ 9 10 11]]
rows = np.array([[0,0],[3,3]])  # [[0 0] [3 3]]
cols = np.array([[0,2],[0,2]])  # [[0 2] [0 2]]
y = x[rows,cols]  # > [0,0] [0,2] [3,0] [3,2]
print('这个数组的四个角元素是：')
print(y)
    # 这个数组的四个角元素是：
    # [[ 0  2]
    #  [ 9 11]]
# 返回的结果是包含每个角元素的 ndarray 对象。

# 可以借助切片 : 或 … 与索引数组组合。如下面例子：
a = np.array([[1,2,3], [4,5,6],[7,8,9]])
b = a[1:3, 1:3]
c = a[1:3,[1,2]]
d = a[...,1:]
print(b)
    # [[5 6]
    #  [8 9]]
print(c)
    # [[5 6]
    #  [8 9]]
print(d)
    # [[2 3]
    #  [5 6]
    #  [8 9]]
```



### 4、布尔型索引及切片

可以通过一个布尔数组来索引目标数组。

布尔索引通过布尔运算（如：比较运算符）来获取符合指定条件的元素的数组

```python
# 布尔型索引及切片

ar = np.arange(12).reshape(3,4)
i = np.array([True,False,True])
j = np.array([True,True,False,False])
print(ar)
print(i)
print(j)
print(ar[i,:])  # 在第一维度做判断，只保留True，这里第一维度就是行，ar[i,:] = ar[i]（简单书写格式）
print(ar[:,j])  # 在第二维度做判断，这里如果ar[:,i]会有警告，因为i是3个元素，而ar在列上有4个
# 布尔型索引：以布尔型的矩阵去做筛选

m = ar > 5
print(m)  # 这里m是一个判断矩阵
print(ar[m])  # 用m判断矩阵去筛选ar数组中>5的元素 → 重点！后面的pandas判断方式原理就来自此处
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
[ True False  True]
[ True  True False False]
[[ 0  1  2  3]
 [ 8  9 10 11]]
[[0 1]
 [4 5]
 [8 9]]
[[False False False False]
 [False False  True  True]
 [ True  True  True  True]]
[ 6  7  8  9 10 11]
```

In [15]:

```python
# 数组索引及切片的值更改、复制

ar = np.arange(10)
print(ar)
ar[5] = 100
ar[7:9] = 200
print(ar)
# 一个标量赋值给一个索引/切片时，会自动改变/传播原始数组

ar = np.arange(10)
b = ar.copy()
b[7:9] = 200
print(ar)
print(b)
# 复制
[0 1 2 3 4 5 6 7 8 9]
[  0   1   2   3   4 100   6 200 200   9]
[0 1 2 3 4 5 6 7 8 9]
[  0   1   2   3   4   5   6 200 200   9]
```



## 10 byteswap字节交换

多字节对象 -> 连续字节序列 

- 大端模式：指数据的高字节保存在内存的低地址中
- 小端模式：指数据的低字节保存在内存的低地址中

```python
a = np.array([1, 26, 789, 6789], dtype=np.int16) 
# array([   1,   26,  789, 6789], dtype=int16)

# 以16进制显示a的内存地址
map(hex, a) # <map at 0x2298d228580>
# byteswap 大小模式交换，完成字节交换
a.byteswap(True) # array([   256,   6656,   5379, -31462], dtype=int16)
map(hex, a) # <map at 0x2298d572460>
```



## 11 线性代数

> dot -> 两个数组点积元素对应相乘 ->(a, b, out=None(保存dot计算结果))
> vdot -> 两个向量的点积 -> 机器
> inner -> 两个数组的内积
> matmul -> 两个数组的矩阵积
> determinant -> 数组行列式
> solve -> 求解线性矩阵方程 -> 线性数据 非线性数据 -> 线性回归
> inv -> 计算矩阵的乘法逆矩阵

## ndarray 对象的内部机理

在前面的内容中，我们已经详细讲述了 `ndarray` 的使用，在本章的开始部分，我们来聊一聊 `ndarray` 的内部机理，以便更好的理解后续的内容。

### 1、ndarray 的组成

*ndarray* 与数组不同，它不仅仅包含数据信息，还包括其他描述信息。*ndarray* 内部由以下内容组成：

- 数据指针：一个指向实际数据的指针。
- 数据类型（dtype）：描述了每个元素所占字节数。
- 维度（shape）：一个表示数组形状的元组。
- 跨度（strides）：一个表示从当前维度前进道下一维度的当前位置所需要“跨过”的字节数。

*NumPy* 中，数据存储在一个**均匀连续的内存块**中，可以这么理解，*NumPy* 将多维数组在内部以一维数组的方式存储，我们只要知道了每个元素所占的字节数（dtype）以及每个维度中元素的个数（shape），就可以快速定位到任意维度的任意一个元素。

*dtype* 及 *shape* 前文中已经有详细描述，这里我们来讲下 *strides*。

**示例**

```python
ls = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], 
      [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]
a = np.array(ls, dtype=int)
print(a)
print(a.strides)
```

**输出：**

```python
[[[ 1  2  3  4]
  [ 5  6  7  8]
  [ 9 10 11 12]]

 [[13 14 15 16]
  [17 18 19 20]
  [21 22 23 24]]]
(48, 16, 4)
```

上例中，我们定义了一个三维数组，*dtype* 为 *int*，*int* 占 4个字节。
第一维度，从元素 1 到元素 13，间隔 12 个元素，总字节数为 48；
第二维度，从元素 1 到元素 5，间隔 4 个元素，总字节数为 16；
第三维度，从元素 1 到元素 2，间隔 1 个元素，总字节数为 4。
所以跨度为(48, 16, 4)。

## 普通迭代

*ndarray* 的普通迭代跟 *Python* 及其他语言中的迭代方式无异，**N** 维数组，就要用 **N** 层的 `for` 循环。

**示例：**

```python
import numpy as np

ls = [[1, 2], [3, 4], [5, 6]]
a = np.array(ls, dtype=int)
for row in a:
    for cell in row:
        print(cell)
```

**输出：**

```undefined
1
2
3
4
5
6
```

上例中，`row` 的数据类型依然是 `numpy.ndarray`，而 `cell` 的数据类型是 `numpy.int32`。

## nditer 多维迭代器

*NumPy* 提供了一个高效的**多维迭代器**对象：*nditer* 用于迭代数组。在普通方式的迭代中，**N** 维数组，就要用 **N** 层的 `for` 循环。但是使用 `nditer` 迭代器，一个 `for` 循环就能遍历整个数组。（因为 *ndarray* 在内存中是连续的，连续内存不就相当于是一维数组吗？遍历一维数组当然只需要一个 `for` 循环就行了。）

### 1、基本示例

**例一：**

```python
ls = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
      [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]
a = np.array(ls, dtype=int)
for x in np.nditer(a):
    print(x, end=", ")
```

**输出：**

```python
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
```

### 2、order 参数：指定访问元素的顺序

创建 *ndarray* 数组时，可以通过 *order* 参数指定元素的顺序，按行还是按列，这是什么意思呢？来看下面的示例：

**例二：**

```python
ls = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
      [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]
a = np.array(ls, dtype=int, order='F')
for x in np.nditer(a):
    print(x, end=", ")
```

**输出：**

```undefined
1, 13, 5, 17, 9, 21, 2, 14, 6, 18, 10, 22, 3, 15, 7, 19, 11, 23, 4, 16, 8, 20, 12, 24, 
```

> `nditer` 默认以内存中元素的顺序（order='K'）访问元素，对比**例一**可见，创建 *ndarray* 时，指定不同的顺序将影响元素在内存中的位置。

**例三：**
`nditer` 也可以指定使用某种顺序遍历。

```python
ls = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
      [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]
a = np.array(ls, dtype=int, order='F')
for x in np.nditer(a, order='C'):
    print(x, end=", ")
```

**输出：**

```undefined
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
```

> 行主顺序（`order='C'`）和列主顺序（`order='F'`），参看 https://en.wikipedia.org/wiki/Row-_and_column-major_order。例一是行主顺序，例二是列主顺序，如果将 *ndarray* 数组想象成一棵树，那么会发现，行主顺序就是深度优先，而列主顺序就是广度优先。NumPy 中之所以要分行主顺序和列主顺序，主要是为了在矩阵运算中提高性能，顺序访问比非顺序访问快几个数量级。（矩阵运算将会在后面的章节中讲到）

### 3、op_flags 参数：迭代时修改元素的值

默认情况下，*nditer* 将视待迭代遍历的数组为只读对象（**readonly**），为了在遍历数组的同时，实现对数组元素值得修改，必须指定 `op_flags` 参数为 **readwrite** 或者 **writeonly** 的模式。

**例四：**

```python
import numpy as np

a = np.arange(5)
for x in np.nditer(a, op_flags=['readwrite']):
    x[...] = 2 * x
print(a)
```

**输出：**

```json
[0 1 2 3 4]
```

### 4、flags 参数

`flags` 参数需要传入一个数组或元组，既然参数类型是数组，我原本以为可以传入多个值的，但是，就下面介绍的 4 种常用选项，我试了，不能传多个，例如 `flags=['f_index', 'external_loop']`，运行**报错**。

#### （1）使用外部循环：external_loop

**将一维的最内层的循环转移到外部循环迭代器，使得 \*NumPy\* 的矢量化操作在处理更大规模数据时变得更有效率。**

简单来说，当指定 `flags=['external_loop']` 时，将返回一维数组而并非单个元素。具体来说，当 *ndarray* 的顺序和遍历的顺序一致时，将所有元素组成一个一维数组返回；当 *ndarray* 的顺序和遍历的顺序不一致时，返回每次遍历的一维数组（这句话特别不好描述，看例子就清楚了）。

**例五：**

```python
import numpy as np

ls = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
      [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]
a = np.array(ls, dtype=int, order='C')
for x in np.nditer(a, flags=['external_loop'], order='C'):
    print(x,)
```

**输出：**

```json
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24]
```

**例六：**

```python
b = np.array(ls, dtype=int, order='F')
for x in np.nditer(b, flags=['external_loop'], order='C'):
    print(x,)
```

**输出：**

```json
[1 2 3 4]
[5 6 7 8]
[ 9 10 11 12]
[13 14 15 16]
[17 18 19 20]
[21 22 23 24]
```

#### （2）追踪索引：c_index、f_index、multi_index

**例七：**

```python
import numpy as np

a = np.arange(6).reshape(2, 3)
it = np.nditer(a, flags=['f_index'])

while not it.finished:
    print("%d <%d>" % (it[0], it.index))
    it.iternext()
```

**输出：**

```xml
0 <0>
1 <2>
2 <4>
3 <1>
4 <3>
5 <5>
```

这里索引之所以是这样的顺序，因为我们选择的是列索引（f_index）。直观的感受看下图：

![img](https://img-blog.csdnimg.cn/20190328211901100.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2d1bGlhbmcyMQ==,size_16,color_FFFFFF,t_70)

> 遍历元素的顺序是由 `order` 参数决定的，而行索引（c_index）和列索引（f_index）不论如何指定，并不会影响元素返回的顺序。它们仅表示在当前内存顺序下，如果按行/列顺序返回，各个元素的下标应该是多少。

**例八：**

```python
import numpy as np

a = np.arange(6).reshape(2, 3)
it = np.nditer(a, flags=['multi_index'])

while not it.finished:
    print("%d <%s>" % (it[0], it.multi_index))
    it.iternext()
```

**输出：**

```xml
0 <(0, 0)>
1 <(0, 1)>
2 <(0, 2)>
3 <(1, 0)>
4 <(1, 1)>
5 <(1, 2)>
```

### 5、同时迭代多个数组

说到同时遍历多个数组，第一反应会想到 *zip* 函数，而在 *nditer* 中不需要。

**例九：**

```python
a = np.array([1, 2, 3], dtype=int, order='C')
b = np.array([11, 12, 13], dtype=int, order='C')
for x, y in np.nditer([a, b]):
    print(x, y)
```

**输出：**

```undefined
1 11
2 12
3 13
```

## 其他函数

### 1、flatten函数

`flatten` 函数将多维 *ndarray* 展开成一维 *ndarray* 返回。
**语法：**

```vbnet
flatten(order='C')
```

**示例：**

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]], dtype=int, order='C')
b = a.flatten()
print(b)
print(type(b))
```

**输出：**

```python
[1 2 3 4 5 6]
<class 'numpy.ndarray'>
```

### 2、flat

`flat` 返回一个迭代器，可以遍历数组中的每一个元素。

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]], dtype=int, order='C')
for b in a.flat:
    print(b)
print(type(a.flat))
```

**输出：**

```python
1
2
3
4
5
6
<class 'numpy.flatiter'>
```











```
# 存储/读取文本文件

ar = np.random.rand(5,5)
np.savetxt('array.txt',ar, delimiter=',')
# np.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')：存储为文本txt文件

ar_loadtxt = np.loadtxt('array.txt', delimiter=',')
print(ar_loadtxt)
# 也可以直接 np.loadtxt('C:/Users/Hjx/Desktop/array.txt')
[[ 0.28280684  0.66188985  0.00372083  0.54051044  0.68553963]
 [ 0.9138449   0.37056825  0.62813711  0.83032184  0.70196173]
 [ 0.63438739  0.86552157  0.68294764  0.2959724   0.62337767]
 [ 0.67411154  0.87678919  0.53732168  0.90366896  0.70480366]
 [ 0.00936579  0.32914898  0.30001813  0.66198967  0.04336824]]
```