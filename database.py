import streamlit as st
from pymongo import MongoClient

# Replace with your MongoDB connection string
# For a local MongoDB server, it would typically be: "mongodb://localhost:27017/"
# For MongoDB Atlas, it would be something like: "mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
# username = st.secrets.mongo["username"]
# password = st.secrets.mongo["password"]
MONGO_URI = st.secrets.CONNECTION_STRING

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client.muscle_ultrasound
collection = db.datasets

# Example data
example_data = [
    {
        "muscle": "Gastrocnemius Medialis",
        "image_type": ".tiff",
        "device": "GE",
        "age": 25,
        "sex": "Male",
        "height": 180,
        "weight": 75,
        "dataset_link": "https://example.com/dataset1",
    },
    {
        "muscle": "Vastus Lateralis",
        "image_type": ".tiff",
        "device": "Siemens",
        "age": 30,
        "sex": "Female",
        "height": 165,
        "weight": 60,
        "dataset_link": "https://example.com/dataset2",
    },
    {
        "muscle": "Vastus Lateralis",
        "image_type": ".jpeg",
        "device": "Esaote",
        "age": 40,
        "sex": "Male",
        "height": 175,
        "weight": 80,
        "dataset_link": "https://example.com/dataset3",
    },
]

# Insert data into the collection
# collection.insert_many(example_data)

# Retrieve and print data from the collection
query = {"muscle": "Gastrocnemius Medialis"}
results = collection.find(query)
print([result["dataset_link"] for result in results])
