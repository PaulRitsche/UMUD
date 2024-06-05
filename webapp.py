import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd

# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"
# st.session_state.query = {"muscle": "", "image_type": "", "device": "", "age": ""}
# st.session_state.link = {"dataset_link": ""}
muscles = ["Gastrocnemius Medialis", "Vastus Lateralis", "Vastus Medialis"]
image_types = ["all", ".tiff", ".jpeg", ".png"]
devices = ["all", "Siemens", "Philips", "GE"]

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
    connection_string = st.secrets.mongo["CONNECTION_STRING"]
    return pymongo.MongoClient(connection_string, tls=True)


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource(ttl=600)
def get_data():
    client = init_connection()
    db = client.muscle_ultrasound
    items = db.datasets
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
    st.write("The database is hosted on MongoDB Atlas.")
    st.write(
        "The database contains metadata for all included datasets, in my mind from images, videos and 3DUS."
    )
    st.write(
        "The database is currently not publicly available, but the datasets will be."
    )
    st.write(
        "Who to approach, index all images or just the datasets, only labeled datasets??"
    )
    st.write("LICENSE!!!!!!!!")


elif selected_tab == "Datasets":

    st.header("Enter Metadata:")
    with st.form("entry_form", clear_on_submit=False):

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
            items = get_data()

            # Form query for MongoDB

            query = {"muscle": muscle_select}
            if image_types_select != "all":
                query["image_type"] = image_types_select
            if devices_select != "all":
                query["device"] = devices_select
            if age_select != 0:
                query["age"] = age_select

            # Filter data
            print(query)
            results = items.find(query)

            # Collect dataset links
            dataset_links = [result["dataset_link"] for result in results]
            print(dataset_links)
            # Display dataset links
            st.write("### Dataset Links:")
            st.text_area("Link Return Field", "\n".join(dataset_links))

            # TODO include database filtering

elif selected_tab == "Database":

    st.header("Database")

    items = get_data()
    df = pd.DataFrame(items.find({}))
    unique_muscles = df["muscle"].unique().tolist()
    selected_muscle = st.multiselect("", unique_muscles)
    if selected_muscle:
        df = df[df["muscle"].isin(selected_muscle)]
    st.write(df)

    # TODO make a filterable dataframe for databse exploration https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
    st.write(
        "Description of the database and all included datasets in form of interactive table."
    )

    "---"


else:
    st.header("Challenge")

    # User upload section

    st.write("The idea is to propose a challenge for the community.")
    st.write(
        "The challenge will be to create a model (or any analysis script) to predict the muscle parameters in an unseen test set."
    )
    st.write(
        "I would suggest to use kaggle competition format. The results could be communicated in a workshop at the ECSS, ISB..."
    )

    # st.header("Upload Your Results")
    # uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Scoreboard #TODO this should also be fed by the database
    st.header("Scoreboard")

    st.write("Upload or Email?!")

    results = pd.DataFrame(
        {
            "Name": ["Neil", "Olivier", "Paul"],
            "Model IoU": [1, 0.9, 0.8],
            "Model Dice": [0.9, 0.8, 0.7],
            "SEM Fascicle Length": [0.1, 0.5, 0.7],
            "SEM Pennation Angle": [0.1, 0.5, 0.7],
            "SEM Muscle Thickness": [0.1, 0.5, 0.7],
        }
    )

    st.write(
        results
    )  # TODO use st_aggrid to improve table look https://medium.com/@nikolayryabykh/enhancing-your-streamlit-tables-with-aggrid-advanced-tips-and-tricks-250d4b57903
    # TODO check out PyGWalker as well
