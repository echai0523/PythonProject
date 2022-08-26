# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 10:56

input: 
output: 
Short Description:
    - 知识点：
        - isnull()
        - notnull()
        - dropna() dropna存在缺失值则丢弃该行/列。
            - axis={'0':丢掉整列, '1':丢掉整行}
            - how={'any':存在缺失值, 'all':整行/列都是缺失值}
        - fillna() 填写缺失的值
        - isnull() 缺失值用True代替，其他值用False代替
            - np.any() 找到缺失值
Change History:

"""
import pandas as pd
import numpy as np


def isnull_and_notnull():
    # 常用
    # isnull(isna)和notnull(notna)  公司用isnull notnull
    # pandas中不要用is None等来完成比较，可能会存在非常多的情况!
    print(pd.isnull == pd.isna)  # True
    print(pd.notnull == pd.notna)  # True
    # Pands会把np.nan、None以及数据缺失认为为NULL
    print(pd.isnull(np.nan))
    print(pd.isnull(pd.NA))
    print(pd.isnull(pd.NaT))  # 日期空只在pd中定义
    print(pd.isnull(None))

    # 从数据结构加载
    sr = pd.Series(["a", "b", 1, None], dtype="string")
    print(sr)
    print(sr.isnull())

    print(sr[3] is pd.NA)  # True
    # 不要使用 == 判断
    print("na", sr[3] == pd.NA, type(sr[3] == pd.NA))  # na <NA> <class 'pandas._libs.missing.NAType'>
    pd.isnull(sr[3])  # True

    sr2 = pd.Series(["a", "b", 1, None], dtype="str")
    print(sr2)  # dtype object
    print(pd.isnull(sr[3]))  # True
    print(sr2.isnull())  # 依然有效

    sr3 = pd.Series(["a", "b", 1, None], dtype="string")
    print(sr3.isnull())  # None也是可以被isnull识别

    sr4 = pd.Series(["a", "b", 1, None])
    print(sr4)  # dtype object
    sr4 = sr4.convert_dtypes()
    print(sr4)

    sr5 = pd.Series(["a", "b", "c", None])
    print(sr5)  # dtype object
    sr5 = sr5.convert_dtypes()  # 专成了string
    print(type(sr5[3]))  # 类型仍然为缺失值

    # 时间类型
    st1 = pd.Series([pd.to_datetime('2018-09-08'), None], dtype="datetime64[ns]")
    print(st1)
    print(st1.isnull())  # is null也是用于pd.NaT类型

    # 从csv加载数据
    # 读取的时候指定
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv",
                     dtype={"text_content": "str"})
    print(df)
    print(df.isnull())

    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv",
                     dtype={"text_content": "string"})
    print(df)
    print(df.isnull())

    # astype事后转换 string和str存在差异
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv")
    df["text_content"] = df["text_content"].astype("str")
    print(df.isnull())  # astype str会强转
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv")
    df["text_content"] = df["text_content"].astype("string")  # 如果事后再转换类型，会强转字符串类型
    print(df)
    print(df.isnull())  # string会保留null值
    # type(df["text_content"][3])  # pandas._libs.missing.NAType
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv")
    df["text_content"] = df["text_content"].astype("string")  # 在老版本这样用可能会报错。 在老version中要先转“str” 再转string


def parse_nan():
    """处理丢失数据"""
    datas = pd.date_range('20210101', periods=6)
    df = pd.DataFarme(np.arange(24).reshape((6, 4)), index=datas, columns=['A', 'B', 'C', 'D'])

    # 缺失值位置填充NaN
    df.iloc[0, 1] = np.nan
    df.iloc[1, 2] = np.nan

    # dropna
    print(df.dropna(axis=0, how='any'))

    # fillna
    print(df.fillna(value=0))

    # isnull
    print(df.isnull())  # True
    # np.any() 找到缺失值
    print(np.any(df.isnull()) == True)


def main():
    # 学习
    parse_nan()


if __name__ == '__main__':
    main()
