template_data = [
    {
        "DATASET_NAME": "DeepACSA_2022",  # Name the dataset accordingly
        "DOI": "10.17605/OSF.IO/A3U4V",  # Provide a DOI
        "VERSION": 1.0,  # Version of the dataset
        "MUSCLE": [
            "Rectus femoris",
            "Vastus lateralis",
            "Gastrocnemius medialis",
            "Gastrocnemius lateralis",
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": [
            "proximal",
            "middle",
            "distal",
        ],  # Which muscle regions are included in the dataset?
        "DEVICE": [
            "ACUSON Juniper, SIEMENS Healthineers Erlangen, Germany",
            "Aixplorer Ultimate, SuperSonic Imagine, Aix-en-Provence, France",
            "Mylab 70, linear-array 47-mm probe, Esaote Biomedica, Genova, Italy",
        ],  # What US device was used?
        "PROBE": [
            "linear-array 54-mm probe, 12 L3 Acuson",
            "linear-array 38-mm probe, Superline SL10-2",
            "linear-array 47-mm probe, Esaote",
        ],  # What probe was used?
        "DATA_TYPE": "images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "tif",  # What is the file type of the data?
        "IMAGE_TYPE": "panoramic",  # If images are included, are they static or panoramic?
        "DATA_PLANE": "transverse",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": 38.2,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": None,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": None,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "both",  # Included males, females, or both?
        "SAMPLE_SIZE": 153,  # How many participants are included in the dataset?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "The labels are provided as binary masks of the whole muscle anatomical cross-sectional area.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "The DeepACSA dataset contains panoramic ultrasound images of the human rectus femoris (RF), vastus lateralis (VL), gastrocnemius medialis (GM) and lateralis (GL) muscles. A total of 1772 (including image augmentation) ultrasound images from 153 participants (age = 38.2 yr, range = 13–78). The images were acquired with the participants in supine (VL and RF) and prone (GM and GL) positions at multiple regions.",  # Describe the data in 3-4 sentences.
        "DATASET_YEAR": 2022,  # What year was the dataset created?
        "PUBLICATION_LINK": "https://journals.lww.com/acsm-msse/fulltext/2022/12000/deepacsa__automatic_segmentation_of.21.aspx",  # Can you provide a link to the publication containing the data?
        "AUTHORS": [
            "Paul Ritsche",
            "Philipp Wirth",
            "Neil J. Cronin",
            "Fabio Sarto",
            "Marco V. Narici",
            "Oliver Faude",
            "Martino V. Franchi",
        ],  # Who are the authors of the data?
        "CONTACT": [
            "paul.ritsche@unibas.ch",
        ],  # Provide contact details of the authors.
        "DATASET_LINK": "https://osf.io/a3u4v/",  # Will be provided by us if not already existent.
        "LICENSE": "Apache License 2.0",  # What is the license of the data?
        "SCANNING_FREQUENCY": None,  # What is the scanning frequency of the data?
        "SAMPLING_RATE": None,  # What is the sampling rate or fps of the data collection?
    }
]
