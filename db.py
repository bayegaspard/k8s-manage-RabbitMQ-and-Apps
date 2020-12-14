import psycopg2



def db():
    
    connection = psycopg2.connect(user="postgres",
                                  password="t00r",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO srint_tbl (strg) VALUES (%s)"""
    record_to_insert = ("message")
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into mobile table")

db()
