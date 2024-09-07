from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Replace with your actual database connection parameters
db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "arul",
    "password": "pass"
}

def fetch_vehicle_data():
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vehicles")
            data = cur.fetchall()
            return data

@app.route('/')
def index():
    vehicle_data = fetch_vehicle_data()
    return render_template('read.html', data=vehicle_data)

if __name__ == '__main__':
    app.run(debug=True)
