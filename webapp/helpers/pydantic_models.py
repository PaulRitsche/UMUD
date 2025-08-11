import streamlit_pydantic as sp
from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator
from typing import List, Optional, Set
import json
from enum import Enum
import re


class SelectionValueMuscle(str, Enum):
    # Lower limb muscles
    RECTUS_FEMORIS = "Rectus Femoris"
    VASTUS_LATERALIS = "Vastus Lateralis"
    VASTUS_MEDIALIS = "Vastus Medialis"
    VASTUS_INTERMEDIUS = "Vastus Intermedius"
    QUADRICEPS_FEMORIS = "Quadriceps Femoris"
    BICEPS_FEMORIS = "Biceps Femoris"
    SEMITENDINOSUS = "Semitendinosus"
    SEMIMEMBRANOSUS = "Semimembranosus"
    GASTROCNEMIUS_MEDIALIS = "Gastrocnemius Medialis"
    GASTROCNEMIUS_LATERALIS = "Gastrocnemius Lateralis"
    SOLEUS = "Soleus"
    TIBIALIS_ANTERIOR = "Tibialis Anterior"
    PERONEUS_LONGUS = "Peroneus Longus"
    FLEXOR_HALLUCIS_LONGUS = "Flexor Hallucis Longus"
    EXTENSOR_HALLUCIS_LONGUS = "Extensor Hallucis Longus"
    FLEXOR_DIGITORUM_LONGUS = "Flexor Digitorum Longus"
    EXTENSOR_DIGITORUM_LONGUS = "Extensor Digitorum Longus"

    # Upper limb muscles
    BICEPS_BRACHII = "Biceps Brachii"
    TRICEPS_BRACHII = "Triceps Brachii"
    DELTOID = "Deltoid"
    BRACHIALIS = "Brachialis"
    FLEXOR_CARPI_RADIALIS = "Flexor Carpi Radialis"
    FLEXOR_CARPI_ULNARIS = "Flexor Carpi Ulnaris"
    PALMARIS_LONGUS = "Palmaris Longus"
    EXTENSOR_CARPI_RADIALIS = "Extensor Carpi Radialis"
    EXTENSOR_CARPI_ULNARIS = "Extensor Carpi Ulnaris"
    EXTENSOR_DIGITORUM = "Extensor Digitorum"
    PRONATOR_TERES = "Pronator Teres"
    SUPINATOR = "Supinator"
    FLEXOR_DIGITORUM_SUPERFICIALIS = "Flexor Digitorum Superficialis"
    FLEXOR_DIGITORUM_PROFUNDUS = "Flexor Digitorum Profundus"
    LUMBAR_MULTIFIDUS = "Lumbar Multifidus"


class SelectionValueFileType(str, Enum):
    # Image types
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    TIFF = "tiff"
    TIF = "tif"
    GIF = "gif"
    WEBP = "webp"
    SVG = "svg"
    RAW = "raw"

    # Video types
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    MKV = "mkv"
    WMV = "wmv"
    FLV = "flv"
    WEBM = "webm"
    MPEG = "mpeg"
    MPG = "mpg"
    GP3 = "3gp"
    ASF = "asf"
    TVD = "tvd"

    # Volume types
    MHA = "mha"  # Medical imaging file format
    NRRD = "nrrd"  # Nearly Raw Raster Data
    DICOM = "dicom"  # Digital Imaging and Communications in Medicine
    NIFTI = "nifti"  # Neuroimaging Informatics Technology Initiative
    HDR = "hdr"  # Analyze format header file
    IMG = "img"  # Analyze format image file
    VTK = "vtk"  # Visualization Toolkit file format
    GIPL = "gipl"  # Guy's Image Processing Lab file format


class SelectionValueMuscleRegion(str, Enum):
    PROXIMAL = "Proximal"
    MIDDLE = "Middle"
    DISTAL = "Distal"
    WHOLE = "Whole"


class SelectionValueCaptureType(str, Enum):
    IMAGE = "Image"
    VIDEO = "Video"
    VOLUME = "Volume"


class SelectionValueImageType(str, Enum):
    STATIC = "Static"
    PANORAMIC = "Panoramic"


class SelectionValueImagePlane(str, Enum):
    LONGITUDINAL = "Longitudinal"
    TRANSVERSE = "Transverse"


class SelectionValueParticipantSex(str, Enum):
    FEMALE = "Female"
    MALE = "Male"
    BOTH = "Both"


class SelectionValueSoftwareLicense(str, Enum):
    MIT = "MIT License"
    APACHE_2 = "Apache License 2.0"
    GPL_2 = "GNU General Public License (GPL) 2.0"
    GPL_3 = "GNU General Public License (GPL) 3.0"
    LGPL_2_1 = "GNU Lesser General Public License (LGPL) 2.1"
    LGPL_3 = "GNU Lesser General Public License (LGPL) 3.0"
    BSD_2 = "BSD 2-Clause License (Simplified)"
    BSD_3 = "BSD 3-Clause License (Revised)"
    MPL_2 = "Mozilla Public License 2.0 (MPL 2.0)"
    ECLIPSE_2 = "Eclipse Public License 2.0"
    ARTISTIC_2 = "Artistic License 2.0"
    CC0 = "Creative Commons Zero v1.0 Universal (CC0)"
    CC_BY_4 = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
    CC_BY_SA_4 = (
        "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
    )
    UNLICENSE = "The Unlicense"
    PDDL = "Public Domain Dedication and License (PDDL)"
    AFL_3 = "Academic Free License v3.0"
    BOOST = "Boost Software License 1.0"
    ISC = "ISC License"
    ODC_BY = "Open Data Commons Attribution License (ODC-By)"
    ODBL = "Open Data Commons Open Database License (ODbL)"
    ODC_PDDL = "Open Data Commons Public Domain Dedication and License (PDDL)"


class SelectionValueUltrasoundDevice(str, Enum):
    # GE Healthcare
    GE_LOGIQ_E = "GE Logiq E"
    GE_LOGIQ_E9 = "GE Logiq E9"
    GE_LOGIQ_S8 = "GE Logiq S8"
    GE_LOGIQ_P9 = "GE Logiq P9"
    GE_LOGIQ_E10 = "GE Logiq E10"
    GE_VIVID_E95 = "GE Vivid E95"
    GE_VOLUSON_E10 = "BE Voluson e10"

    # Siemens Healthineers
    SIEMENS_JUNIPER = "Siemens Acuson Juniper"
    SIEMENS_S2000 = "Siemens Acuson S2000"
    SIEMENS_S3000 = "Siemens Acuson S3000"
    SIEMENS_SEQUOIA = "Siemens Acuson Sequoia"

    # Philips
    PHILIPS_AFFINITI_50 = "Philips Affiniti 50"
    PHILIPS_AFFINITI_70 = "Philips Affiniti 70"
    PHILIPS_EPIQ_5 = "Philips Epiq 5"
    PHILIPS_EPIQ_7 = "Philips Epiq 7"
    PHILIPS_LUMIFY = "Philips Lumify"
    PHILIPS_HD11 = "Philips HD11"

    # Esaote
    ESAOTE_MYLAB_25 = "Esaote MyLab 25 Gold"
    ESAOTE_MYLAB_50 = "Esaote MyLab 50"
    ESAOTE_MYLAB_60 = "Esaote MyLab 60"
    ESAOTE_MYLAB_70 = "Esaote MyLab 70"
    ESAOTE_MYLAB_9 = "Esaote MyLab 9 eXP"
    ESAOTE_MYLAB_X8 = "Esaote MyLab X8"
    ESAOTE_MYLAB_OMEGA = "Esaote MyLab Omega"
    ESAOTE_MYLAB_TWICE = "Esaote MyLab Twice"

    # BK Medical
    BK_FLEX_FOCUS_800 = "BK Medical Flex Focus 800"
    BK_PRO_FOCUS_2202 = "BK Medical Pro Focus 2202"

    # Canon/Toshiba
    CANON_APLIO_300 = "Canon Aplio 300"
    CANON_APLIO_400 = "Canon Aplio 400"
    CANON_APLIO_I800 = "Canon Aplio i800"
    CANON_XARIO_100G = "Canon Xario 100G"

    # Alpinion
    ALPINION_E_CUBE_7 = "Alpinion E-CUBE 7"
    ALPINION_E_CUBE_8 = "Alpinion E-CUBE 8"
    ALPINION_E_CUBE_15 = "Alpinion E-CUBE 15"

    # Aixplorer/Supersonic Imagine
    AIXPLORER_ULTIMATE = "Aixplorer Ultimate"
    AIXPLORER_MACH_30 = "Aixplorer Mach 30"
    AIXPLORER_MACH_20 = "Aixplorer Mach 20"
    AIXPLORER_V6 = "Aixplorer V6"

    # Mindray
    MINDRAY_RESONA_7 = "Mindray Resona 7"
    MINDRAY_DC_80 = "Mindray DC-80"
    MINDRAY_M9 = "Mindray M9"

    # Samsung
    SAMSUNG_HS50 = "Samsung HS50"
    SAMSUNG_RS80A = "Samsung RS80A"
    SAMSUNG_RS85 = "Samsung RS85 Prestige"

    # Hitachi/Fujifilm
    HITACHI_ARIETTA_70 = "Hitachi Arietta 70"
    HITACHI_NOBLUS = "Hitachi Noblus"
    HITACHI_ARIETTA_850 = "Hitachi Arietta 850"
    HITACHI_ALOKA_ALPHA10 = "Hitachi Aloka Alpha-10"
    HITACHI_ALOKA_SSD500 = "Hitachi Aloka SSD-5000 PHD"

    # Sonosite
    SONOSITE_EDGE_II = "Fujifilm Sonosite Edge II"
    SONOSITE_M_TURBO = "Fujifilm Sonosite M-Turbo"
    SONOSITE_S_SERIES = "Fujifilm Sonosite S Series"
    SONOSITE_XP = "Fujifilm Sonosite X-Porte"

    # Terason
    TERASON_USMART_3200T = "Terason uSmart 3200T"
    TERASON_USMART_3300 = "Terason uSmart 3300"

    # Zonare
    ZONARE_ZS3 = "Zonare ZS3"
    ZONARE_Z_ONE_PRO = "Zonare Z-One Pro"

    # Telemed
    TELEMED_ARTUS_EXT_1H = "Telemed ArtUs EXT-1H"
    TELEMED_ARTUS_EXT_2H = "Telemed ArtUs EXT-2H"
    TELEMED_MICRUS_PRO = "Telemed MicrUs Pro"
    TELEMED_SMARTUS_EXT = "Telemed SmartUs EXT"
    TELEMED_ECHO_BLASTER_128 = "Telemed Echo Blaster 128"
    TELEMED_LOGICSCAN_128 = "Telemed LogicScan 128"

    # S-Sharp
    S_SHARP_PRODIGY = "S-Sharp Prodigy"


# Define the schema using Pydantic
class DatasetMetadata(BaseModel):
    DATASET_NAME: str = Field(
        ...,
        description="Name of the dataset containing the name and the year separated by an underscore, e.g., 'DeepACSA_2022'.",
    )
    DOI: Optional[str] = Field(
        ..., description="Optional. Digital Object Identifier (DOI) of the dataset."
    )
    VERSION: str = Field(
        ...,
        regex=r"^\d+\.\d+(?:\.\d+)?$",
        description="Version of the dataset following semver principles (i.e., 1.0.0).",
    )
    MUSCLE: Set[SelectionValueMuscle] = Field(
        ...,
        description="List of muscles included in the dataset. Choose one or mulitple from the available options.",
    )
    MUSCLE_REGION: Set[SelectionValueMuscleRegion] = Field(
        ...,
        description="List of muscle regions (proximal, middle, distal). Choose one or mulitple from the available options.",
    )
    DEVICE: Set[SelectionValueUltrasoundDevice] = Field(
        ...,
        description="Optional. Ultrasound device used to collect the data. Choose one or mulitple from the available options.",
    )
    TRANSDUCER: Optional[str] = Field(
        ...,
        description="Optional. List of transducers used, separated by commas.",
    )
    DATA_TYPE: SelectionValueCaptureType = Field(
        ...,
        description="Type of data in the dataset (Images, Videos, Volumes). Choose one.",
    )
    FILE_TYPE: Set[SelectionValueFileType] = Field(
        ...,
        description="File type of the data (e.g., jpg, png, mp4). Choose one or multiple.",
    )
    IMAGE_TYPE: Set[SelectionValueImageType] = Field(
        ..., description="Image type (Static, Panoramic). Choose one or multiple."
    )
    IMAGE_NUMBER: Optional[int] = Field(
        None,
        ge=0,
        description="Optional. Number of images/videos in the dataset. Select value.",
    )
    VIDEO_NUMBER: Optional[int] = Field(
        None,
        ge=0,
        description="Optional. Number of videos in the dataset. Select value.",
    )
    DATA_PLANE: Set[SelectionValueImagePlane] = Field(
        ...,
        description="Plane in which the images/videos were collected (Transverse, Longitudinal). Choose one or multiple.",
    )
    SCANNING_FREQUENCY: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Optional. Scanning frequency in MHz (1-100). Select value.",
    )
    SAMPLING_RATE: Optional[int] = Field(
        None,
        ge=0,
        le=1000,
        description="Optional. Sampling rate or fps (0-200). Select value.",
    )
    PARTICIPANT_AGE: Optional[int] = Field(
        ...,
        ge=0,
        le=100,
        description="Optional. Mean age of participants (0-100). Select mean value.",
    )
    PARTICIPANT_HEIGHT: Optional[int] = Field(
        ...,
        ge=0,
        le=220,
        description="Optional. Mean height of participants in cm (0-220). Select mean value.",
    )
    PARTICIPANT_BODYMASS: Optional[int] = Field(
        ...,
        ge=0,
        le=200,
        description="Optional. Mean body mass of participants in kg (0-200). Select mean value.",
    )
    PARTICIPANT_SEX: SelectionValueParticipantSex = Field(
        ..., description="Sex of participants (Male, Female, Both). Choose one."
    )
    SAMPLE_SIZE: int = Field(
        ...,
        ge=0,
        description="Number of participants included in the dataset (minimum 1). Enter n.",
    )
    DATA_LABELS: bool = Field(
        ..., description="Whether labels are provided for the data. Select Checkbox."
    )
    DATA_LABELS_DESCRIPTION: Optional[str] = Field(
        ...,
        max_length=1000,
        description="Optional. Description of the labels provided. As detailed as necessary but as short as possible.",
    )
    SHORT_DESCRIPTION: str = Field(
        ...,
        max_length=5000,
        description="Brief description of the dataset (max 500 characters). As detailed as necessary but as short as possible.",
    )
    DATASET_YEAR: str = Field(
        ...,
        regex=r"^\d{4}$",
        description="Year the dataset was created (4-digit year).",
    )
    PUBLICATION_LINK: Optional[str] = Field(
        ..., description="Optional. URL Link to the publication containing the data."
    )
    DATASET_LINK: HttpUrl = Field(..., description="Link to the dataset.")
    AUTHORS: str = Field(
        ...,
        description="List of authors of the dataset, separated by commas.",
        max_length=1000,
    )
    CONTACT: str = Field(
        ...,
        description="List of contact emails of the authors, separated by commas.",
        max_length=500,
    )
    LICENSE: SelectionValueSoftwareLicense = Field(
        ..., description="License under which the data is shared."
    )

    @validator("DATASET_NAME", allow_reuse=True)
    def validate_dataset_name(cls, value):
        """
        Ensure the dataset name follows the format: DeepACSA_2022.
        """
        regex = r"^[A-Za-z0-9]+_[0-9]{4}$"
        if not re.match(regex, value.strip()):
            raise ValueError(
                f"Dataset name '{value}' is not in the correct format. It must be in the format 'Name_YYYY'."
            )
        return value

    @validator("TRANSDUCER", allow_reuse=True)
    def validate_transducer(cls, value: str) -> List[str]:
        """
        Validate and process the authors field.

        Ensure the field is not empty, and return a list of authors split by commas.
        """
        if not value.strip():
            return None
        # Split the input into a list of authors
        transducer = [trans.strip() for trans in value.split(",") if trans.strip()]
        if not transducer:
            raise ValueError(
                "Transducer field must contain at least one valid Transducer."
            )
        return transducer

    @validator("SCANNING_FREQUENCY", pre=True, always=True, allow_reuse=True)
    def interpret_zero_freq_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None
        return value

    @validator("SAMPLING_RATE", pre=True, always=True, allow_reuse=True)
    def interpret_zero_sr_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None
        return value

    @validator("IMAGE_NUMBER", pre=True, always=True, allow_reuse=True)
    def interpret_zero_sr_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None
        return value

    @validator("VIDEO_NUMBER", pre=True, always=True, allow_reuse=True)
    def interpret_zero_sr_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None
        return value

    @validator("PARTICIPANT_HEIGHT", pre=True, always=True, allow_reuse=True)
    def interpret_zero_height_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None

        if value is not None and value < 50:
            raise ValueError("Height is unusually low. Please check the input.")
        return value

    @validator("PARTICIPANT_BODYMASS", pre=True, always=True, allow_reuse=True)
    def interpret_zero_weight_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None

        if value is not None and value < 10:
            raise ValueError("Weight is unusually low. Please check the input.")
        return value

    @validator("PARTICIPANT_AGE", pre=True, always=True, allow_reuse=True)
    def interpret_zero_age_as_none(cls, value):
        """Interpret a value of 0 as None."""
        if value == 0:
            return None
        return value

    @validator("CONTACT", allow_reuse=True)
    def validate_emails(cls, value):
        """Validate comma-separated emails."""
        emails = [email.strip() for email in value.split(",")]
        for email in emails:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError(f"Invalid email address: {email}")
        return value

    @validator("AUTHORS", allow_reuse=True)
    def validate_authors(cls, value: str) -> List[str]:
        """
        Validate and process the authors field.

        Ensure the field is not empty, and return a list of authors split by commas.
        """
        if not value.strip():
            raise ValueError("Authors field cannot be empty.")
        # Split the input into a list of authors
        authors = [author.strip() for author in value.split(",") if author.strip()]
        if not authors:
            raise ValueError("Authors field must contain at least one valid author.")
        return authors

    @validator("SHORT_DESCRIPTION", allow_reuse=True)
    def validate_description(cls, value):
        """Ensure the description is not empty."""
        if not value.strip():
            raise ValueError("Short description cannot be empty.")
        return value

    @validator("DOI", allow_reuse=True)
    def validate_doi(cls, value: str) -> str:
        """Ensure DOI matches the correct pattern."""
        if value is not None and value.strip():  # Check if value is not None or empty
            regex = r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$"
            if not re.match(regex, value.strip()):
                raise ValueError(f"DOI '{value}' is not in a valid format.")
        return value

    @validator("PUBLICATION_LINK", allow_reuse=True)
    def validate_publication_link(cls, value: str) -> str:
        """Ensure PUBLICATION_LINK is a valid URL."""
        if value is not None and value.strip():  # Check if value is not None or empty
            regex = (
                r"^(https?|ftp):\/\/"  # Protocol
                r"(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}"  # Domain
                r"|localhost"  # Allow localhost
                r"|((\d{1,3}\.){3}\d{1,3}))"  # IP Address
                r"(:\d+)?(\/[-A-Za-z0-9@:%_+.~#?&/=]*)?$"  # Port and path
            )
            if not re.match(regex, value.strip()):
                raise ValueError(
                    f"Publication link '{value}' is not in a valid format."
                )
        return value

    @validator("DATASET_LINK", allow_reuse=True)
    def validate_dataset_link(cls, value: str) -> str:
        """Ensure DATASET_LINK is a valid URL."""
        # Regular expression to validate a proper URL (if HttpUrl is not enough)
        regex = (
            r"^(https?|ftp):\/\/"  # Protocol
            r"(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}"  # Domain
            r"|localhost"  # Allow localhost
            r"|((\d{1,3}\.){3}\d{1,3}))"  # IP Address
            r"(:\d+)?(\/[-A-Za-z0-9@:%_+.~#?&/=]*)?$"  # Port and path
        )
        if not re.match(regex, value.strip()):
            raise ValueError(f"Dataset link '{value}' is not in a valid format.")
        return value
