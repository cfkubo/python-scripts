import pika
import json
import configparser
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from flask import Flask, render_template

app = Flask(__name__)

# Load configuration from a file (optional)
config = configparser.ConfigParser()
config.read('config.py')
rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')  # Handle potential errors
rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')  # Handle potential errors
rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')  # Handle potential errors
rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')  # Handle potential errors
rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')  # Handle potential errors

# Replace with your actual database connection parameters
db_config = {
    "host": '127.0.0.1',
    "port": '5432',
    "database": "postgres",
    "user": "arul",
    "password": "pass"
}

def load_json_data(json_data, table_name, db_config):
    """
    Loads JSON data into a PostgreSQL table.

    Args:
        json_data (dict): The JSON data to load.
        table_name (str): The name of the table.
        db_config (dict): A dictionary containing database connection parameters.
    """

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            # Extract values from JSON data
            make = json_data['make']
            model = json_data['model']
            gps_location = json_data['gps-location'].split(',')
            mileage = json_data['mileage']
            fuel_level = json_data['fuel_level']
            temperature = json_data['temperature']
            serviced_date = json_data['serviced_date']
            next_service_date = json_data['next_service_date']
            vehicle_alerts = json_data['vehicle_alerts']

            #latitude, longitude  = gps-location
            # print(gps_location)
            gps_location_str = ''.join(gps_location)
            # print(gps_location_str)
            latitude, longitude  = gps_location_str.split(' ')
            # data_without_brackets = vehicle_alerts[1:-1]

            # print(latitude,longitude)
            # print(data_without_brackets)

            # Insert data into the table
            cur.execute(
                f"""
                INSERT INTO vehicles (make, model, latitude, longitude, mileage, fuel_level, temperature, serviced_date, next_service_date, vehicle_alerts)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (make, model, latitude, longitude , mileage, fuel_level, temperature, serviced_date, next_service_date, vehicle_alerts)
            )

            # print(query % (make, model, latitude, longitude , mileage, fuel_level, temperature, serviced_date, next_service_date, vehicle_alerts))

            conn.commit()
            print("Data inserted successfully!")

def consume_from_rabbitmq(queue_name):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        json_data = json.loads(body)
        # print(json.dumps(json_data, indent=4))
        load_json_data(json_data, "vehicles", db_config)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()

@app.route('/')
def index():
    return render_template('postgres.html')

if __name__ == '__main__':
    consume_from_rabbitmq(rabbitmq_queue)
    app.run(debug=True)


# CREATE TABLE vehicles (
#     id SERIAL PRIMARY KEY,
#     make VARCHAR(255) NOT NULL,
#     model VARCHAR(255) NOT NULL,
#     latitude VARCHAR(255) NOT NULL,
#     longitude VARCHAR(255) NOT NULL,
#     mileage INTEGER NOT NULL,
#     fuel_level VARCHAR(255) NOT NULL,
#     temperature VARCHAR(255) NOT NULL,
#     serviced_date DATE NOT NULL,
#     next_service_date DATE,
#     vehicle_alerts VARCHAR(255)[]
# );
