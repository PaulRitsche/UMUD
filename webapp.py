import streamlit as st

# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"


# --------------------

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
)
st.title("Universal Muscle Ultrasound Repository" + " " + page_icon)

# Input fields
muscles = ["Gastrocnemius Medialis", "Vastus Lateralis", "Vastus Medialis"]
image_types = ["tif", "jped", "png"]
devices = ["Siemens", "Philips", "GE"]


entry_dict = {
    "muscle": ["Gastrocnemius Medialis", "Vastus Lateralis", "Vastus Medialis"],
    "image_type": ["tif", "jped", "png"],
    "device": ["Siemens", "Philips", "GE"],
}

st.header("Metadata")
with st.form("entry_form", clear_on_submit=True):

    "---"
    muscle_select = st.selectbox("muscle", muscles)
    "---"
    image_types_select = st.selectbox("image_type", image_types)
    "---"
    devices_select = st.selectbox("device", devices)
    "---"
    age_select = st.number_input(
        "age", min_value=0, max_value=120, format="%i", step=10
    )
    "---"
    st.text_area("Link Return Field")

    submitted = st.form_submit_button("Submit Query")
    if submitted:

        st.write(muscle_select)
        st.write(image_types_select)
        st.write(devices_select)


# use st.chache_resoure for databse connection as this will store the db and dont relaod it everytime
