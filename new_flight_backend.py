from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="flight_booking"
)
cursor = conn.cursor()

# Create flights table
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(20),
    departure_time TIME,
    arrival_time TIME,
    travel_date DATE,
    source VARCHAR(100),
    destination VARCHAR(100)
)
""")

# Create bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    flight_id INT,
    travel_date DATE,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
)
""")
conn.commit()

# Search flights
@app.route("/search-flights", methods=["GET"])
def search_flights():
    source = request.args.get("from")
    destination = request.args.get("to")
    travel_date = request.args.get("date")

    cursor.execute("""
        SELECT * FROM flights WHERE source=%s AND destination=%s AND travel_date=%s
    """, (source, destination, travel_date))
    rows = cursor.fetchall()

    flights = []
    for row in rows:
        flights.append({
            "id": row[0],
            "flight_number": row[1],
            "departure_time": str(row[2]),
            "arrival_time": str(row[3]),
            "travel_date": str(row[4]),
            "source": row[5],
            "destination": row[6]
        })
    return jsonify(flights)

# Book a flight
@app.route("/book", methods=["POST"])
def book_flight():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    source = data.get("from")
    destination = data.get("to")
    travel_date = data.get("date")

    try:
        # Find matching flight
        cursor.execute("""
            SELECT id FROM flights
            WHERE source = %s AND destination = %s AND travel_date = %s
            LIMIT 1
        """, (source, destination, travel_date))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "No matching flight found."}), 404

        flight_id = result[0]

        # Book the flight
        cursor.execute("""
            INSERT INTO bookings (name, email, flight_id, travel_date)
            VALUES (%s, %s, %s, %s)
        """, (name, email, flight_id, travel_date))
        conn.commit()

        return jsonify({"message": "Booking successful!"})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Booking failed."}), 500


@app.route("/", methods=["GET"])
def home():
    return "Flight booking API running."

if __name__ == "__main__":
    app.run(debug=True)