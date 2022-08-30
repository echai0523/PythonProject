# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 17:04

input: 
output: 
Short Description: 

Change History:

"""
import pandas as pd
import numpy as np


def data_extract_v1():
    """选择数据"""
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=['A', 'B', 'C', 'D'])

    print(df['A'], df.A)
    print(df[0:3], df['20130102':'20130104'])

    # select by label: loc
    print(df.loc['20130102'])
    print(df.loc[:, ['A', 'B']])
    print(df.loc['20130102', ['A', 'B']])

    # select by position: iloc
    print(df.iloc[3])
    print(df.iloc[3, 1])
    print(df.iloc[3:5, 0:2])
    print(df.iloc[[1, 2, 4], [0, 2]])

    # mixed selection: ix
    print(df.ix[:3, ['A', 'C']])
    # Boolean indexing
    print(df[df.A > 0])
    """设置值"""
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=['A', 'B', 'C', 'D'])

    df.iloc[2, 2] = 1111
    df.loc['2013-01-03', 'D'] = 2222
    df.A[df.A > 0] = 0
    df['F'] = np.nan
    df['G'] = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130101', periods=6))
    print(df)


def data_extract():
    """
    loc()   通过行/lie名选取    -> type: str
    iloc()  通过索引值index选取 -> type: int
    :return:
    """
    # 数据选取
    # 查看指定列  return - Series类型数据
    print(df['Q1'])
    print(df.Q1)  # 如何列名满足python变量名要求，可使用

    # 选择多列
    print(df[['team', 'Q1']])  # 只看这两列，注意括号
    print(df.loc[:, ['team', 'Q1']])  # df.loc[x, y] x行，y列
    # df.iloc[] # 自然索引

    # 查看行
    print(df[df.index == 'Liver'])  # 指定姓名

    # 用自然索引选择，类似列表的切片
    print(df[0:3])  # 前三行
    print(df[0:10:2])  # 在前10个中每两个取一个
    print(df.iloc[:10, :])  # 前10个  # []中必须是整型数据、布尔,切片形式
    print(df.iloc[[True, False, True]])
    print(df.iloc[lambda x: x.index % 2 == 0])

    # 指定行和列
    print(df.loc['Ben', 'Q1':'Q4'])  # 只看Ben的四个季度成绩
    print(df.loc['Eorge':'Alexander', 'team':'Q1'])  # 指定行区间

    # 条件选择
    print(df[df.Q1 > 90])  # Q1>90
    print(df[df.team == 'C'])  # team==C
    print(df[df.index == 'Oscar'])  # 指定索引

    print(df[(df['Q1'] > 90) & (df['team'] == 'C')])  # and关系
    print(df[df['team'] == 'C'].loc[df.Q1 > 90])  # 多重筛选


def sort_():
    # 排序
    df.sort_values(by='Q1')  # 按Q1列数据升序排列
    df.sort_values(by='Q1', ascending=False)  # 降序
    df.sort_values(['team', 'Q1'], ascending=[True, False])  # team先升序再进行Q1降序


def group_agg():
    df.groupby('team').sum()  # 按team分组对应列相加
    df.groupby('team').mean()  # 按team分组对应列求平均
    # 按team分组不同列不同的计算方法
    df.groupby('team').agg({
        'Q1': sum,  # 总和
        'Q2': 'count',  # 总数
        'Q3': 'mean',  # 平均
        'Q4': max,  # 最大值
    })


def data_t():
    print(df.groupby('team').sum().T)  # 转置
    print(df.groupby('team').sum().stack())  # 转置
    print(df.groupby('team').sum().unstack())  # 转置


def main():
    """简单介绍"""
    # 查看数据
    print(df.head())  # 查看 ···前的几条数据
    print(df.head(3))  # 可以写明查看几条数据
    print(df.sample(5))  # 随机查看5(几)条数据
    print(df.index)
    print(df.values)
    print(df.dtypes)

    # 验证数据
    print(df.shape)  # (100, 6)
    print(df.info())  # 查看索引、数据类型和内存信息
    print(df.describe())  # 查看数值类型的汇总统计，计算出各数字字段的总和(count)、平均数(mean)、标准差(std)、最小值(min)、四分位数和最大值(max)
    print(df.dtypes)  # 查看各字段类型
    print(df.axes)  # 显示数据行和列名
    print(df.columns)  # 列名

    # 统计
    print(df.mean())    # 返回所有列均值
    print(df.mean(1))   # 返回所有行均值
    print(df.corr())    # 返回列与列间的相关系数
    print(df.count())   # 返回每一列的非空值个数
    print(df.max())     # 返回每一列最大值
    print(df.min())     # 返回每一列最小值
    print(df.median())  # 返回每一列中位数
    print(df.std())     # 返回每一列标准差
    print(df.var())     # 返回每一列方差
    print(df.mode())    # 返回每一列众数

    # 增加列
    df['total'] = df.Q1 + df.Q2 + df.Q3 + df.Q4
    df['total1'] = df.loc[:, "Q1": "Q4"].apply(lambda x: sum(x), axis=1)

    # 建立索引
    df.set_index('name', inplace=True)  # 建立索引并True生效
    df.head()


if __name__ == '__main__':
    df = pd.read_excel('https://www.gairuo.com/file/data/dataset/team.xlsx')
    # 查、验证、统计、建立索引
    main()
    # 数据选取
    data_extract()
    # 排序
    sort_()
    # 分组聚合
    group_agg()
