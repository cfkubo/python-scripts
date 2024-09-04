#curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from the API"}' http://localhost:5000/post_message
#curl http://localhost:5000/get_messages

import pika
from flask import Flask, request, jsonify
import configparser

config = configparser.ConfigParser()
config.read('config.py')

rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')
rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')
rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')
rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')
rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')

# Flask app
app = Flask(__name__)

def connect_to_rabbitmq():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    return channel

@app.route('/post_message', methods=['POST'])
def post_message():
    data = request.get_json()
    message = data.get('message')
    if message:
        channel = connect_to_rabbitmq()
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
        return jsonify({'message': 'Message sent successfully'})
    else:
        return jsonify({'error': 'Message not provided'})

# @app.route('/get_messages', methods=['GET'])
# def get_messages():
#     # Assuming you want to read all messages from the queue
#     channel = connect_to_rabbitmq()
#     while True:
#         method, properties, body = channel.basic_get(queue=rabbitmq_queue)
#         if body is None:
#             break
#         message = body.decode('utf-8')
#         # Process the message (e.g., save to a database, return in a response)
#         print(message)
#     return jsonify({'message': 'Messages retrieved'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    channel = connect_to_rabbitmq()
    messages = []
    while True:
        method, properties, body = channel.basic_get(queue=rabbitmq_queue)
        if body is None:
            break
        message = body.decode('utf-8')
        messages.append(message)
        # Print the message to the console
        print(f"Received message: {message}")
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
