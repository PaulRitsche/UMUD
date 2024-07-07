import pytest


def validate_template_data(entry):
    """
    Validate a single entry in the template data against the expected data types and structure.

    Parameters:
    entry (dict): A dictionary representing a single entry in the template data.

    Raises:
    AssertionError: If any field is missing or if the field's type does not match the expected type.
    """

    # Define the expected types for each field in the template
    expected_types = {
        "DATASET_NAME": str,
        "MUSCLE": str,
        "MUSCLE_REGION": str,
        "DEVICE": str,
        "PROBE": str,
        "DATA_TYPE": str,
        "FILE_TYPE": str,
        "IMAGE_TYPE": str,
        "DATA_PLANE": str,
        "PARTICIPANT_AGE": (float, type(None)),
        "PARTICIPANT_HEIGHT": (float, type(None)),
        "PARTICIPANT_WEIGHT": (float, type(None)),
        "PARTICIPANT_FATMASS": (float, type(None)),
        "PARTICIPANT_MUSCLEMASS": (float, type(None)),
        "PARTICIPANT_SEX": str,
        "DATA_LABELS": bool,
        "DATA_LABELS_DESCRIPTION": str,
        "SHORT_DESCRIPTION": str,
        "PUBLICATION_LINK": (str, type(None)),
        "AUTHORS": list,
        "CONTACT": list,
        "DATASET_LINK": (str, type(None)),
        "LICENSE": str,
    }

    # Validate each field in the entry
    for field, expected_type in expected_types.items():
        assert field in entry, f"Missing field: {field}"
        assert isinstance(
            entry[field], expected_type
        ), f"Incorrect type for {field}: expected {expected_type}, got {type(entry[field])}"

        # Additional checks for list elements
        if field in ["AUTHORS", "CONTACT"]:
            assert all(
                isinstance(item, str) for item in entry[field]
            ), f"Incorrect type in list for {field}: all items should be str"


def test_template_data():
    """
    Test function to validate the entries in the template data against the specified data types and format.

    Uses the validate_template_data function to check each entry in the template_data list.
    """

    # Define the template data to be validated
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

    # Validate each entry in the template data
    for entry in template_data:
        validate_template_data(entry)


if __name__ == "__main__":
    pytest.main()
