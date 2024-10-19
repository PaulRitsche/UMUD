template_data = [
    {
        "DATASET_NAME": "DL_Track_US_2023",  # Name the dataset accordingly
        "DOI": "10.17605/OSF.IO/7MJSC",  # Provide a DOI
        "VERSION": 1.0,  # Version of the dataset
        "MUSCLE": [
            "Medial Gastrocnemius",
            "Soleus",
            "Vastus Laterlis",
            "Tibialis Anterior",
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": [
            "middle",
        ],  # Which muscle regions are included in the dataset?
        "DEVICE": [
            "Aloka Alpha-10 Hitachi Healthcare",
            "ArtUS EXT-1H TELEMED",
            "HD11 Philips Electronics",
            "Echo Blaster 128 TELEMED",
        ],  # What US device was used?
        "PROBE": None,  # What probe was used?
        "DATA_TYPE": "images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "tif",  # What is the file type of the data?
        "IMAGE_TYPE": "static",  # If images are included, are they static or panoramic?
        "DATA_PLANE": "longitudinal",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": None,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": None,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": None,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "both",  # Included males, females, or both?
        "SAMPLE_SIZE": None,  # How many participants are included in the dataset?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "The labels are provided as binary masks with visible fascicle fragments and aponeuroses being labeled.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "The dataset includes males and females and most images were from young participants (age range:18−35y, 57% males), although data from older participants aged up to about 70 and older than 60 are also included (20% of whole data set and 60% of those were males). Around 570 images for the aponeurosis model and 310 images for the muscle fascicle model were included. Along with the corresponding images, the manually created binary masks were used as ground truth labels to train the two deep neural networks. The data is augmented to approximately 1700 aponeurosis and fascicle images using height and width shift, brightness and rotation. The augmentation operations are all applied in random order to an image with in the specified range. The images are sampled at random from ultrasound video data during several dynamic conditions.",  # Describe the data in 3-4 sentences.
        "DATASET_YEAR": 2024,  # What year was the dataset created?
        "PUBLICATION_LINK": "https://doi.org/10.1016/j.ultrasmedbio.2023.10.011",  # Can you provide a link to the publication containing the data?
        "AUTHORS": [
            "Paul Ritsche",
            "Martino V. Franchi",
            "Oliver Faude",
            "Taija Finni",
            "Olivier Seynnes",
            "Neil J. Cronin",
        ],  # Who are the authors of the data?
        "CONTACT": [
            "paul.ritsche@unibas.ch",
        ],  # Provide contact details of the authors.
        "DATASET_LINK": "https://osf.io/xbawc/",  # Will be provided by us if not already existent.
        "LICENSE": "Apache License 2.0",  # What is the license of the data?
        "SCANNING_FREQUENCY": None,  # What is the scanning frequency of the data?
        "SAMPLING_RATE": None,  # What is the sampling rate or fps of the data collection?
    }
]
