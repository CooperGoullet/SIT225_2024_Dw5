import csv
from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb+srv://s222326285:Hy07boTyJknc4YF4@accelerometer1.a16ok.mongodb.net/?retryWrites=true&w=majority&appName=Accelerometer1"

# Create a MongoClient object using the connection string
client = MongoClient(connection_string)

# Access the database
db = client['accelerometer_data']

# Access the collection
collection = db['sensor_readings']

# Query the data
data = collection.find()

# Open a CSV file to write data
with open('accelerometer_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['x', 'y', 'z', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for document in data:
        writer.writerow({
            'x': document.get('x', ''),
            'y': document.get('y', ''),
            'z': document.get('z', ''),
            'timestamp': document.get('timestamp', '')  # Default to empty string if not present
        })

print("Data has been written to accelerometer_data.csv")
