
import streamlit as st
from templates.template_dictionary import template_data
from helpers.loading_functions import load_dua, get_data


st.set_page_config(page_title="Datasets", page_icon="📊")
# Horizontal line separator

st.markdown(
    "<h1 style='text-align: center; '>Universal Musculoskeletal Ultrasound Database</h1>",
    unsafe_allow_html=True,
)

st.markdown("---")

# Intro section with concise and readable text
st.markdown(
    """
    <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px">
        <h4 style="text-align: center;">Explore Muscle Ultrasound Datasets</h4>
        <p style="text-align: center;">
            Use this tab to query datasets by applying specific metadata filters. Select the relevant filters, input the values, and retrieve datasets that meet your criteria.
            Choose the filters you want to apply from the list below. You can apply multiple filters for more precise results.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# Section for selecting filters
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("##### Select Metadata Filters")

# Filter options
filter_options = list(template_data[0].keys())
selected_filters = st.multiselect(
    "", filter_options, help="Select the filters you want to use."
)

if len(selected_filters) > 0:

    # Create a form for inputting filter values
    with st.form("entry_form", clear_on_submit=False):

        st.markdown("##### Enter Filter Values")
        filter_inputs = {}

        for key in selected_filters:
            input_type = template_data[0].get("type", "str")

            # Fetch unique values from the database
            items = get_data()
            unique_values = items.distinct(key)

            # Dynamically render the input type for each filter
            if input_type == "str":
                filter_inputs[key] = st.selectbox(key, options=unique_values)
            elif input_type == "int":
                filter_inputs[key] = st.selectbox(key, options=unique_values)
            elif input_type == "float":
                filter_inputs[key] = st.selectbox(key, options=unique_values)
            elif input_type == "bool":
                filter_inputs[key] = st.checkbox(key)
            elif input_type == "list":
                filter_inputs[key] = st.multiselect(key, options=unique_values)

        # Horizontal separator
        st.markdown("---")

        # Data Usage Agreement section in an expander
        with st.expander("Data Usage Agreement", expanded=False):
            st.markdown(load_dua())  # Display DUA content

        # Warning and submit button
        st.warning(
            "By submitting, you agree to the Data Usage Agreement.",
        )

        # Primary action button
        submitted = st.form_submit_button("Submit Query", type="primary")

        # Horizontal line separator
        st.markdown("---")

        if submitted:

            items = get_data()
            query = {k: v for k, v in filter_inputs.items() if v}

            st.markdown("##### Formed Query")
            st.json(query)
            results = items.find(query)

            if results:
                st.markdown("##### Dataset Links and Descriptions:")
                for result in results:
                    link = result.get("DATASET_LINK", "No link available")
                    description = result.get(
                        "SHORT_DESCRIPTION", "No description available"
                    )
                    # Display the link and its corresponding description
                    st.markdown(f"- **[{link}]({link})**")
                    st.markdown(f"  {description}")
            else:
                st.write("No datasets found for the selected criteria.")