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
        "DATASET_NAME": "BicepsFem3DUS_2024",
        "DOI": "10.48610/a38a05d",
        "VERSION": "1.0",
        "MUSCLE": [
            "Biceps Femoris"
        ],
        "MUSCLE_REGION": [
            "Whole"
        ],
        "DEVICE": [
            "Telemed ArtUs EXT-1H"
        ],
        "TRANSDUCER": [
            "LF11-5H60-A3"
        ],
        "DATA_TYPE": "Volume",
        "FILE_TYPE": [],
        "IMAGE_TYPE": [],
        "DATA_PLANE": [
            "Longitudinal"
        ],
        "SCANNING_FREQUENCY": None,
        "SAMPLING_RATE": None,
        "PARTICIPANT_AGE": 27,
        "PARTICIPANT_HEIGHT": 179,
        "PARTICIPANT_WEIGHT": 75,
        "PARTICIPANT_SEX": "Both",
        "SAMPLE_SIZE": 12,
        "DATA_LABELS": False,
        "DATA_LABELS_DESCRIPTION": "",
        "SHORT_DESCRIPTION": "This dataset comprises data used for the analyses of hamstring muscle adaptations following 9 weeks of eccentric training and 3 weeks of detraining, focusing on fascicle lengths measured via 3D ultrasound, sarcomere lengths obtained through microendoscopy, and knee flexor force assessed using load cells. Alongside these measurements, the dataset includes all relevant data used for statistical analyses, presented in CSV files. These data provide detailed insights into the multiscale adaptations of hamstring muscles to eccentric training and detraining periods. Note that the downloadable dataset does not only contain 3DUS images but other data from the study as well.",
        "DATASET_YEAR": "2024",
        "PUBLICATION_LINK": "https://www.sciencedirect.com/science/article/pii/S2095254624001534?via%3Dihub#sec0022",
        "DATASET_LINK": "https://espace.library.uq.edu.au/view/UQ:a38a05d",
        "AUTHORS": [
            "Max H. Andrews",
            "Anoosha Pai S",
            "Reed D. Gurchiek",
            "Patricio A. Pincheira",
            "Akshay S. Chaudhari",
            "Paul W. Hodges",
            "Glen A. Lichtwark",
            "Scott L. Delp"
        ],
        "CONTACT": "data@library.uq.edu.au",
        "LICENSE": "Creative Commons Attribution 4.0 International (CC BY 4.0)"
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"DATASET_NAME": "BicepsFem3DUS_2024"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
