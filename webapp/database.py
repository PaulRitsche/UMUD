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
        "DATASET_NAME": "DeepMTJ_2021",  # Name the dataset accordingly
        "DOI": None,  # Provide a DOI
        "VERSION": 1.0,  # Version of the dataset
        "MUSCLE": [
            "Gastrocnemius medialis",
            "Gastrocnemius lateralis",
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": "distal",  # Which muscle regions are included in the dataset?
        "DEVICE": [
            "Aixplorer V6, SuperSonic Imagine, Aix-en-Provence, France",
            "MyLab 60, Esoate Biomedical, Genova, Italy",
            "ArtUs EXT-1H, TELEMED, Milan, Italy ",
        ],  # What US device was used?
        "PROBE": [
            "linear-array 90mm, LA923",
            "linear-array 60mm, LV8-5N60-A2",
            "linear-array 38-mm probe, Superline SL10-2",
        ],  # What probe was used?
        "DATA_TYPE": "images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "jpeg",  # What is the file type of the data?
        "IMAGE_TYPE": "static",  # If images are included, are they static or panoramic?
        "DATA_PLANE": "Longitudinal",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": None,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": None,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": None,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "both",  # Included males, females, or both?
        "SAMPLE_SIZE": 161,  # How many participants are included in the dataset?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "Manually set labels in the training dataset denote exact pixel positions of estimated MTJ positions in the image and images were labelled by a total of four raters. For our training, we used soft labeling, where we assigned probability values to each image pixel. We used probability maps at the same resolution as original images, where we modeled positions of the MTJ by a 2D normal distribution with a covariance of 100 pixels at positions of specialist labels.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "Data were collected at the University of Graz, the Graz University of Technology and the University of Queensland between 2014 and 2020 on 123 healthy and 38 impaired individuals inclduing children and adults. With 1590 recordings, the isometric maximum voluntary contractions (MVC) and passive torque movements (PT) on the medial gastrocnemius (MG) had the largest share in the dataset. A smaller amount of data was collected on the MG during running (48 recordings). The measurements on the lateral gastrocnemius (LG) consist of 109 recordings. The complete and fully anonymous dataset holds 1747 video recordings with a mean length of 19.84 seconds per video. Sequences were captured at frame-rates of 30 frames per second (fps) for studies with an Aixplorer V6 (SuperSonic Imagine, Aix-en-Provence, France) US system (Aixplorer), 25 fps for studies with the Esaote MyLab60 system (Esaote), and 30-80 fps for the Telemed ArtUs US (Telemed), respectively. The scanning frequency varied between 7 to 9 MHz.",  # Describe the data in 3-4 sentences.
        "DATASET_YEAR": "2021",  # What year was the dataset created?
        "PUBLICATION_LINK": "10.1109/TBME.2021.3130548",  # Can you provide a link to the publication containing the data?
        "AUTHORS": [
            "Christoph Leitner",
            "Robert Jarolim",
            "Bernhard Englmair",
            "Annika Kruse",
            "Karen Andrea Lara Hernandez",
            "Andreas Konrad",
            "Eric Yung-Sheng Su",
            "Jorg Schrottner",
            "Luke A Kelly",
            "Glen A Lichtwark",
            "Markus Tilp",
            "Christian Baumgartner",
        ],  # Who are the authors of the data?
        "CONTACT": [
            "christoph.leitner@tugraz.at",
        ],  # Provide contact details of the authors.
        "DATASET_LINK": "https://osf.io/wgy4d/",  # Will be provided by us if not already existent.
        "LICENSE": "CC-By Attribution 4.0 International",  # What is the license of the data?
        "SCANNING_FREQUENCY": None,  # What is the scanning frequency of the data?
        "SAMPLING_RATE": 80,  # What is the sampling rate or fps of the data collection?
    }
]


# Insert data into the collection
# Uncomment the next line to insert template data into database
collection.insert_many(dictionary)

# Retrieve and print data from the collection
query = {"DATASET_NAME": "DeepMTJ_2021"}
results = collection.find(query)

# Print the result, DATASET_LINK must be present
print([result["DATASET_LINK"] for result in results])
