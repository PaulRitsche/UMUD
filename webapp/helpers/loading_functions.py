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
        str(Path(__file__).with_name("webapp_files")) + "/usage_agreement.txt", "r"
    ) as file:
        return file.read()


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
    # items = list(items)  # make hashable for st.cache_data
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