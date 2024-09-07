import json
import random
import time
import datetime
from geopy.distance import distance
from geopy.geocoders import Nominatim
import pika
import configparser
from faker import Faker
from json import dumps


config = configparser.ConfigParser()
config.read('config.py')

rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')
rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')
rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')
rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')
rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')

def generate_random_car():
    fake = Faker()

    return {
        'make': fake.company(),
        'model': fake.word(),
        'gps-location': f'{random.uniform(31.7946, 42.7946)}, {random.uniform(-38.7946, -146.5348)}',
        #'gps-location': f'{fake.latitude()},{fake.longitude()}',  # Latitude,Longitude format
        'mileage': random.randint(0, 200000),
        'fuel_level': round(random.uniform(10, 70), 2),  # Percentage
        'temperature': round(random.uniform(-40, 125), 2),  # Celsius
        'serviced_date': fake.date_between(start_date='-10y', end_date='-1d').isoformat(),  # Past date within 1 year
        'next_service_date': fake.date_between(start_date='+1d', end_date='+5d').isoformat(),  # Future date within 1 year
                             # if random.random() < 0.1 else None),  # 10% chance of no next service date
        'vehicle_alerts': random.choices(['Engine Light On', 'Low Tire Pressure', None], weights=[0.05, 0.1, 0.85])  # Random alerts
    }

# dumps(datetime.now(), default=json_serial)
# Connect to RabbitMQ
# Connect to RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue,durable=True,arguments={"x-queue-type": "quorum"})
# channel.queue_declare(queue=rabbitmq_queue)
# channel.queue_declare(queue='vehicle_data')

# Main loop to generate and send car data
while True:
    car_data = generate_random_car()
    channel.basic_publish(exchange='',
                         routing_key=rabbitmq_queue,
                         body=json.dumps(car_data))
    print("Sent:", json.dumps(car_data))

    time.sleep(3)  # Simulate sensor readings every minute

# Close the connection
connection.close()

# import csv
# import random
# from faker import Faker
#
#
# # fake = Faker()
#
# # def generate_random_car():
# #     return {
# #         'make': fake.company(),
# #         'model': fake.word(),
# #         'gps-location': f'{fake.latitude()},{fake.longitude()}',  # Latitude,Longitude format
# #         'mileage': random.randint(0, 200000),
# #         'fuel_level': round(random.uniform(10, 70), 2),  # Percentage
# #         'temperature': round(random.uniform(-40, 125), 2)  # Celsius
# #     }
#
# def generate_random_car():
#     fake = Faker()
#
#     return {
#         'make': fake.company(),
#         'model': fake.word(),
#         'gps-location': f'{fake.latitude()},{fake.longitude()}',  # Latitude,Longitude format
#         'mileage': random.randint(0, 200000),
#         'fuel_level': round(random.uniform(10, 70), 2),  # Percentage
#         'temperature': round(random.uniform(-40, 125), 2),  # Celsius
#         'last_service_date' : fake.generate_date(past=True),  #'last_service_date': fake.past_date(days=365, tzinfo=None),  # Past date within 1 year
#         'next_service_date': (fake.future_date(past=False)  # Future date within 1 year
#                              if random.random() < 0.1 else None),  # 10% chance of no next service date
#         'alerts': random.choices(['Engine Light On', 'Low Tire Pressure', None], weights=[0.05, 0.1, 0.85])  # Random alerts
#     }
#
# def generate_random_cars(num):
#     return [generate_random_car() for _ in range(num)]
#
# def write_to_csv(data, filename='cars.csv'):
#     with open(filename, 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
#
# # Generate 100 random cars and write to CSV
# cars = generate_random_cars(100)
# write_to_csv(cars)



# import json
# import random
# import time
# import datetime
# from geopy.distance import distance
# from geopy.geocoders import Nominatim
# import pika
# import configparser
# from geopy.distance import geodesic
#
#
#
# config = configparser.ConfigParser()
# config.read('config.py')
#
# rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')
# rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')
# rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')
# rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')
# rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')
#
# geolocator = Nominatim(user_agent="vechile-data-generator")  # Replace with your app name
#
# # Define vehicle models and initial locations
# vehicle_models = ["Model A", "Model B", "Model C"]
# initial_locations = [
#     "New York, NY",
#     "Los Angeles, CA",
#     "Chicago, IL",
#     "Houston, TX",
#     "Phoenix, AZ"
# ]
#
# # Define data generation ranges
# temperature_range = (50, 90)  # Adjust temperature range as needed
# fuel_level_range = (10, 100)  # Adjust fuel level range as needed
# mileage_range = (0, 100000)  # Adjust mileage range as needed
# distance_km = random.randint(10, 100)
# current_location = random.uniform(-90, 90)
# bearing = (0, 88)
# # Function to generate a random GPS location within a specified distance
# # def generate_random_location(current_location, distance_km):
# #     lat, lon = current_location
# #     bearing = random.randint(0, 360)
# #     new_lat, new_lon = destination_point(lat, lon, distance_km, bearing)
# #     return new_lat, new_lon
# new_location = geodesic(kilometers=distance_km).destination(current_location, bearing=bearing)
#
# def generate_random_location(current_location, distance_km):
#     lat, lon = current_location
#     bearing = random.randint(0, 360)
#     new_location = geodesic(kilometers=distance_km, bearing=bearing, degrees=True).destination(current_location)
#     return new_location.latitude, new_location.longitude
#
# # Function to calculate the distance between two GPS points
# def calculate_distance(point1, point2):
#     return distance(point1, point2).km
#
# # Function to determine if a maintenance alert should be triggered
# def trigger_maintenance_alert(mileage, last_service_mileage):
#     return mileage - last_service_mileage >= 10000  # Adjust mileage threshold as needed
#
# # Connect to RabbitMQ
# # Connect to RabbitMQ
# credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
# )
# channel = connection.channel()
# channel.queue_declare(queue=rabbitmq_queue)
# # channel.queue_declare(queue='vehicle_data')
#
# # Create initial vehicle data
# vehicles = []
# for model in vehicle_models:
#     initial_location = random.choice(initial_locations)
#     vehicles.append({
#         "model": model,
#         "gps_location": geolocator.geocode(initial_location),
#         "temperature": random.randint(*temperature_range),
#         "fuel_level": random.randint(*fuel_level_range),
#         "maintenance_alerts": False,
#         "mileage": 0,
#         "next_service_date": datetime.datetime.now() + datetime.timedelta(days=365)
#     })
#
# # Main loop to generate and send sensor data
# while True:
#     for vehicle in vehicles:
#         current_location = vehicle["gps_location"]
#         new_location = generate_random_location(current_location, random.randint(10, 100))
#         vehicle["gps_location"] = new_location
#         vehicle["temperature"] = random.randint(*temperature_range)
#         vehicle["fuel_level"] = random.randint(*fuel_level_range)
#         vehicle["mileage"] += calculate_distance(current_location, new_location)
#         vehicle["maintenance_alerts"] = trigger_maintenance_alert(vehicle["mileage"],
#                                                                  vehicle["next_service_date"].timestamp())
#         if vehicle["maintenance_alerts"]:
#             vehicle["next_service_date"] += datetime.timedelta(days=365)
#
#         # Create a JSON object
#         vehicle_data = {
#             "model": vehicle["model"],
#             "gps_location": str(vehicle["gps_location"]),
#             "temperature": vehicle["temperature"],
#             "fuel_level": vehicle["fuel_level"],
#             "maintenance_alerts": vehicle["maintenance_alerts"],
#             "mileage": vehicle["mileage"],
#             "next_service_date": vehicle["next_service_date"].strftime("%Y-%m-%d")
#         }
#
#         # Publish the JSON data to RabbitMQ
#         channel.basic_publish(exchange='',
#                              routing_key='vehicle_data',
#                              body=json.dumps(vehicle_data))
#         print("Sent:", json.dumps(vehicle_data))
#
#     time.sleep(60)  # Simulate sensor readings every minute
#
# # Close the connection
# connection.close()

# import random
# import time
# import datetime
# from geopy.distance import distance
# from geopy.geocoders import Nominatim
#
# geolocator = Nominatim(user_agent="vechile-data-generator")  # Replace with your app name
#
# # Define vehicle models and initial locations
# vehicle_models = ["Model A", "Model B", "Model C"]
# initial_locations = [
#     "New York, NY",
#     "Los Angeles, CA",
#     "Chicago, IL",
#     "Houston, TX",
#     "Phoenix, AZ"
# ]
#
# # Define data generation ranges
# temperature_range = (50, 90)  # Adjust temperature range as needed
# fuel_level_range = (10, 100)  # Adjust fuel level range as needed
# mileage_range = (0, 100000)  # Adjust mileage range as needed
#
# # Function to generate a random GPS location within a specified distance
# def generate_random_location(current_location, distance_km):
#     lat, lon = current_location
#     bearing = random.randint(0, 360)
#     new_lat, new_lon = destination_point(lat, lon, distance_km, bearing)
#     return new_lat, new_lon
#
# # Function to calculate the distance between two GPS points
# def calculate_distance(point1, point2):
#     return distance(point1, point2).km
#
# # Function to determine if a maintenance alert should be triggered
# def trigger_maintenance_alert(mileage, last_service_mileage):
#     return mileage - last_service_mileage >= 10000  # Adjust mileage threshold as needed
#
# # Create initial vehicle data
# vehicles = []
# for model in vehicle_models:
#     initial_location = random.choice(initial_locations)
#     vehicles.append({
#         "model": model,
#         "gps_location": geolocator.geocode(initial_location),
#         "temperature": random.randint(*temperature_range),
#         "fuel_level": random.randint(*fuel_level_range),
#         "maintenance_alerts": False,
#         "mileage": 0,
#         "next_service_date": datetime.datetime.now() + datetime.timedelta(days=365)
#     })
#
# # Main loop to generate and print data
# while True:
#     for vehicle in vehicles:
#         current_location = vehicle["gps_location"]
#         new_location = generate_random_location(current_location, random.randint(10, 100))
#         vehicle["gps_location"] = new_location
#         vehicle["temperature"] = random.randint(*temperature_range)
#         vehicle["fuel_level"] = random.randint(*fuel_level_range)
#         vehicle["mileage"] += calculate_distance(current_location, new_location)
#         vehicle["maintenance_alerts"] = trigger_maintenance_alert(vehicle["mileage"],
#                                                                  vehicle["next_service_date"].timestamp())
#         if vehicle["maintenance_alerts"]:
#             vehicle["next_service_date"] += datetime.timedelta(days=365)
#
#         # Create a JSON object
#         vehicle_data = {
#             "model": vehicle["model"],
#             "gps_location": str(vehicle["gps_location"]),
#             "temperature": vehicle["temperature"],
#             "fuel_level": vehicle["fuel_level"],
#             "maintenance_alerts": vehicle["maintenance_alerts"],
#             "mileage": vehicle["mileage"],
#             "next_service_date": vehicle["next_service_date"].strftime("%Y-%m-%d")
#         }
#
#         # Print the JSON data
#         print(json.dumps(vehicle_data, indent=4))
#
#     time.sleep(60)  # Simulate sensor readings every minute
#
#
# # import pika
# # import random
# # import time
# # import datetime
# # import configparser
# #
# # config = configparser.ConfigParser()
# # config.read('config.py')
# #
# # rabbitmq_host = config.get('rabbitmq', 'rabbitmq_host')
# # rabbitmq_port = config.get('rabbitmq', 'rabbitmq_port')
# # rabbitmq_user = config.get('rabbitmq', 'rabbitmq_user')
# # rabbitmq_password = config.get('rabbitmq', 'rabbitmq_password')
# # rabbitmq_queue = config.get('rabbitmq', 'rabbitmq_queue')
# #
# # # Vehicle data generation
# # def generate_vehicle_data():
# #     name = random.choice(["Car", "Truck", "Motorcycle", "SUV", "Van"])
# #     gps_location = (random.uniform(-90, 90), random.uniform(-180, 180))
# #     mileage = random.randint(0, 100000)
# #     fuel_level = random.randint(0, 100)
# #     temperature = random.randint(0, 100)
# #     serviced_date = datetime.datetime.now().strftime("%Y-%m-%d")
# #     next_service_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d")
# #     color = random.choice(["Red", "Blue", "Green", "Black", "White"])
# #     maintenance_alerts = random.choice([True, False])
# #
# #     return {
# #         "name": name,
# #         "gps_location": gps_location,
# #         "mileage": mileage,
# #         "fuel_level": fuel_level,
# #         "temperature": temperature,
# #         "serviced_date": serviced_date,
# #         "next_service_date": next_service_date,
# #         "color": color,
# #         "maintenance_alerts": maintenance_alerts
# #     }
# #
# # def main():
# #     # Connect to RabbitMQ
# #     credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
# #     connection = pika.BlockingConnection(
# #         pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
# #     )
# #     channel = connection.channel()
# #     channel.queue_declare(queue=rabbitmq_queue)
# #
# #     while True:
# #         vehicle_data = generate_vehicle_data()
# #         channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=str(vehicle_data))
# #         print("Sent vehicle data:", vehicle_data)
# #         time.sleep(5)  # Adjust the interval as needed
# #
# #     connection.close()
# #
# # if __name__ == "__main__":
# #     main()
