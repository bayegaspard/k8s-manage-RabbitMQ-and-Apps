# producer.py
# This script will publish MQ message to my_exchange MQ exchange

import pika
import random


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'bitnami')))
channel = connection.channel()


import random
for x in range(20):
    val = random.randrange(2,60,2)
    if val > 30 :
      #  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'bitnami')))
       # channel = connection.channel()

        channel.basic_publish(exchange='my-exchange', routing_key='test', body='Test')

#        connection.close()
    elif val < 30:
       # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'bi>
        #channel = connection.channel()

        channel.basic_publish(exchange='my-exchange', routing_key='test', body='23')

 #       connection.close()
    else:
        print("error")


connection.close()
