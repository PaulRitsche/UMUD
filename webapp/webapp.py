import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import urllib.parse
import os
import json
import ast
from templates.template_dictionary import template_data


def clean_dataframe(df):
    """
    Clean the dataframe to ensure all data is properly encoded and formatted.
    """
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = (
            df[col]
            .astype(str)
            .apply(lambda x: x.encode("utf-8", "ignore").decode("utf-8", "ignore"))
        )
    return df


def get_categorical_columns(df):
    """
    Identify all categorical columns in the dataframe.
    """
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def load_scoreboard():
    # This function should be modified to load data from your database if needed.
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
    return results


def display_scoreboard(df):
    """
    Display the scoreboard using st_aggrid for better visualization.
    """
    # Add medals to the top three rows
    medals = ["🥇", "🥈", "🥉"] + [""] * (len(df) - 3)
    df.insert(0, "Medal", medals)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False, groupable=True)
    gb.configure_side_bar()
    grid_options = gb.build()
    AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)


def filter_dataframe(df):
    """
    Display an interactive, filterable dataframe using st_aggrid and provide a download button.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_default_column(editable=True, groupable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_side_bar()
    grid_options = gb.build()
    grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)
    return grid_response["data"]


def display_charts(df, selected_plots, group_by_column):
    """
    Display interactive charts based on the dataframe and user selections.
    """
    st.subheader("Interactive Charts")

    for plot in selected_plots:
        if plot == "Muscle Distribution":
            fig, ax = plt.subplots()
            muscle_count = (
                df.groupby(group_by_column)["MUSCLE"]
                .value_counts()
                .unstack()
                .plot(kind="bar", stacked=True, ax=ax)
            )
            ax.set_title("Muscle Distribution")
            ax.set_xlabel(group_by_column)
            ax.set_ylabel("Count")
            st.pyplot(fig)

        elif plot == "Age Distribution" and "PARTICIPANT_AGE" in df.columns:
            fig, ax = plt.subplots()
            df.groupby(group_by_column)["PARTICIPANT_AGE"].plot(
                kind="hist", bins=20, alpha=0.5, ax=ax
            )
            ax.set_title("Age Distribution")
            ax.set_xlabel("Age")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)


def get_download_button(df, filename="filtered_data.csv"):
    """
    Generate a link to download the filtered dataframe as a CSV file.
    """
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return st.download_button(
        label="Download Filtered Data as CSV",
        data=buffer,
        file_name=filename,
        mime="text/csv",
    )


def create_email_link(subject, body, recipient, filenames):
    """
    Create a mailto link with the given subject, body, recipient, and filenames.
    """
    body += "\n\nAttachments:\n" + "\n".join(filenames)
    params = {"subject": subject, "body": body, "to": recipient}
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    mailto_link = f"mailto:?{query_string}"
    return mailto_link


def get_download_link(content, filename, mime):
    """
    Generate a link to download the given content as a file.
    """
    b64 = base64.b64encode(content.encode()).decode()  # Convert to base64
    href = f'<a href="data:{mime};base64,{b64}" download="{filename}">Download detailed instructions...</a>'
    return href


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
st.title("Universal Muscle Ultrasound Database" + " " + page_icon)


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

    st.markdown(
        """
    <div style="text-align: center;">
        <h2>Welcome to the UMUD Repository!</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    ### About UMUD
    The **UMUD repository** is a comprehensive database hosted on MongoDB Atlas. It contains metadata for a wide range of datasets, including images, videos, and 3D ultrasound (3DUS) data. Our mission is to provide an accessible platform for researchers and developers to access and utilize this data for various purposes, including model training and medical research.
    """
    )

    st.markdown(
        """
    ### Current Status
    - **Database Accessibility**: The database is currently not publicly available, but the datasets will be.
    - **Metadata Information**: Contains detailed metadata for all included datasets.
    """
    )

    st.markdown(
        """
    ### Features
    - 📁 **Variety of Data**: Includes images, videos, and 3DUS data.
    - 🏷️ **Labeled Datasets**: Focus on datasets that include labels for better training and validation.
    - 🔍 **Metadata Indexing**: Comprehensive indexing of metadata for easy search and retrieval.
    """
    )

    st.markdown(
        """
    ### Contact Us
    For any questions or inquiries, please contact our support team.
    """
    )

    # License section with GPL-3.0 license
    st.markdown(
        """
    ### License
    The UMUD repository and datasets are licensed under the **[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)**. You are free to:
    - **Share**: Copy and redistribute the material in any medium or format.
    - **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially.

    Under the following terms:
    - **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
    - **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
    """
    )

    # Contributing section
    st.markdown(
        """
    ### Contributing
    We welcome contributions from the community! Here are some ways you can contribute:
    - **Data Contributions**: If you have relevant datasets that you would like to share, please get in touch with us.
    - **Code Contributions**: Help us improve the repository by contributing to the codebase.
    - **Feedback**: Provide feedback on the existing datasets and features, and suggest improvements.

    To contribute, please contact us at [contribute@umudrepository.org](mailto:contribute@umudrepository.org) or visit our [GitHub repository](https://github.com/UMUD-repo) for more information.
    """
    )

    # Future plans section
    st.markdown(
        """
    ### Future Plans
    We are continuously working on expanding the repository and making it publicly accessible. Stay tuned for updates!
    """
    )

    # Closing message
    st.markdown(
        """
    <div style="text-align: center;">
        <h4>Thank you for visiting the UMUD Repository!</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )


elif selected_tab == "Datasets":

    st.header("🔍 Enter Metadata to Query Datasets")

    # Allow users to select which filters they want to use
    st.markdown("#### Select Filters to Apply")
    filter_options = list(template_data[0].keys())
    selected_filters = st.multiselect(
        "Select Filters", filter_options, help="Select which filters you want to apply."
    )

    # Create a form for user input
    with st.form("entry_form", clear_on_submit=True):
        st.markdown("#### Provide Filter Values")
        filter_inputs = {}

        for key in selected_filters:
            # description = template_data[0][key].get(
            #     "description", "No description available"
            # )
            input_type = template_data[0].get("type", "str")

            # st.markdown(f"**{key}**")
            # st.popover(description)

            # Fetch unique values for the field from the database
            items = get_data()
            unique_values = items.distinct(key)

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

        "---"
        submitted = st.form_submit_button("Submit Query")

        if submitted:
            items = get_data()
            query = {k: v for k, v in filter_inputs.items() if v}

            st.markdown("#### Formed Query")
            st.json(query)
            results = items.find(query)

            dataset_links = [result["DATASET_LINK"] for result in results]
            dataset_descriptions = results.distinct("SHORT_DESCRIPTION")

            if dataset_links:
                st.markdown("### Dataset Links:")
                for link in dataset_links:
                    st.markdown(f"- [{link}]({link})")

                if dataset_descriptions:
                    st.markdown(f"  {', '.join(dataset_descriptions)}")

                else:
                    st.write("No dataset descriptions found for the selected criteria.")
            else:
                st.write("No datasets found for the selected criteria.")

            # if dataset_links:
            #     st.download_button(
            #         label="Download Dataset Links",
            #         data="\n".join(dataset_links),
            #         file_name="dataset_links.txt",
            #         mime="text/plain",
            #     )

elif selected_tab == "Database":

    st.header("Database")

    items = get_data()
    df = pd.DataFrame(items.find({}))

    if df.empty:
        st.write("No data available in the database.")

    # Clean the dataframe
    df = clean_dataframe(df)

    # Display filtered dataframe with filtering capabilities
    st.subheader("Dataset Overview")
    filtered_df = filter_dataframe(df)
    with st.expander("Filtered Data to download...", expanded=False):
        st.write(filtered_df)
        # Add download button for the filtered dataframe
        get_download_button(filtered_df)

    # Dropdown for plot selection
    st.subheader("Interactive Charts")
    plot_options = ["Muscle Distribution", "Age Distribution"]
    selected_plots = st.multiselect(
        "Select Plots to Display",
        plot_options,
        default=["Muscle Distribution"],
    )

    # Dropdown for grouping selection
    categorical_columns = get_categorical_columns(df)
    group_by_column = st.selectbox(
        "Select Column to Group By",
        options=categorical_columns,
    )

    # Display interactive charts
    display_charts(df, selected_plots, group_by_column)

else:
    st.header("Challenge")

    st.write(
        """
        Welcome to the UMUD Community Challenge! This challenge is designed to engage the community in developing models or 
        analysis scripts to predict muscle parameters in an unseen test set. Participants are encouraged to use any tools or 
        techniques at their disposal to create the best predictive models possible. 

        The format of the challenge is inspired by Kaggle competitions, where participants can submit their predictions, 
        and a leaderboard will track the top-performing models.
        """
    )

    # Save instructions to a text file and create a download button

    instructions_path = "/webapp_files/challenge_instructions.txt"
    if os.path.exists(instructions_path):
        with open(instructions_path, "r") as file:
            instructions_content = file.read()
        st.download_button(
            label="📜 Download Challenge Instructions",
            data=instructions_content,
            file_name="challenge_instructions.txt",
            mime="text/plain",
        )

    st.subheader("Submit Your Results via Email")
    recipient_email = "support@umudchallenge.org"
    subject = "UMUD Challenge Submission"
    body = "Please find attached my submission for the UMUD Challenge."

    uploaded_files = st.file_uploader(
        "Choose files to send", type=None, accept_multiple_files=True
    )

    if uploaded_files:
        filenames = [file.name for file in uploaded_files]
        mailto_link = create_email_link(subject, body, recipient_email, filenames)
        st.markdown(f"[Send Email](mailto:{mailto_link})", unsafe_allow_html=True)

    st.header("Scoreboard")

    # Load and display the scoreboard
    scoreboard_df = load_scoreboard()
    display_scoreboard(scoreboard_df)

# TODO check out PyGWalker as well
