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
        "DATASET_NAME": "HEELRISE_2017",
        "DOI": "10.23729/d540861d-dcfb-40a6-ad44-ffee9416584c",
        "VERSION": "1.0",
        "MUSCLE": [
            "Gastrocnemius Medialis"
        ],
        "MUSCLE_REGION": [
            "Middle"
        ],
        "DEVICE": [
            "Telemed LogicScan 128"
        ],
        "TRANSDUCER": [
            "LV7.5/60/90z"
        ],
        "DATA_TYPE": "Video",
        "FILE_TYPE": [
            "mp4"
        ],
        "IMAGE_TYPE": [
            "Static"
        ],
        "IMAGE_NUMBER": None,
        "VIDEO_NUMBER": 151,
        "DATA_PLANE": [
            "Longitudinal"
        ],
        "SCANNING_FREQUENCY": 6,
        "SAMPLING_RATE": 80,
        "PARTICIPANT_AGE": 27,
        "PARTICIPANT_HEIGHT": 174,
        "PARTICIPANT_BODYMASS": 69,
        "PARTICIPANT_SEX": "Both",
        "SAMPLE_SIZE": 13,
        "DATA_LABELS": False,
        "DATA_LABELS_DESCRIPTION": "",
        "SHORT_DESCRIPTION": "Medial gastrocnemius muscle fascicle behavior was assessed during repetitive heel-rise exercises with varying tempo (0,5 Hz and 0,83 Hz) and load from 13 participants (6 females, 7 males). Their mean age was 27 years, height 174 cm and weight 69 kg. Ultrasound videos were captured using Logicscan 128 (Telemed Ltd.) device with LV7.5/60/96Z transducer with 6MHz scanning frequency and sampling frequency of 80 frames per second. Videos are in avi format. During heel-rise exercises, the load was varied by exercising with one or two legs and adding extra 10%, 30%, or 40% of body weight. Filenames contain this information the first number referring to tempo (30 or 50), LEG for single leg, BW for double leg and the last numbers (if any) refer to added extra load (10, 30 or 40). Thus, 01_30BW.avi refers to participant 01 when performing heel rises with two legs and body weight only with the slower pace",
        "DATASET_YEAR": "2017",
        "PUBLICATION_LINK": "https://jyx.jyu.fi/bitstream/handle/123456789/66588/URN%3aNBN%3afi%3ajyu-201912025076.pdf?sequence=1&isAllowed=y",
        "DATASET_LINK": "https://etsin.fairdata.fi/dataset/d2cbac90-d916-469e-877f-6053d817a765",
        "AUTHORS": [
            "Taija Finni",
            "Emma Niemi",
            "Glen Lichtwark"
        ],
        "CONTACT": "taija.finni@jyu.fi",
        "LICENSE": "Creative Commons Attribution 4.0 International (CC BY 4.0)"
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"DATASET_NAME": "HEELRISE_2017"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
