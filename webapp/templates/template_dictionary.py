"""
UMUD Database Template

This module provides a template for creating entries in the UMUD (Ultrasound Muscle Data) database. 
The template is a dictionary containing various fields that describe the dataset in detail. 
The information provided in this template will be used to create a new entry in a MongoDB database.
Some of these fields are categorical, while others are numerical. Please adhere to the categories
provided in the template when fields are categorical (This is indicated by CHOOSE FROM).

Each field in the template must be filled out with the appropriate data. 
Below, you will find a detailed explanation of each field along with its expected data type and an example of a completed entry.

### Fields and Their Descriptions

- **DATASET_NAME (str):** 
  - *Description:* Name of the dataset.
  - *Example:* "Quadriceps_Muscle_Sonography_2024"

- **DOI (str):**
  - *Description*: The digital object identifier (DOI) for the dataset.
  - *Example:* "10.1000/182"

- **VERSION (float):**
  - *Description:* Version of the dataset.
  - *Example:* "1.0"

- **MUSCLE (list of str):**
  - *Description:* The muscle(s) included in the dataset.
  - *Example:* ["Rectus femoris", "Vastus lateralis"]

- **MUSCLE_REGION (list of str):**
  - *Description:* The specific regions of the muscle included in the dataset.
  - *Options:* Choose from proximal (0-33% of muscle/bone length), middle (33-66% of muscle/bone length), distal (66-100% of muscle/bone length).
  - *Example:* ["proximal", "middle"]

- **DEVICE_MODEL (str):**
  - *Description:* The ultrasound device used to collect the data.
  - *Example:* "Siemens Juniper"

- **PROBE_MODEL (str):**
  - *Description:* The model of the probe used during data collection.fond
  - *Example:* "ML6-15"

- **DATA_TYPE (str):**
  - *Description:* The type of data collected in the dataset.
  - *Options:* Choose from images, videos, volumes.
  - *Example:* "images"

- **FILE_TYPE (str):**
  - *Description:* The file format of the data.
  - *Example:* "jpg"

- **IMAGE_TYPE (str):**
  - *Description:* Specifies whether the images are static or panoramic.
  - *Options:* Choose from static, panoramic.
  - *Example:* "static"

- **DATA_PLANE (str):**
  - *Description:* The plane in which the images/videos were collected.
  - *Options:* Choose from transverse, longitudinal.
  - *Example:* "transverse"

- **PARTICIPANT_AGE (float):**
  - *Description:* Mean age of the participants.
  - *Example:* 29.5

- **PARTICIPANT_HEIGHT (float):**
  - *Description:* Mean height of the participants (in cm).
  - *Example:* 175.3

- **PARTICIPANT_WEIGHT (float):**
  - *Description:* Mean weight of the participants (in kg).
  - *Example:* 70.8

- **PARTICIPANT_SEX (str):**
  - *Description:* Sex of the participants included in the study.
  - *Options:* Choose from male, female, both.
  - *Example:* "both"

- **SAMPLE_SIZE (int):**
  - *Description:* The number of participants included in the dataset.
  - *Example:* 100

- **DATA_LABELS (bool):**
  - *Description:* Whether labels are provided for the data.
  - *Options:* Choose from True, False.
  - *Example:* True

- **DATA_LABELS_DESCRIPTION (str):**
  - *Description:* Description of the labels provided for the data. Elaborate on the format of the labels and how they were created.
  - *Example:* "Labels provided in CSV format, indicating muscle thickness at different regions."

- **SHORT_DESCRIPTION (str):**
  - *Description:* A brief description of the dataset (3-4 sentences).
  - *Example:* "This dataset includes ultrasound images of the quadriceps muscle, collected from 50 participants aged 20-40. Images were taken using a GE Logiq E9 with a ML6-15 probe, focusing on the proximal and middle regions of the muscle."

- **DATASET_YEAR (str):**
  - *Description:* The year in which the dataset was created.
  - *Format:* Use the format YYYY.
  - *Example:* "2024"

- **PUBLICATION_LINK (str):**
  - *Description:* A link to the publication containing the data, if available.
  - *Example:* "https://doi.org/10.1000/quadriceps2024"

- **AUTHORS (list of str):**
  - *Description:* Names of the authors of the dataset.
  - *Example:* ["Dr. Jane Doe", "Dr. John Smith"]

- **CONTACT (list of str):**
  - *Description:* Contact details of the authors.
  - *Example:* ["jane.doe@university.edu", "john.smith@hospital.org"]

- **DATASET_LINK (str):**
  - *Description:* A link to the dataset, to be provided if not already existent.
  - *Example:* "https://datarepository.university.edu/quadriceps2024"

- **LICENSE (str):**
  - *Description:* The license under which the data is shared.
  - *Example:* "CC BY 4.0"

### Additional Instructions:

- **Filling Out the Template:** Each field must be completed with the exact data type specified. For example, if a field requires a string, do not enter a number or a list.
- **Placeholder for Missing Information:** If you do not have information for a particular field, enter "None". Do not leave any fields empty.
- **Consistency:** Ensure that the information you provide is consistent throughout the template. For example, if you mention a specific muscle region in the MUSCLE_REGION field, this should be reflected accurately in the description fields.
- **Validation:** Before submitting, double-check your entries for accuracy. Any errors or inconsistencies could lead to your dataset being rejected from the UMUD database.
- **Submission:** Once your template is complete, submit it through the designated submission process.

**Note:** Your filled-out template must match the pre-specified data types and format. We cannot consider your entry if it does not. Before inserting your entry in our database, please be aware that we will thoroughly check the template for errors. 

Thank you for contributing to the UMUD database! Your participation helps advance research and knowledge in muscle ultrasound data analysis.
"""

template_data = [
    {
        "DATASET_NAME": "Quadriceps Muscle Data 2024",  # Name the dataset accordingly
        "DOI": "10.1000/quadriceps2024",  # Provide a DOI
        "VERSION": "1.0",  # Version of the dataset
        "MUSCLE": [
            "Rectus Femoris"
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
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
