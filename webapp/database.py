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
        "DATASET_NAME": "Leg3dUS_2024",
        "DOI": "",
        "VERSION": "1.0",
        "MUSCLE": ["Soleus", "Gastrocnemius Lateralis", "Gastrocnemius Medialis"],
        "MUSCLE_REGION": ["Whole"],
        "DEVICE": ["Aixplorer Ultimate"],
        "TRANSDUCER": ["50mm linear"],
        "DATA_TYPE": "Volume",
        "FILE_TYPE": "MHA",
        "IMAGE_TYPE": None,
        "DATA_PLANE": None,
        "SCANNING_FREQUENCY": None,
        "SAMPLING_RATE": None,
        "PARTICIPANT_AGE": None,
        "PARTICIPANT_HEIGHT": 173,
        "PARTICIPANT_WEIGHT": 64,
        "PARTICIPANT_SEX": "Both",
        "SAMPLE_SIZE": 44,
        "DATA_LABELS": True,
        "DATA_LABELS_DESCRIPTION": "Labels represent four different muscle types with integer values {0,100,150,200} corresponding to the background, Soleus (SOL), Gastrocnemius Medialis (GM), and Gastrocnemius Lateralis (GL).",
        "SHORT_DESCRIPTION": "The dataset assembles pairs of Ultrasound volumes and 3-labels muscles of the low-limb leg from 44 healthy volunteers, aged between 18 and 45 years, with an average height of 173\u00b111 cm and body mass of 64.3\u00b112.4 kg.Three-dimensional arrays are in MetaImage Medical Format (MHA), with an average voxel grid of 564\u00d7632\u00d71443 (\u00b149\u00d738\u00d7207), with an isotropic voxel spacing of about 0.276993 mm\u00b3 (\u00b10.015 mm\u00b3). The ultrasound imaging utilized a 40mm linear VERMON probe with a frequency range of 2-10 MHz, and an Aixplorer, Supersonic Imagine Ultrasound machine. The tracking of the ultrasound probe was meticulously performed with a 6-camera Optitrack system. During the scans, participants were positioned prone with their leg in a custom-made bath, ensuring minimal pressure influence on the measurements. Multiple parallel sweeps, ranging from the knee to the ankle and recorded every 5 mm in low-speed mode, were conducted. The resulting high-resolution 3D ultrasound volumes were compounded using the tracking matrices of the probe, offering an unprecedented level of detail and accuracy in musculoskeletal imaging. The annotations, carried out by two double-blinded experts, focused on evaluating intra-operative volumetric error, which was found to be as low as 4%.",
        "DATASET_YEAR": "2024",
        "PUBLICATION_LINK": "https://link.springer.com/article/10.1007/s11548-024-03170-7",
        "DATASET_LINK": "https://www.cs.cit.tum.de/camp/publications/leg-3d-us-dataset/",
        "AUTHORS": [
            "Vanessa Gonzalez Duque",
            "Alexandra Marquardt",
            "Yordanka Velikova",
            "Lilian Lacourpaille",
            "Antoine Nordez",
            "Marion Crouzier",
            "Hong Joo Lee",
            "Diana Mateus",
            "Nassir Navab",
        ],
        "CONTACT": "vanessag.duque@tum.de",
        "LICENSE": "GNU General Public License (GPL) 3.0",
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"DATASET_NAME": "Leg3dUS_2024"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
