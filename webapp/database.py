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
        "DATASET_NAME": "SMA_2019",
        "DOI": "10.17632/dpmf9bz8pt.2",
        "VERSION": "2.0",
        "MUSCLE": [
            "Tibialis Anterior",
            "Gastrocnemius Medialis"
        ],
        "MUSCLE_REGION": [
            "Whole"
        ],
        "DEVICE": [
            "Telemed LogicScan 128",
            "Philips HD11"
        ],
        "TRANSDUCER": [
            "LV7.5/60/96Z",
            "HL9.0/60/128Z-2"
        ],
        "DATA_TYPE": "Image",
        "FILE_TYPE": [
            "png"
        ],
        "IMAGE_TYPE": [
            "Static"
        ],
        "IMAGE_NUMBER": 114,
        "VIDEO_NUMBER": None,
        "DATA_PLANE": [
            "Longitudinal"
        ],
        "SCANNING_FREQUENCY": None,
        "SAMPLING_RATE": None,
        "PARTICIPANT_AGE": None,
        "PARTICIPANT_HEIGHT": None,
        "PARTICIPANT_BODYMASS": None,
        "PARTICIPANT_SEX": None,
        "SAMPLE_SIZE": 15,
        "DATA_LABELS": None,
        "DATA_LABELS_DESCRIPTION": "",
        "SHORT_DESCRIPTION": "Ultrasound images of muscle architecture were acquired using LogicScan 128 EXT-1Z systems with transducers LV7.5/60/96Z and HL9.0/60/128Z-2, at scanning frequencies of 9–12 MHz, to analyze the gastrocnemius medialis and tibialis anterior and Phillips HD11 at scanning frequency from 5-12 MHz. Data were collected from 15 participants, with optimized settings for fascicle and aponeurosis visualization. To assess the influence of different ultrasound settings, three sample groups were analyzed: Sample A: Scans of the gastrocnemius medialis from 15 individuals, acquired at 9 MHz using a 96-element transducer (60 mm, LV7.5/60/96Z, LogicScan 128 EXT-1Z, Telemed, Lithuania). Sample B: Additional scans of the gastrocnemius medialis from 15 individuals, taken at 12 MHz with a 128-element transducer (50 mm, 5–12 MHz HD11XE, Phillips, Bothell, Washington, USA). Sample C: Dynamic scans of the tibialis anterior, acquired at 12 MHz using a 128-element transducer (60 mm, HL9.0/60/128Z-2, LogicScan 128 EXT-1Z, Telemed, Lithuania), recorded at 15 frames per second during unconstrained dorsiflexion-plantarflexion movements.",
        "DATASET_YEAR": "2019",
        "PUBLICATION_LINK": "https://doi.org/10.1371/journal.pone.0229034",
        "DATASET_LINK": "https://data.mendeley.com/datasets/dpmf9bz8pt/2",
        "AUTHORS": [
            "Oliver R. Seynnes",
            "Neil J. Cronin"
        ],
        "CONTACT": "olivier.seynnes@nih.no",
        "LICENSE": "Creative Commons Attribution 4.0 International (CC BY 4.0)"
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"DATASET_NAME": "SMA_2019"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
