import streamlit as st
from streamlit_option_menu import option_menu
import pymongo

# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"
st.session_state.query = ""
st.session_state.link = {"dataset_link": ""}
muscles = ["Gastrocnemius Medialis", "Vastus Lateralis", "Vastus Medialis"]
image_types = ["tiff", "jpeg", "png"]
devices = ["Siemens", "Philips", "GE"]

# --------------------

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
)
st.title("Universal Muscle Ultrasound Repository" + " " + page_icon)


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    username = st.secrets.mongo["username"]
    password = st.secrets.mongo["password"]
    return pymongo.MongoClient(
        f"mongodb+srv://{username}:{password}@umud.jmbqpo0.mongodb.net/?retryWrites=true&w=majority&appName=UMUD"
    )


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource(ttl=600)
def get_data():
    db = client.muscle_ultrasound
    items = db.metadata
    # items = list(items)  # make hashable for st.cache_data
    return items


# Specify tabs
selected_tab = option_menu(
    "",
    options=["Home", "Datasets", "Database", "Challenge"],
    icons=["house", "file-earmark-bar-graph", "archive", "trophy"],
    default_index=0,
    orientation="horizontal",
)

if selected_tab == "Home":
    st.header("Home")
    st.write("Welcome to the UMUD repository!")

elif selected_tab == "Datasets":

    st.header("Enter Metadata:")
    with st.form("entry_form", clear_on_submit=True):

        # Muscle selection
        muscle_select = st.selectbox("muscle", muscles)
        # Image types
        image_types_select = st.selectbox("image_type", image_types)
        # device list
        devices_select = st.selectbox("device", devices)
        # Age range
        age_select = st.number_input(
            "age", min_value=0, max_value=120, format="%i", step=10
        )

        "---"
        # Submit button
        submitted = st.form_submit_button("Submit Query")
        if submitted:
            client = init_connection()
            items = get_data()

            # Form query for MongoDB
            st.session_state.query = {
                "muscle": muscle_select,
                "image_type": image_types_select,
                "device": muscle_select,
                "age": age_select,
            }

            # Filter data
            st.session_state.link = items.find_one(
                {"muscle": st.session_state.query["muscle"]}
            )
            # TODO include database filtering
        "---"
        # Text area for link return
        st.text_area("Link Return Field", st.session_state.link["dataset_link"])

elif selected_tab == "Database":
    st.header("Database")
    st.write("Coming soon!")

else:
    st.header("Challenge")

    # User upload section
    st.header("Upload Your Results")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


# use st.chache_resoure for databse connection as this will store the db and dont relaod it everytime
# Print results.
