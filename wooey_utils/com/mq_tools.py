import pika

from wooey_utils.com.config import *


def get_mq_ch(exchange_name,queue_name):
    auth = pika.PlainCredentials(MQ_USER, MQ_PWD)
    mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HSOT, port=MQ_PORT, credentials=auth))
    channel = mq_conn.channel()
    channel.exchange_declare(exchange=exchange_name,
                             passive=False,
                             exchange_type='direct',
                             auto_delete=False,
                             durable=True
                             )
    channel.queue_declare(queue=queue_name,
                          passive=False,  # 检查队列是否存在,如果不存在ChannelClosed
                          durable=True,  # 队列持久化参数，默认不持久化
                          auto_delete=False,  # 当最后一个消费者退订后自动删除，默认不开启
                          exclusive=False,  # 设置独享队列，该队列只被当前的connection使用，如果该tcp关闭了，队列会被删除
                          )
    channel.queue_bind(queue_name, exchange_name)
    return channel