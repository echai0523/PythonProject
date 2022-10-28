
## 删除空行/列: dropna
- axis：轴。 
  - 0或'index': 按行删除；
  - 1或'columns': 按列删除。
- how：筛选方式。
  - any: 该行/列只要有一个以上的空值，就删除该行/列；
  - all: 该行/列全部都为空值，就删除该行/列。
- thresh：非空元素最低数量。int型，默认为None。
  - 如果该行/列中，非空元素数量小于这个值，就删除该行/列。
- subset：指定筛选某列或某行。由subset限制的子区域，是判断是否删除该行/列的条件判断区域。
  - axis=0或‘index’: subset中元素为列的索引；
  - axis=1或者‘column’: subset中元素为行的索引。
- inplace：是否原地替换。布尔值，默认为False。
  - True: 在原DataFrame上进行操作，返回值为None。
> df.dropna(axis=0, how="any", thresh=None, subset=['annotation'], inplace=False)

## 根据某列去重: drop_duplicates
- subset： 列表的形式填写要进行去重的列名，默认为 None ，表示根据所有列进行。
- keep： 可选参数有三个：first、 last、 False， 默认值 first。 
  - first 表示： 保留第一次出现的重复行，删除后面的重复行。
  - last 表示： 删除重复项，保留最后一次出现。
  - False 表示： 删除所有重复项。
- inplace：默认为 False，删除重复项后返回副本。
  - True，直接在原数据上删除重复项。
> df.drop_duplicates(subset=['comment'], keep='first', inplace=True)




