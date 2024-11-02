template_data = template_data = [
    {
        "DATASET_NAME": "Deep_MTJ_2021",  # Name the dataset accordingly
        "DOI": None,  # Provide a DOI
        "VERSION": "1.0",  # Version of the dataset
        "MUSCLE": [
            "Gastrocnemius medialis",
            "Gastrocnemius lateralis",
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": None,  # Which muscle regions are included in the dataset?
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
        "IMAGE_TYPE": None,  # If images are included, are they static or panoramic?
        "DATA_PLANE": "Longitudinal",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": None,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": None,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": None,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "both",  # Included males, females, or both?
        "SAMPLE_SIZE": "161",  # How many participants are included in the dataset?
        "DATA_LABELS": "Yes",  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": None,  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "",  # Describe the data in 3-4 sentences.
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
