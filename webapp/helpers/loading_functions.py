from pathlib import Path
import streamlit as st
import pymongo


def load_dua():
    """
    Load the data usage agreement from file.

    Returns
    -------
    str
        Data usage agreement as a string.
    """
    with open(
        str(Path(__file__).resolve().parent.parent / "webapp_files" / "usage_agreement.txt"), "r"
    ) as file:
        return file.read()


def read_newsfeed(filepath):
    """
    Reads news items from a text file and returns them as a list of strings.

    Parameters
    ----------
    filepath : str
        The path to the newsfeed text file.

    Returns
    -------
    list
        A list of news items as strings.
    """
    try:
        with open(filepath, "r") as file:
            news_items = file.readlines()
        return [item.strip() for item in news_items]
    except Exception as e:
        st.error(f"Error reading newsfeed: {e}")
        return []


# Currently Not Used
def load_scoreboard():
    """
    Load the scoreboard data.

    Returns
    -------
    pandas.DataFrame
        A dataframe containing the scoreboard data.
    """

    # This function should be modified to load data from database if needed.
    results = pd.DataFrame(
        {
            "Name": ["Neil", "Olivier", "Paul"],
            "SEM Fascicle Length (cm)": [0.1, 0.5, 0.7],
            "SEM Pennation Angle (cm)": [0.1, 0.5, 0.7],
            "SEM Muscle Thickness (cm)": [0.1, 0.5, 0.7],
        }
    )
    return results


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource(ttl=600)
def get_data():
    """
    Pull data from the MongoDB collection.

    Returns
    -------
    pymongo.collection.Collection
        A MongoDB collection instance containing the datasets.
    """
    client = init_connection()
    db = client.muscle_ultrasound
    items = db.datasets
    return items


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    """
    Initialize connection to MongoDB.

    Returns
    -------
    pymongo.MongoClient
        A MongoDB client instance.
    """
    connection_string = st.secrets.mongo["CONNECTION_STRING"]
    return pymongo.MongoClient(connection_string, tls=True)