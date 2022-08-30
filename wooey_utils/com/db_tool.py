# from oneutils import local_ip_if_linux,Dbclass

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.pool import NullPool
import psycopg2
from wooey_utils.com.config import *



class Dbclass():
    def __init__(self, db_setting, dbname):
        self.db_setting = db_setting
        self.dbname = dbname
        self.tunnel, self._db = self.initdb()

    def initdb(self):
        engine = create_engine(
            f'postgresql+psycopg2://{self.db_setting["user"]}:{self.db_setting["pwd"]}@{self.db_setting["host"]}:{self.db_setting["port"]}/{self.dbname}',
            poolclass=NullPool,
            connect_args={'connect_timeout': 30})
        Session = sessionmaker(bind=engine)
        session = Session()
        return None, session

    def db_insert(self, sql, data):
        try:
            # data是字典列表数组
            result = self._db.execute(text(sql), data)


        except Exception as e:
            self._db.rollback()
            print(e)
            raise Exception('db_insert FAILED')
        else:
            self._db.commit()
            return result


    def db_del(self, sql):
        try:
            self._db.execute(sql)
        except BaseException:
            raise Exception('db_del FAILED')
        else:
            self._db.commit()

    def db_query(self, sql):
        try:
            result = self._db.execute(sql).fetchall()
            return result
        except BaseException as e:
            print("error msg:", e)
            raise Exception('db_query FAILED')

    def db_execute(self, sql, msg):

        try:
            result = self._db.execute(sql)
        except BaseException:
            # print(sql)
            raise Exception('db_excute FAILED')
        else:
            self._db.commit()
            return result

    def db_execute_return_id(self, sql, msg):

        try:
            result = self._db.execute(sql).fetchall()
        except BaseException:
            # print(sql)
            raise Exception('db_excute FAILED')
        else:
            self._db.commit()
            return result


    def close(self):

        self._db.close()
        if self.tunnel is not None:
            self.tunnel.close()



### 不要在循环中使用
def get_data_db_conn():
    conn = psycopg2.connect(host=RDS_DATA_DB_HOST, user=RDS_DATA_DB_USER,
                            password=RDS_DATA_DB_PSW, database=RDS_DATA_DB_NAME,
                                port=RDS_DATA_DB_PORT)
    return conn

def get_con_eng():
    engine = create_engine(
        f'postgresql+psycopg2://{RDS_DATA_DB_USER}:{RDS_DATA_DB_PSW}@{RDS_DATA_DB_HOST}:{RDS_DATA_DB_PORT}/{RDS_DATA_DB_NAME}',
        poolclass=NullPool,
        connect_args={'connect_timeout': 30}
    )
    con = engine.connect()
    return con



def get_data_db():
    db_setting = {"host": RDS_DATA_DB_HOST, "user": RDS_DATA_DB_USER, "pwd": RDS_DATA_DB_PSW,"port":RDS_DATA_DB_PORT}
    db = Dbclass(db_setting, dbname=RDS_DATA_DB_NAME)
    return db

