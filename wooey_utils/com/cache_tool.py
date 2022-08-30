import redis
from wooey_utils.com.config import *

def get_redis_conn():
    redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return redis_conn


# def get_mq_conn():
#     auth = pika.PlainCredentials(MQ_USER, MQ_PWD)
#     mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HSOT,port=MQ_PORT,credentials=auth))
#     return mq_conn
