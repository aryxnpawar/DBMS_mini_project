-- Create the database
CREATE DATABASE IF NOT EXISTS flight_booking;

-- Use the database
USE flight_booking;

-- Create the flights table
CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(20) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    travel_date DATE NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL
);

-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    flight_id INT NOT NULL,
    travel_date DATE NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO flights (flight_number, departure_time, arrival_time, travel_date, source, destination)
VALUES
('AI101', '08:00:00', '10:00:00', '2025-04-12', 'Delhi', 'Mumbai'),
('AI102', '14:30:00', '16:30:00', '2025-04-12', 'Delhi', 'Bangalore'),
('AI103', '09:00:00', '11:00:00', '2025-04-13', 'Mumbai', 'Chennai');
