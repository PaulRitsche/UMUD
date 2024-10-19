template_data = [
    {
        "DATASET_NAME": "FALLMUD_2017",  # Name the dataset accordingly
        "DOI": None,  # Provide a DOI
        "VERSION": 1.0,  # Version of the dataset
        "MUSCLE": [
            "Gastrocnemius",
            "Soleus",
        ],  # What muscle is included in the dataset? If more than one, split the dataset into multiple parts
        "MUSCLE_REGION": "middle",  # Which muscle regions are included in the dataset?
        "DEVICE": "AlokaSSD-5000 PHD 7.5 MHz",  # What US device was used?
        "PROBE": None,  # What probe was used?
        "DATA_TYPE": "images",  # Does the dataset contain images, videos, or volumes?
        "FILE_TYPE": "jpg",  # What is the file type of the data?
        "IMAGE_TYPE": "static",  # If images are included, are they static or panoramic?
        "DATA_PLANE": "longitudinal",  # In what plane were the images/videos collected?
        "PARTICIPANT_AGE": 30,  # Mean age of participants.
        "PARTICIPANT_HEIGHT": None,  # Mean height of participants (in cm).
        "PARTICIPANT_WEIGHT": None,  # Mean weight of participants (in kg).
        "PARTICIPANT_SEX": "both",  # Included males, females, or both?
        "SAMPLE_SIZE": 8,  # How many participants are included in the dataset?
        "DATA_LABELS": True,  # Are labels provided for the data?
        "DATA_LABELS_DESCRIPTION": "The labels are provided as binary masks.",  # If labels are provided, what is the format of the labels?
        "SHORT_DESCRIPTION": "This dataset presents an investigation into the feasibility of using deep learning methods for developing abitrary full spatial resolution regression analysis of B-mode ultrasound images of human skeletal muscle. Dynamic ultrasound images sequences of the calf muscles were acquired (25 Hz) from 8 healthy volunteers (4 male, ages: 25–36, median 30). Here, the labels correspond to the extrapolated fascicles including curvature, not only visible fascicle fragments. ",  # Describe the data in 3-4 sentences.
        "DATASET_YEAR": 2017,  # What year was the dataset created?
        "PUBLICATION_LINK": "https://www.mdpi.com/2313-433X/4/2/29",  # Can you provide a link to the publication containing the data?
        "AUTHORS": [
            "Ryan Cunningham",
            "Maria B. Sanchez",
            "Gregory May",
            "Ian Loram",
        ],  # Who are the authors of the data?
        "CONTACT": [
            "M.Sanchez.Puccini@mmu.ac.uk",
            "g.may@mmu.ac.uk",
        ],  # Provide contact details of the authors.
        "DATASET_LINK": "https://kalisteo.cea.fr/index.php/fallmud/",  # Will be provided by us if not already existent.
        "LICENSE": "Attribution-NonCommercial 4.0 International",  # What is the license of the data?
        "SCANNING_FREQUENCY": "7.5Hz",  # What is the scanning frequency of the data?
        "SAMPLING_RATE": 25,  # What is the sampling rate or fps of the data collection?
    }
]
