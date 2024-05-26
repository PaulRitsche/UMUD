import streamlit as st
from streamlit_option_menu import option_menu

# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"
st.session_state.query = ""
muscles = ["Gastrocnemius Medialis", "Vastus Lateralis", "Vastus Medialis"]
image_types = ["tif", "jped", "png"]
devices = ["Siemens", "Philips", "GE"]

# --------------------

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
)
st.title("Universal Muscle Ultrasound Repository" + " " + page_icon)


# Specify tabs
selected_tab = option_menu(
    "Menu",
    options=["Home", "Repository", "Challenge"],
    icons=["house", "archive", "trophy"],
    default_index=0,
    orientation="horizontal",
)

if selected_tab == "Home":
    st.header("Home")
    st.write("Welcome to the UMUD repository!")

elif selected_tab == "Repository":

    st.header("Metadata")
    with st.form("entry_form", clear_on_submit=True):

        "---"
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
            # Form query for MongoDB
            st.session_state.query = {
                "muscle": muscle_select,
                "image_type": image_types_select,
                "device": muscle_select,
                "age": age_select,
            }

            # TODO include database filtering
        "---"
        # Text area for link return
        st.text_area("Link Return Field", value=st.session_state.query)

else:
    st.header("Challenge")
    st.write("Coming soon!")


# use st.chache_resoure for databse connection as this will store the db and dont relaod it everytime
