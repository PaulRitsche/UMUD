"""
UMUD Database Template

This module provides a template for creating entries in the UMUD (Ultrasound Muscle Data) database. 
The template is a dictionary containing various fields that describe the dataset in detail. 
The information provided in this template will be used to create a new entry in a MongoDB database.

Each field in the template must be filled out with the appropriate data. 
Below, you will find a detailed explanation of each field along with its expected data type and an example of a completed entry.

Fields and their descriptions:
- DATASET_NAME (str): Name of the dataset.
- MUSCLE (str): The muscle included in the dataset. If more than one muscle is included, split the dataset into multiple parts.
- MUSCLE_REGION (str): The specific regions of the muscle included in the dataset.
- DEVICE (str): The ultrasound (US) device used to collect the data.
- PROBE (str): The type of probe used during data collection.
- DATA_TYPE (str): The type of data (e.g., images, videos, volumes).
- FILE_TYPE (str): The file format of the data (e.g., jpg, png, mp4).
- IMAGE_TYPE (str): If images are included, specify whether they are static or extended-field-of-view.
- DATA_PLANE (str): The plane in which the images/videos were collected (e.g., transverse, longitudinal).
- PARTICIPANT_AGE (float): Mean age of the participants.
- PARTICIPANT_HEIGHT (float): Mean height of the participants (in cm).
- PARTICIPANT_WEIGHT (float): Mean weight of the participants (in kg).
- PARTICIPANT_FATMASS (float): Mean fat mass of the participants (in kg).
- PARTICIPANT_MUSCLEMASS (float): Mean muscle mass of the participants (in kg).
- PARTICIPANT_SEX (str): Gender of the participants included in the study (e.g., male, female, both).
- DATA_LABELS (bool): Whether labels are provided for the data (True/False).
- DATA_LABELS_DESCRIPTION (str): Description of the labels provided for the data.
- SHORT_DESCRIPTION (str): A brief description of the dataset (3-4 sentences).
- PUBLICATION_LINK (str): A link to the publication containing the data, if available.
- AUTHORS (list of str): Names of the authors of the dataset.
- CONTACT (list of str): Contact details of the authors.
- DATASET_LINK (str): A link to the dataset, to be provided if not already existent.
- LICENSE (str): The license under which the data is shared.

If you can't fill out a field, please instert "None" as a placeholder.
Your filled our template must match the pres-specified data types and format. We cannot consider youd entry if it does not.
Before inserting your entry in our database, please be aware that we will thoroughly check the template for errors.
"""

template_data = [
    {
        "DATASET_NAME": "Quadriceps Muscle Data 2024",  # Name the dataset accordingly
        "MUSCLE": "Quadriceps",  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": "Rectus Femoris",  # Which muscle regions are included in the dataset?
        "DEVICE": "GE Logiq E9",  # What US device was used?
        "PROBE": "Linear Probe",  # What probe was used?
        "DATA_TYPE": "Images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "jpg",  # What is the file type of the data?
        "IMAGE_TYPE": "Static",  # If images are included, are they static or extended-field-of-view?
        "DATA_PLANE": "Transverse",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": 29.5,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": 175.3,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": 70.8,  # Mean weight of participants (in kg).
        "PARTICIPANT_FATMASS": None,  # Mean fat mass of participants (in kg).
        "PARTICIPANT_MUSCLEMASS": None,  # Mean muscle mass of participants (in kg).
        "PARTICIPANT_SEX": "Both",  # Included males, females, or both?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "The labels are provided in the form of a spreadsheet.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "This dataset contains ultrasound images of the quadriceps muscle, specifically the rectus femoris region. Images were collected using a GE Logiq E9 device with a linear probe. The dataset includes static transverse plane images from participants aged 20-40 years.",  # Describe the data in 3-4 sentences.
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
