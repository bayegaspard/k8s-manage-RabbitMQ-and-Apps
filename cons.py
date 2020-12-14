                                              
# consumer.py
# Consume RabbitMQ queue

import pika
import psycopg2
from psycopg2.extras import Json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "bitnami")))
channel = connection.channel()

messages = []



def db():
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="t00r",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO srint_tbl (strg) VALUES (%s)"""
        record_to_insert = (message)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)

    finally:
           #closing database connection.
        if(connection):
             cursor.close()
             connection.close()
             print("PostgreSQL connection is closed")







def db2():
  try:
   connection = psycopg2.connect(user="postgres",
                                  password="t00r",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
   cursor = connection.cursor()

   postgres_insert_query = """ INSERT INTO int_tbl (int_v) VALUES (%s)"""
   record_to_insert = (message)
   cursor.execute(postgres_insert_query, record_to_insert)

   connection.commit()
   count = cursor.rowcount
   print (count, "Record inserted successfully into mobile table")
except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()





def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    print(f'{body} is received')
#    messages = []
    messages.append(body)
    print(messages)

    for message in messages:
       #print(message)
       if message==23:
           print("int")
           db2()
           
       elif message == "Test":
           print ("string")
           db()
       else:
           print("error")






channel.basic_consume(queue="my-app", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
