import streamlit as st
from pymongo import MongoClient

# Replace with your MongoDB connection string
# For a local MongoDB server, it would typically be: "mongodb://localhost:27017/"
# For MongoDB Atlas, it would be something like: "mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
username = st.secrets.mongo["username"]
password = st.secrets.mongo["password"]
MONGO_URI = f"mongodb+srv://{username}:{password}@umud.jmbqpo0.mongodb.net/?retryWrites=true&w=majority&appName=UMUD"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client.muscel_ultrasound
collection = db.metadata

# Example data
example_data = [
    {
        "muscle": "Biceps",
        "image_type": "Type1",
        "device": "DeviceA",
        "age": 25,
        "sex": "Male",
        "height": 180,
        "weight": 75,
        "dataset_link": "https://example.com/dataset1",
    },
    {
        "muscle": "Triceps",
        "image_type": "Type2",
        "device": "DeviceB",
        "age": 30,
        "sex": "Female",
        "height": 165,
        "weight": 60,
        "dataset_link": "https://example.com/dataset2",
    },
    {
        "muscle": "Quadriceps",
        "image_type": "Type3",
        "device": "DeviceC",
        "age": 40,
        "sex": "Male",
        "height": 175,
        "weight": 80,
        "dataset_link": "https://example.com/dataset3",
    },
]

# Insert data into the collection


# Retrieve and print data from the collection
document = collection.find_one({"muscle": "Biceps", "image_type": "Type1"})
print(document["dataset_link"])
