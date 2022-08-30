# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 11:02

input: 
output: 
Short Description: 
    - 知识点：
        - read_csv                    to_csv
        - read_excel                  to_excel  (pandas处理excle:行数上限1048576即2**20，列数上限16384即2**14)
        - read_hdf                    to_hdf
        - read_sql                    to_sql
        - read_json                   to_json
        - read_msgpack(experimental)  to_msgpack(experimental)
        - read_html                   to_html
        - read_gbq(experimental)      to_gbq(experimental)
        - read_stata                  to_stata
        - read_sas                    to_sas
        - read_clipboard              to_clipboard
        - read_pickle                 to_pickle
Change History:

"""
import pandas as pd
import numpy as np


def csv_read_to():
    # 常用
    filepath_or_buffer = "可以是文件路径也可以是url"
    filepath_or_buffer = "http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/350_0af71498f139412cb602f67a18371098.csv"
    encoding = "一般使用utf-8，如果是平台的bom格式，使用utf-8-sig"
    index_col = "指定索引列"
    usecols = "一般用来指定列的范围"
    dtype = "用于指定列的数值类型"

    df = pd.read_csv(filepath_or_buffer, encoding='utf-8-sig')
    # df.info()
    df.head(1)

    df = pd.read_csv(filepath_or_buffer, index_col="file_id", encoding='utf-8-sig')
    print(df.loc[18060742])  # loc by index
    # 被设置成index 将不在输出字段内
    print(df.loc[18060742].to_dict())

    df = pd.read_csv(filepath_or_buffer, usecols=["project_id", "lang"], encoding='utf-8-sig')
    print(df.head(1))

    # 扩展dtypes
    # 根据值做可能转换
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv")
    print(df.dtypes)  # 含NaN值的为 object
    df = df.convert_dtypes()
    print(df.dtypes)  # object被转成了string
    df = pd.read_csv("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/string_test.csv",
                     dtype={"flag": str, "text_content": "string"})
    print(df)
    print(df.dtypes)  # 注意text_content是str类型

    # csv存储
    df.to_csv(
        "test_01.csv",
        sep=",",  # 分隔符，默认","
        encoding='utf-8-sig',  # 默认'utf-8'，
        index=False  # 行索引，默认是true, 一般记得要加
    )


def excel_read_to():
    pd.read_excel(
        "路径或者url",
        sheet_name=0,  # "默认是第一个sheet  可以是int,str,list,None None是全部 list和None返回的是字典"
        header=0,  # "默认第一行，列索引 如果没有表头，指定header=None"
        index_col=None,  # '默认没有'
        usecols=None,  # "默认拿出所有的列, 几种方式A:C, A,C [0,2] ['AAA','CCC] lambda i:i=='AAA' "
        skiprows=None,  # 跳过行 skiprows=1跳过的行数，或者 shiprows=[0,2]，
        names=['a', 'b', 'c'],  # header是None的时候，指定names,否则会替换掉第一行的数据。
        dtype={'a': 'str'},  # 注意都是字符串
        parse_dates=False,  # True 尝试解析 [0,1] [[0,1,2]] ['a','b']
        date_parser=None,  # function 日期解析函数 为None的时候会使用内部的解析器解析.
        na_values=None,  # 列表或者集合['a'] 判定为 'NA'
        keep_default_na=True,  # True判定缺失值转为NaN，False原样输出
        converters=None,  # {"a":lambda i:i+1},
        mangle_dupe_cols=True,  # "默认允许重复并且会重命名重复的列 不能设置成False 还不支持"
    )

    excel_df = pd.read_excel("http://appen-pe.oss-cn-shanghai.aliyuncs.com/example_data/pandas_kt/email_update.xlsx")
    print(excel_df.head())
    # 如果要读excel 需要安装 xlrd和xlwt
    df = pd.read_excel("test.xlsx", sheet_name=["Sheet1", "Sheet3"])  # 可以一次获取多个sheet
    print(df)

    # excel存储

    df.to_excel(
        "out_path.xlsx",  # 文件目录名
        sheet_name='Sheet1',  # 子表名
        index=False,
        na_rep=''  # 缺失值的表示方式
    )

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    # 多表写入：如果要讲多个dataframe写入到不同的sheet
    with pd.ExcelWriter("test.xlsx") as wt:
        df1.to_excel(sheet_name="sheet1")
        df2.to_excel(sheet_name="sheet2")
    # 添加新的数据
    df3 = df1.copy()
    with pd.ExcelWriter('output.xlsx', mode="a", engine="openpyxl") as writer:
        df3.to_excel(writer, sheet_name='Sheet_name_3_3_3')


def sql_read_to():
    import psycopg2
    RDS_DATA_DB_HOST = 'host'
    RDS_DATA_DB_USER = '账号'
    RDS_DATA_DB_PSW = '密码'
    RDS_DATA_DB_NAME = '数据库名'
    RDS_DATA_DB_PORT = 'port'
    conn = psycopg2.connect(host=RDS_DATA_DB_HOST, user=RDS_DATA_DB_USER,
                            password=RDS_DATA_DB_PSW, database=RDS_DATA_DB_NAME,
                            port=RDS_DATA_DB_PORT)
    sql = "sql语句"
    df = pd.read_sql(sql, conn)
    conn.close()  # 关闭链接后 不影响df的使用

    # sql存储
    # df.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)
    engine = create_engine(
        f'postgresql+psycopg2://{RDS_DATA_DB_USER}:{RDS_DATA_DB_PSW}@{RDS_DATA_DB_HOST}:{RDS_DATA_DB_PORT}/{RDS_DATA_DB_NAME}',
        poolclass='NullPool',
        connect_args={'connect_timeout': 30}
    )

    df.to_sql('nums', con=engine, index=False, if_exists="append")  # nums是表名，con
    # if_exists 实际的工作中，尽量使用appen 不要使用replace,或者fail
    #  - fail
    #  - append # 不存在会创建新的   # append有事务的作用
    #  - replace # 慎用，会清空原有数据
    #
    # method{None, ‘multi’, callable}, optional
    # Controls the SQL insertion clause used:
    # None : Uses standard SQL INSERT clause (one per row).
    # ‘multi’: Pass multiple values in a single INSERT clause.


def json_read_to():
    # json读取
    pd.read_json(path_or_buf=None, orient=None, typ='frame', dtype=None, convert_axes=None, convert_dates=True,
                 keep_default_dates=True, numpy=False, precise_float=False, date_unit=None, encoding=None,
                 encoding_errors='strict', lines=False, chunksize=None, compression='infer', nrows=None, )

    # orients is:
    # 'split' : dict like {index -> [index], columns -> [columns], data -> [values]}
    '''
    {
        "columns":["col 1","col 2"],
        "index":["row 1","row 2"],
        "data":[["a","b"],["c","d"]]
    }
    '''
    # 'records' : list like [{column -> value}, ... , {column -> value}]
    '''
    [
      {
        "project_id": "531",
        "ss_folder": "Ake_P15924_ARA_EGY_QN377998_20210725-101610",
        "person_id": "QN377998",
        "audio_url": "appen://531_Ake__ARA_EYG/.../xx.wav",
        "audio_type": "SZSJ",
        "lang": "Arabic(Egypt)",
        "valid_duration": 3.986,
        "content_text": "لقد إشتريت ثلاث طائرات وست سفن حربية.",
        "audio_start": "1.548",
        "audio_end": "5.534",
        "pid": 741693,
        "age": 19,
        "gender": "M",
        "submit_date": "20220124",
        "pack_audio_name": "ArabicEgypt_abqfer_M_19_0949.wav",
        "is_pack": 1,
        "pack_path": "/appen-delivery/wooey_rs/ake/1e09bae1ecdd4360b94c762846075c02"
      },
      ...
    ]
    '''
    # records
    df1 = pd.read_json(
        "http://projecteng.oss-cn-shanghai.aliyuncs.com/0_ProjectData/data_bak/0f207f4f16e34c4caf7b576ab8e535b7.json")
    df1.head(1)
    # 'index' : dict like {index -> {column -> value}}
    '''
    { 
        "row 1":{"col 1":"a","col 2":"b"},
        "row 2":{"col 1":"c","col 2":"d"}
    }
    '''
    # 'columns' : dict like {column -> {index -> value}}
    # 'values' : just the values array

    # json存储
    pd.to_json(path_or_buf=None, orient=None, date_format=None, double_precision=10, force_ascii=True, date_unit='ms', default_handler=None, lines=False, compression='infer', index=True, indent=None, storage_options=None)
    df = pd.DataFrame(
        [["a", "b"], ["c", "d"]],
        index=["row 1", "row 2"],
        columns=["col 1", "col 2"],
    )
    print(df)
    print(df.to_json(orient="split"))  # {"columns":["col 1","col 2"],"index":["row 1","row 2"],"data":[["a","b"],["c","d"]]}
    print(df.to_json(orient="records"))  # [{"col 1":"a","col 2":"b"},{"col 1":"c","col 2":"d"}]
    print(df.to_json(orient="index"))  # {"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}
    print(df.to_json(orient="columns"))  # {"col 1":{"row 1":"a","row 2":"c"},"col 2":{"row 1":"b","row 2":"d"}}
    print(df.to_json(orient="values"))  # [["a","b"],["c","d"]]
    print(df.to_json(
        orient="table"))  # {"schema":{"fields":[{"name":"index","type":"string"},{"name":"col 1","type":"string"},{"name":"col 2","type":"string"}],"primaryKey":["index"],"pandas_version":"0.20.0"},"data":[{"index":"row 1","col 1":"a","col 2":"b"},{"index":"row 2","col 1":"c","col 2":"d"}]}

    # json_normalize: json平铺为df
    data = [
        {"id": 1, "name": {"first": "Coleen", "last": "Volk"}},
        {"name": {"given": "Mark", "family": "Regner"}},
        {"id": 2, "name": "Faye Raker"},
    ]
    # 会自动创建每个字段， 内层的字段通过.拼接
    print(pd.json_normalize(data))

    data = [
        {
            "id": 1,
            "name": "Cole Volk",
            "fitness": {"height": 130, "weight": 60},
        },
        {"name": "Mark Reg", "fitness": {"height": 130, "weight": 60}},
        {
            "id": 2,
            "name": "Faye Raker",
            "fitness": {"height": 130, "weight": 60},
        },
    ]
    # max_level如果是0 那么解析第一层
    print(pd.json_normalize(data, max_level=0))

    data = [{"A": [[1, 2], [3, 4]]}]
    pd.json_normalize(data, "A", record_prefix="Prefix.")


def table_read_to():
    # table读取
    df = pd.read_table("test.txt", names=["col1", "col2"], sep=' ')


def html_read_to():
    # 网页表格很多 : 可以添加参数attrs根据id或者classname获取
    dfs = pd.read_html('https://www.gairuo.com/p/pandas-io', attrs={'id': 'table'})


def main():
    pass


if __name__ == '__main__':
    main()
