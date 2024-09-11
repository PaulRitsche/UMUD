"""
This module connects to a MongoDB database to insert and retrieve muscle ultrasound dataset metadata. 
It uses Streamlit secrets for secure connection management. 

Note
---- 
It is only possible to insert data into the database with access rights to the MongoDB atlas. 
"""

import streamlit as st
from pymongo import MongoClient

MONGO_URI = st.secrets.mongo["CONNECTION_STRING"]

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client.muscle_ultrasound
collection = db.datasets

# Example data
dictionary = [
    {
        "DATASET_NAME": "Quadriceps Muscle Data 2024",  # Name the dataset accordingly
        "DOI": "10.1000/quadriceps2024",  # Provide a DOI
        "VERSION": "1.0",  # Version of the dataset
        "MUSCLE": "Rectus Femoris",  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": [
            "proximal",
            "middle",
        ],  # Which muscle regions are included in the dataset?
        "DEVICE": "Siemens Juniper",  # What US device was used?
        "PROBE": "L12/3 Linear Probe",  # What probe was used?
        "DATA_TYPE": "Images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "jpg",  # What is the file type of the data?
        "IMAGE_TYPE": "Static",  # If images are included, are they static or panoramic?
        "DATA_PLANE": "Transverse",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": 29.5,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": 175.3,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": 70.8,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "Both",  # Included males, females, or both?
        "SAMPLE_SIZE": 100,  # How many participants are included in the dataset?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "The labels are provided in the form of a spreadsheet.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "This dataset contains ultrasound images of the quadriceps muscle, specifically the rectus femoris middle and proximal regions. Images were collected using a Siemens Juniper device with a linear probe. The dataset includes static transverse plane images from participants aged 20-40 years.",  # Describe the data in 3-4 sentences.
        "DATASET_YEAR": "2024",  # What year was the dataset created?
        "PUBLICATION_LINK": "https://doi.org/10.1000/quadriceps2024",  # Can you provide a link to the publication containing the data?
        "AUTHORS": [
            "Dr. Jane Doe",
            "Dr. John Smith",
        ],  # Who are the authors of the data?
        "CONTACT": [
            "jane.doe@university.edu",
            "john.smith@hospital.org",
        ],  # Provide contact details of the authors.
        "DATASET_LINK": "https://datarepository.university.edu/quadriceps2024",  # Will be provided by us if not already existent.
        "LICENSE": "CC BY 4.0",  # What is the license of the data?
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"MUSCLE": "Quadriceps"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
