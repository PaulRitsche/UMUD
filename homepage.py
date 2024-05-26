import streamlit as st
from deta import Deta
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO
import os

# Read Deta Project Key from environment variable
DETA_PROJECT_KEY = "bLbnQSkX_JNprytFEx1rVKBSdWRZRj19qtmxXMgHs"

if not DETA_PROJECT_KEY:
    st.error(
        "Deta Project Key not found. Please set the DETA_PROJECT_KEY environment variable."
    )
    st.stop()

# Initialize Deta
deta = Deta(DETA_PROJECT_KEY)
db = deta.Base("muscle_ultrasound_metadata")

# Example data
example_data = [
    {
        "muscle": "Biceps",
        "image_type": "Type1",
        "device": "DeviceA",
        "age": 25,
        "sex": "Male",
        "height": 180,
        "weight": 75,
        "dataset_link": "https://example.com/dataset1",
    },
    {
        "muscle": "Triceps",
        "image_type": "Type2",
        "device": "DeviceB",
        "age": 30,
        "sex": "Female",
        "height": 165,
        "weight": 60,
        "dataset_link": "https://example.com/dataset2",
    },
    {
        "muscle": "Quadriceps",
        "image_type": "Type3",
        "device": "DeviceC",
        "age": 40,
        "sex": "Male",
        "height": 175,
        "weight": 80,
        "dataset_link": "https://example.com/dataset3",
    },
]

# Populate the database
for data in example_data:
    db.put(data)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        color: #000000;
    }
    .sidebar .sidebar-content {
        background-color: #004466;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #004466;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("Universal Muscle Ultrasound Repository")

# Tabs for dataset selection and scoreboard
tab1, tab2 = st.tabs(["Select and Download Datasets", "Scoreboard"])

# Tab 1: Select and Download Datasets
with tab1:
    st.header("Search Ultrasound Datasets")
    muscle = st.selectbox(
        "Muscle", ["Any"] + [item["muscle"] for item in db.fetch().items]
    )
    image_type = st.selectbox("Image Type", ["Any", "Type1", "Type2", "Type3"])
    device = st.text_input("Device")
    age = st.number_input("Age", min_value=0, max_value=120, value=0)
    sex = st.selectbox("Sex", ["Any", "Male", "Female"])
    height = st.number_input("Height (cm)", min_value=0, value=0)
    weight = st.number_input("Weight (kg)", min_value=0, value=0)

    # Search button
    if st.button("Search"):
        query = {}
        if muscle != "Any":
            query["muscle"] = muscle
        if image_type != "Any":
            query["image_type"] = image_type
        if device:
            query["device"] = device
        if age > 0:
            query["age"] = age
        if sex != "Any":
            query["sex"] = sex
        if height > 0:
            query["height"] = height
        if weight > 0:
            query["weight"] = weight

        results = db.fetch(query).items
        if results:
            st.write("Search Results:")
            for item in results:
                st.json(item)
                st.markdown(f"[Download Dataset]({item['dataset_link']})")
        else:
            st.write("No matching datasets found.")

# Tab 2: Scoreboard
with tab2:
    st.header("Challenge")

    # Challenge dataset
    challenge_dataset_link = "https://example.com/challenge_dataset"
    st.markdown(f"[Download Challenge Dataset]({challenge_dataset_link})")

    # Upload results
    uploaded_file = st.file_uploader("Upload your results (CSV format)", type="csv")
    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        st.write("Uploaded Results")
        st.write(uploaded_df)

        # Save uploaded results
        results_buffer = BytesIO()
        uploaded_df.to_csv(results_buffer, index=False)
        results_key = f"results_{st.session_state.get('run_id', 1)}.csv"
        deta.Drive("challenge_results").put(results_key, results_buffer.getvalue())
        st.success("Results uploaded successfully!")

    # Scoreboard
    st.header("Scoreboard")
    validation_set = pd.read_csv(
        "validation_set.csv"
    )  # Placeholder for the actual validation set
    st.write("Validation Set")
    st.write(validation_set)

    # Compare uploaded results with validation set
    if uploaded_file is not None:
        comparison = uploaded_df.compare(validation_set)
        st.write("Comparison with Validation Set")
        st.write(comparison)
