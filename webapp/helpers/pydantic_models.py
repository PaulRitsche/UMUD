
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


class SelectionValueMuscleRegion(str, Enum):
    PROXIMAL = "proximal"
    MIDDLE = "middle"
    DISTAL = "distal"


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
    CC_BY_SA_4 = "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
    UNLICENSE = "The Unlicense"
    PDDL = "Public Domain Dedication and License (PDDL)"
    AFL_3 = "Academic Free License v3.0"
    BOOST = "Boost Software License 1.0"
    ISC = "ISC License"
    ODC_BY = "Open Data Commons Attribution License (ODC-By)"
    ODBL = "Open Data Commons Open Database License (ODbL)"
    ODC_PDDL = "Open Data Commons Public Domain Dedication and License (PDDL)"

class SelectionValueUltrasoundDevice(str, Enum):
    GE_LOGIQ_E9 = "GE Logiq E9"
    GE_LOGIQ_S8 = "GE Logiq S8"
    GE_LOGIQ_P9 = "GE Logiq P9"
    SIEMENS_JUNIPER = "Siemens Acuson Juniper"
    SIEMENS_S2000 = "Siemens Acuson S2000"
    SIEMENS_S3000 = "Siemens Acuson S3000"
    PHILIPS_AFFINITI_50 = "Philips Affiniti 50"
    PHILIPS_AFFINITI_70 = "Philips Affiniti 70"
    PHILIPS_EPIQ_5 = "Philips Epiq 5"
    PHILIPS_EPIQ_7 = "Philips Epiq 7"
    ESAOTE_MYLAB_25 = "Esaote MyLab 25 Gold"
    ESAOTE_MYLAB_50 = "Esaote MyLab 50"
    ESAOTE_MYLAB_9 = "Esaote MyLab 9 eXP"
    BK_FLEX_FOCUS_800 = "BK Medical Flex Focus 800"
    BK_PRO_FOCUS_2202 = "BK Medical Pro Focus 2202"
    CANON_APLIO_300 = "Canon Aplio 300"
    CANON_APLIO_400 = "Canon Aplio 400"
    CANON_APLIO_I800 = "Canon Aplio i800"
    ALPINION_E_CUBE_7 = "Alpinion E-CUBE 7"
    ALPINION_E_CUBE_8 = "Alpinion E-CUBE 8"
    MINDRAY_RESONA_7 = "Mindray Resona 7"
    MINDRAY_DC_80 = "Mindray DC-80"
    SAMSUNG_HS50 = "Samsung HS50"
    SAMSUNG_RS80A = "Samsung RS80A"
    HITACHI_ARIETTA_70 = "Hitachi Arietta 70"
    HITACHI_NOBLUS = "Hitachi Noblus"
    SONOSITE_EDGE_II = "Fujifilm Sonosite Edge II"
    SONOSITE_M_TURBO = "Fujifilm Sonosite M-Turbo"
    TERASON_USMART_3200T = "Terason uSmart 3200T"
    ZONARE_ZS3 = "Zonare ZS3"
    TELEMED_ARTUS_EXT_1H = "Telemed ArtUs EXT-1H"
    TELEMED_ARTUS_EXT_2H = "Telemed ArtUs EXT-2H"
    TELEMED_MICRUS_PRO = "Telemed MicrUs Pro"
    TELEMED_SMARTUS_EXT = "Telemed SmartUs EXT"
    TELEMED_ECHO_BLASTER_128 = "Telemed Echo Blaster 128"
    TELEMED_LOGICSCAN_128 = "Telemed LogicScan 128"
    TELEMED_VOLUSON_E10 = "Telemed Voluson e10"

# Define the schema using Pydantic


class DatasetMetadata(BaseModel):
    DATASET_NAME: str = Field(
        ...,
        description="Name of the dataset containing the name and the year separated by an underscore, e.g., 'DeepACSA_2022'.",
    )
    DOI: Optional[str] = Field(
        ...,
        description="Digital Object Identifier (DOI) of the dataset.",
        regex=r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$",
    )
    VERSION: str = Field(
        ..., regex=r"^\d+\.\d+(?:\.\d+)?$", description="Version of the dataset."
    )
    MUSCLE: Set[SelectionValueMuscle] = Field(
        ..., description="List of muscles included in the dataset."
    )
    MUSCLE_REGION: Set[SelectionValueMuscleRegion] = Field(
        ..., description="List of muscle regions (proximal, middle, distal)."
    )
    DEVICE: Optional[SelectionValueUltrasoundDevice] = Field(
        ..., description="Ultrasound device used to collect the data."
    )
    PROBE: Optional[str] = Field(
        ..., description="Model of the probe used during data collection."
    )
    DATA_TYPE: SelectionValueCaptureType = Field(
        ..., description="Type of data in the dataset (Images, Videos, Volumes)."
    )
    FILE_TYPE: SelectionValueFileType = Field(
        ..., description="File type of the data (e.g., jpg, png, mp4)."
    )
    IMAGE_TYPE: SelectionValueImageType = Field(
        ..., description="Image type (Static, Panoramic)."
    )
    DATA_PLANE: SelectionValueImagePlane = Field(
        ..., description="Plane in which the images/videos were collected."
    )
    PARTICIPANT_AGE: float = Field(
        ..., ge=0, le=100, description="Mean age of participants (0-100)."
    )
    PARTICIPANT_HEIGHT: float = Field(
        ..., ge=0, le=220, description="Mean height of participants in cm (0-220)."
    )
    PARTICIPANT_WEIGHT: float = Field(
        ..., ge=0, le=200, description="Mean weight of participants in kg (0-200)."
    )
    PARTICIPANT_SEX: SelectionValueParticipantSex = Field(
        ..., description="Sex of participants (Male, Female, Both)."
    )
    SAMPLE_SIZE: int = Field(
        ...,
        ge=1,
        description="Number of participants included in the dataset (minimum 1).",
    )
    DATA_LABELS: bool = Field(
        ..., description="Whether labels are provided for the data."
    )
    DATA_LABELS_DESCRIPTION: Optional[str] = Field(
        None, description="Description of the labels provided."
    )
    SHORT_DESCRIPTION: str = Field(
        ...,
        max_length=500,
        description="Brief description of the dataset (max 500 characters).",
    )
    DATASET_YEAR: str = Field(
        ...,
        regex=r"^\d{4}$",
        description="Year the dataset was created (4-digit year).",
    )
    PUBLICATION_LINK: Optional[str] = Field(
        ..., description="Link to the publication containing the data."
    )
    AUTHORS: str = Field(
        ...,
        description="List of authors of the dataset, separated by commas.",
        max_length=500,
    )
    CONTACT: str = Field(
        ...,
        description="List of contact emails of the authors, separated by commas.",
        max_length=500,
    )
    DATASET_LINK: HttpUrl = Field(..., description="Link to the dataset.")
    LICENSE: SelectionValueSoftwareLicense = Field(..., description="License under which the data is shared.")
    SCANNING_FREQUENCY: Optional[int] = Field(
        None, ge=1, le=100, description="Scanning frequency in Hz (1-100)."
    )
    SAMPLING_RATE: Optional[int] = Field(
        None, ge=0, le=200, description="Sampling rate or fps (0-200)."
    )

    @validator("CONTACT", allow_reuse=True)
    def validate_emails(cls, value):
        """Validate comma-separated emails."""
        emails = [email.strip() for email in value.split(",")]
        for email in emails:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError(f"Invalid email address: {email}")
        return value

    @validator("AUTHORS", allow_reuse=True)
    def validate_authors(cls, value):
        """Ensure authors field is not empty."""
        if not value.strip():
            raise ValueError("Authors field cannot be empty.")
        return value

    @validator("SHORT_DESCRIPTION", allow_reuse=True)
    def validate_description(cls, value):
        """Ensure the description is not empty."""
        if not value.strip():
            raise ValueError("Short description cannot be empty.")
        return value