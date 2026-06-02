import sqlite3
conn = sqlite3.connect('Airport')

conn.execute("DROP TABLE IF EXISTS pilots")
conn.execute("DROP TABLE IF EXISTS Flights")
conn.execute("DROP TABLE IF EXISTS Destinations")

conn.execute("""
CREATE TABLE Pilots (
    Employee_ID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    LicenceNumber TEXT UNIQUE NOT NULL,
    DoB DATE NOT NULL
)
""")

conn.execute("""
CREATE TABLE Destinations (
    CityCode TEXT NOT NULL,
    Airport TEXT NOT NULL,
    City TEXT NOT NULL,

    PRIMARY KEY (CityCode, Airport)
)
""")

conn.execute("""
CREATE TABLE Flights (
Flight_No INTEGER PRIMARY KEY,
Time TEXT NOT NULL,
Date DATE NOT NULL,

Pilot_ID INTEGER,
CityCode TEXT NOT NULL,
Airport TEXT NOT NULL,

FOREIGN KEY (Pilot_ID)
REFERENCES Pilots(Employee_ID)
ON DELETE SET NULL
ON UPDATE CASCADE,

FOREIGN KEY (CityCode, Airport)
REFERENCES Destinations(CityCode, Airport)
)
""")

#Populate the tables with sample data#

conn.execute("""INSERT INTO Pilots VALUES
(1, 'John', 'Miller', 'LIC1001', '1985-04-12'),
(2, 'Anna', 'Peterson', 'LIC1002', '1990-09-23'),
(3, 'Mark', 'Johnson', 'LIC1003', '1982-01-15'),
(4, 'Elena', 'Ivanova', 'LIC1004', '1995-07-30'),
(5, 'David', 'Brown', 'LIC1005', '1988-11-05'),
(6, 'Sarah', 'Wilson', 'LIC1006', '1992-03-19'),
(7, 'Michael', 'Clark', 'LIC1007', '1981-08-14'),
(8, 'Olivia', 'Taylor', 'LIC1008', '1994-12-01'),
(9, 'Daniel', 'Anderson', 'LIC1009', '1987-06-28'),
(10, 'Sophia', 'Thomas', 'LIC1010', '1991-10-17'),
(11, 'James', 'White', 'LIC1011', '1983-02-11'),
(12, 'Emma', 'Harris', 'LIC1012', '1996-04-25'),
(13, 'Lucas', 'Martin', 'LIC1013', '1989-09-09'),
(14, 'Mia', 'Garcia', 'LIC1014', '1993-05-13'),
(15, 'Ethan', 'Moore', 'LIC1015', '1986-07-21');""")


conn.execute("""INSERT INTO Destinations VALUES
('NYC', 'JFK', 'New York'),
('LON', 'LHR', 'London'),
('PAR', 'CDG', 'Paris'),
('ROM', 'FCO', 'Rome'),
('BER', 'BER', 'Berlin'),
('MAD', 'MAD', 'Madrid'),
('AMS', 'AMS', 'Amsterdam'),
('DXB', 'DXB', 'Dubai'),
('TYO', 'HND', 'Tokyo'),
('SYD', 'SYD', 'Sydney'),
('IST', 'IST', 'Istanbul'),
('CHI', 'ORD', 'Chicago'),
('TOR', 'YYZ', 'Toronto'),
('SIN', 'SIN', 'Singapore'),
('LAX', 'LAX', 'Los Angeles');""")


conn.execute("""INSERT INTO Flights VALUES
(1001, '08:30', '2026-05-20', 1, 'NYC', 'JFK'),
(1002, '12:15', '2026-05-20', 2, 'LON', 'LHR'),
(1003, '15:45', '2026-05-21', 3, 'PAR', 'CDG'),
(1004, '09:10', '2026-05-22', 4, 'ROM', 'FCO'),
(1005, '18:00', '2026-05-22', 5, 'BER', 'BER'),
(1006, '07:20', '2026-05-23', 6, 'MAD', 'MAD'),
(1007, '13:50', '2026-05-23', 7, 'AMS', 'AMS'),
(1008, '22:10', '2026-05-24', 8, 'DXB', 'DXB'),
(1009, '11:40', '2026-05-24', 2, 'TYO', 'HND'),
(1010, '16:30', '2026-05-25', 10, 'SYD', 'SYD'),
(1011, '05:55', '2026-05-25', 11, 'IST', 'IST'),
(1012, '14:25', '2026-05-26', 12, 'CHI', 'ORD'),
(1013, '19:15', '2026-05-26', 13, 'TOR', 'YYZ'),
(1014, '10:05', '2026-05-27', 14, 'SIN', 'SIN'),
(1015, '21:45', '2026-05-27', 15, 'LAX', 'LAX');""")

conn.commit()

cursor = conn.execute("SELECT * FROM Pilots")
for row in cursor.fetchall():
    print(row)

#Select flight information based on different criteria#
print("\nFlights departing from New York:")
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, p.FirstName || ' ' || p.LastName AS PilotName, d.City, d.Airport
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE d.City = 'New York'""")
for row in cursor.fetchall():
    print(row)


print("\nFlights piloted by Michael Clark:")
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, p.FirstName || ' ' || p.LastName AS PilotName, d.City, d.Airport
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE p.FirstName = 'Michael' AND p.LastName = 'Clark'""")
for row in cursor.fetchall():
    print(row)


print("\nFlights departing from 2026-05-20 to 2026-05-27:")
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, d.City, d.Airport
                         FROM Flights f
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE f.Date BETWEEN '2026-05-20' AND '2026-05-27'""")
for row in cursor.fetchall():
    print(row)


#Schedule modification#
print("\nChanging departure time for flight 1003:")
cursor =conn.execute("UPDATE Flights SET Time = '16:00' WHERE Flight_No = 1003")
conn.commit()
cursor = conn.execute("SELECT * FROM Flights WHERE Flight_No = 1003")
for row in cursor.fetchall():
    print(row)


print("\nChanging destination for flight 1005:")
cursor = conn.execute("SELECT * FROM Flights WHERE Flight_No = 1005")
for row in cursor.fetchall():
    print(row)
cursor = conn.execute("UPDATE Flights SET CityCode = 'LON', Airport = 'LHR' WHERE Flight_No = 1005")
conn.commit()
cursor = conn.execute("SELECT * FROM Flights WHERE Flight_No = 1005")
for row in cursor.fetchall():
    print(row)


#Pilot assignment#
print("\nAssigning pilot Sarah Wilson to flight 1005:")
cursor = conn.execute("""SELECT * FROM Flights  JOIN Pilots p ON Flights.Pilot_ID = p.Employee_ID
                       WHERE Flight_No = 1005""")
for row in cursor.fetchall():
    print(row)
cursor = conn.execute("UPDATE Flights SET Pilot_ID = 6 WHERE Flight_No = 1005")
conn.commit()
cursor = conn.execute("""SELECT * FROM Flights JOIN Pilots p ON Flights.Pilot_ID = p.Employee_ID 
                       WHERE Flight_No = 1005""")
for row in cursor.fetchall():
    print(row)


print("\nAssign Mark Johnson to all flights going to London:")
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, p.FirstName || ' ' || p.LastName AS PilotName, d.City, d.Airport
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE d.City = 'London'""")
for row in cursor.fetchall():
    print(row)

cursor = conn.execute("""UPDATE Flights SET Pilot_ID = (SELECT Employee_ID FROM Pilots WHERE FirstName = 'Mark' AND LastName = 'Johnson')
                         WHERE Flight_No IN (SELECT f.Flight_No
                         FROM Flights f
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE d.City = 'London')""")
conn.commit()
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, p.FirstName || ' ' || p.LastName AS PilotName, d.City, d.Airport
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE d.City = 'London'""")
for row in cursor.fetchall():
    print(row)


print("\nGet the schedule for pilot Anna Peterson:")
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, d.City, d.Airport
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE p.FirstName = 'Anna' AND p.LastName = 'Peterson'""")
for row in cursor.fetchall():
    print(row)


#Destination management#
print("\nAdding new destination: Barcelona (BCN):")
cursor = conn.execute("SELECT * FROM Destinations")
for row in cursor.fetchall():
    print(row)
cursor = conn.execute("INSERT INTO Destinations VALUES ('BCN', 'BCN', 'Barcelona')")
conn.commit()
cursor = conn.execute("SELECT * FROM Destinations")
for row in cursor.fetchall():
    print(row)


print("\nUpdating airport code for Tokyo:")
cursor = conn.execute("SELECT * FROM Destinations WHERE City = 'Tokyo'")
for row in cursor.fetchall():
    print(row)
cursor = conn.execute("UPDATE Destinations SET Airport = 'NRT' WHERE City = 'Tokyo'")
conn.commit()
cursor = conn.execute("SELECT * FROM Destinations WHERE City = 'Tokyo'")
for row in cursor.fetchall():
    print(row)

print("\nUpdate destination for flight 1001:");
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, d.City, d.Airport
                         FROM Flights f
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE f.Flight_No = 1001""")
for row in cursor.fetchall():
    print(row)
cursor = conn.execute("UPDATE Flights SET CityCode = 'LAX', Airport = 'LAX' WHERE Flight_No = 1001")
conn.commit()
cursor = conn.execute("""SELECT f.Flight_No, f.Time, f.Date, d.City, d.Airport
                         FROM Flights f
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         WHERE f.Flight_No = 1001""")
for row in cursor.fetchall():
    print(row)


#Data summary#
print("\nNumber of flights per destination:")
cursor = conn.execute("""SELECT d.City, COUNT(*) AS FlightCount
                         FROM Flights f
                         JOIN Destinations d ON f.CityCode = d.CityCode AND f.Airport = d.Airport
                         GROUP BY d.City""")
for row in cursor.fetchall():
    print(row)


print("\nNumber of flights per pilot:")
cursor = conn.execute("""SELECT p.FirstName || ' ' || p.LastName AS PilotName, COUNT(*) AS FlightCount
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         GROUP BY p.Employee_ID""")
for row in cursor.fetchall():
    print(row)


print("\nPilots with more than 2 flights scheduled:")
cursor = conn.execute("""SELECT p.FirstName || ' ' || p.LastName AS PilotName, COUNT(*) AS FlightCount
                         FROM Flights f
                         JOIN Pilots p ON f.Pilot_ID = p.Employee_ID
                         GROUP BY p.Employee_ID
                         HAVING COUNT(*) > 2""")
for row in cursor.fetchall():
    print(row)