#create table demo (txt varchar);
#insert into demo (txt) values ('Hello from postgres Rabbitmq!!!')

import psycopg2
import pika

import configparser

config = configparser.ConfigParser()
config.read('config.py')

rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')
rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')
rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')
rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')
rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')

pg_host = config.get('postgres', 'pg_host')
pg_port = config.get('postgres', 'pg_port')
pg_user = config.get('postgres', 'pg_user')
pg_password = config.get('postgres', 'pg_password')
pg_database = config.get('postgres', 'pg_database')

def main():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        database=pg_database,
        user=pg_user,
        password=pg_password
    )
    cursor = conn.cursor()

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)

    # Read data from PostgreSQL and write to RabbitMQ
    try:
        cursor.execute("SELECT * FROM demo")
        for row in cursor:
            # Convert row to a string for simplicity
            message = str(row)
            channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
            print("Sent message:", message)
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
        connection.close()

if __name__ == "__main__":
    main()
