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

# Connection helper (avoids timeout)
def get_connection_and_cursor():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="flight_booking"
    )
    return conn, conn.cursor(dictionary=True)

# View all flights
@app.route("/flights", methods=["GET"])
def get_flights():
    conn, cursor = get_connection_and_cursor()
    cursor.execute("SELECT * FROM flights")
    rows = cursor.fetchall()
    conn.close()

    flights = []
    for row in rows:
        flights.append({
            "id": row["id"],
            "flight_number": row["flight_number"],
            "departure_time": str(row["departure_time"]),
            "arrival_time": str(row["arrival_time"]),
            "travel_date": str(row["travel_date"]),
            "source": row["source"],
            "destination": row["destination"]
        })
    return jsonify(flights)

# Add a new flight
@app.route("/add-flight", methods=["POST"])
def add_flight():
    data = request.get_json()
    conn, cursor = get_connection_and_cursor()
    cursor.execute("""
        INSERT INTO flights (flight_number, departure_time, arrival_time, travel_date, source, destination)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["flight_number"], data["departure_time"], data["arrival_time"],
        data["travel_date"], data["source"], data["destination"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Flight added successfully!"})

# Delete a flight
@app.route("/delete-flight/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    conn, cursor = get_connection_and_cursor()
    cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Flight deleted successfully!"})

# View all bookings
@app.route("/bookings", methods=["GET"])
def get_bookings():
    conn, cursor = get_connection_and_cursor()
    cursor.execute("""
        SELECT b.id, b.name, b.email, b.travel_date,
               f.flight_number, f.source, f.destination
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
    """)
    rows = cursor.fetchall()
    conn.close()

    bookings = []
    for row in rows:
        bookings.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "travel_date": str(row["travel_date"]),
            "flight_number": row["flight_number"],
            "source": row["source"],
            "destination": row["destination"]
        })

    return jsonify(bookings)

# Test route
@app.route("/", methods=["GET"])
def home():
    return "Admin API running."

if __name__ == "__main__":
    app.run(debug=True)
