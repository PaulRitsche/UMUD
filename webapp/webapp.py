import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib.pyplot as plt
from pathlib import Path
from io import BytesIO
import base64
import urllib.parse
import os
import json
from templates.template_dictionary import template_data

# TODO


def clean_dataframe(df):
    """
    Clean the dataframe to ensure all data is properly encoded and formatted.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe with properly encoded and formatted data.
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

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to analyze.

    Returns
    -------
    list
        A list of column names that are categorical or object type.
    """
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


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


# def load_scoreboard():
#     """
#     Load the scoreboard data.

#     Returns
#     -------
#     pandas.DataFrame
#         A dataframe containing the scoreboard data.
#     """

#     # This function should be modified to load data from database if needed.
#     results = pd.DataFrame(
#         {
#             "Name": ["Neil", "Olivier", "Paul"],
#             "SEM Fascicle Length (cm)": [0.1, 0.5, 0.7],
#             "SEM Pennation Angle (cm)": [0.1, 0.5, 0.7],
#             "SEM Muscle Thickness (cm)": [0.1, 0.5, 0.7],
#         }
#     )
#     return results


# def display_scoreboard(df):
#     """
#     Display the scoreboard using st_aggrid for better visualization.

#     Parameters
#     ----------
#     df : pandas.DataFrame
#         The dataframe containing the scoreboard data.
#     """
#     # Add medals to the top three rows
#     medals = ["🥇", "🥈", "🥉"] + [""] * (len(df) - 3)
#     df.insert(0, "Medal", medals)

#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_pagination(paginationAutoPageSize=True)
#     gb.configure_default_column(editable=False, groupable=True)
#     gb.configure_side_bar()
#     grid_options = gb.build()
#     AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)


def filter_dataframe(df):
    """
    Display an interactive, filterable dataframe using st_aggrid and provide a download button.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to be filtered.

    Returns
    -------
    pandas.DataFrame
        The filtered dataframe based on user interactions.
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

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe for chart generation.
    selected_plots : list
        A list of plot types selected by the user.
    group_by_column : str
        The column name to group the data by for visualization.
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

        elif plot == "Data Type Distribution" and "DATA_TYPE" in df.columns:
            fig, ax = plt.subplots()
            datatype_count = (
                df.groupby(group_by_column)["DATA_TYPE"]
                .value_counts()
                .unstack()
                .plot(kind="bar", stacked=True, ax=ax)
            )
            ax.set_title("Data Type Distribution")
            ax.set_xlabel("Type")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)


def get_download_button(df, filename="filtered_data.csv"):
    """
    Generate a link to download the filtered dataframe as a CSV file.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be downloaded.
    filename : str, optional
        The name of the file to be downloaded (default is "filtered_data.csv").

    Returns
    -------
    streamlit.download_button
        A Streamlit download button for the CSV file.
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

    Parameters
    ----------
    subject : str
        The email subject.
    body : str
        The email body.
    recipient : str
        The email recipient.
    filenames : list
        A list of filenames to be attached.

    Returns
    -------
    str
        A mailto link with the specified parameters.
    """
    body += "\n\nAttachments:\n" + "\n".join(filenames)
    params = {"subject": subject, "body": body, "to": recipient}
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    mailto_link = f"mailto:?{query_string}"
    return mailto_link


def get_download_link(content, filename, mime):
    """
    Generate a link to download the given content as a file.

    Parameters
    ----------
    content : str
        The content to be downloaded.
    filename : str
        The name of the file to be downloaded.
    mime : str
        The MIME type of the file.

    Returns
    -------
    str
        An HTML string containing the download link.
    """
    b64 = base64.b64encode(content.encode()).decode()  # Convert to base64
    href = f'<a href="data:{mime};base64,{b64}" download="{filename}">Download detailed instructions...</a>'
    return href


def add_footer():
    """
    Add a footer to the Streamlit app.
    """
    footer = """
    <style>
    .footer {
        background-color: rgba(0, 0, 0, 0);  /* Transparent black background */
        text-align: center;
        padding: 10px;
        font-size: 14px;
        width: 100%;
        position: bottom;
        bottom: 0;
        left: 0;
    }
    .footer a {
        color: #008080;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .footer-divider {
        height: 2px;
        background-color: white;
        width: 100%;
    }
    </style>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var footer = document.querySelector('.footer');
        var observer = new IntersectionObserver(function(entries) {
            if(entries[0].isIntersecting === true)
                footer.style.display = 'block';
            else
                footer.style.display = 'none';
        }, { threshold: [0.9] });
        observer.observe(document.querySelector('#footer-anchor'));
    });
    </script>
    <div id="footer-anchor" style="height: 10px;"></div>
    <div class="footer">
        <p>© 2024 UMUD Repository. All rights reserved.</p>
        <p>Contact: <a href="mailto:umudrepository@gmail.com">umudrepository@gmail.com</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"


# st.session_state.query = {"muscle": "", "image_type": "", "device": "", "age": ""}
# st.session_state.link = {"dataset_link": ""}
# --------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# st.title("Universal Muscle Ultrasound Database" + " " + page_icon)
st.markdown(
    "<h1 style='text-align: center; '>Universal Musculoskeletal Ultrasound Database</h1>",
    unsafe_allow_html=True,
)


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


# Specify tabs
with st.sidebar:
    logo_image_path = str(Path(__file__).with_name("webapp_files"))
    st.image(logo_image_path + "/logo.png", use_column_width=True)

    "---"
    selected_tab = option_menu(
        "",
        options=[
            "Home",
            "Datasets",
            "Database",
            "Challenge",
            "Benchmarks",
            "Contributing",
            "About Us",
        ],
        icons=[
            "house",
            "file-earmark-bar-graph",
            "archive",
            "trophy",
            "stars",
            "person-hearts",
            "info-circle",
        ],
        default_index=0,
        orientation="vertical",
    )

    "---"
    # This adds the footer to the sidebar only.
    add_footer()

if selected_tab == "Home":
    # Welcome Section
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <p><strong>Explore musculoskeletal ultrasonography data for research and development.</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px;">
        <h4 style="text-align: center;">Key Features</h4>
        <ul style="list-style-type: none; padding-left: 0; text-align: left; font-size: 16px;">
            <li>📁 <strong>Variety of Data</strong>: Access images, videos, and 3DUS data.</li>
            <li>🏷️ <strong>Labeled Datasets</strong>: Focused on datasets with comprehensive labels.</li>
            <li>🔍 <strong>Metadata Indexing</strong>: Metadata indexing for efficient searching.</li>
            <li>✨ <strong>Expert Standards</strong>: Expert-analyzed benchmarks and models.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # About UMUD Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        ### About UMUD
        **⚠️ This is a beta version of the UMUD repository, no real datasets are included yet. ⚠️**

        The **UMUD repository** is a centralized platform for musculoskeletal ultrasonography dataset metadata. The database includes B-mode images, videos, 3DUS data, and shear wave elastography data, with a focus on providing labeled datasets for training and research purposes.
        
        Existing  datasets often lack standardized metadata, making it challenging to find the datasets and compare data across different studies. UMUD tries to solve this issue by providing a comprehensive metadata index for musculoskeltal ultrasonography datasets.
        
        Moreover, as part of the [ORMIR](https://www.ormir.org/) community, we aim to set analysis standards by offering benchmark datasets and models, and organizing community challenges.
        """
    )

    news_items_path = str(Path(__file__).with_name("webapp_files"))
    news_items = read_newsfeed(news_items_path + "/newsfeed.txt")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📰 Newsfeed")
    newsfeed_container = """
    <style>
    .news-container {
        max-height: 300px;
        overflow-y: scroll;
        border: 1px solid #e6e6e6;
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 8px;
    }
    .news-item {
        padding: 10px 0;
        border-bottom: 1px solid #ddd;
        font-size: 14px;
    }
    </style>
    <div class="news-container">
    """
    if news_items:
        for item in news_items:
            newsfeed_container += f'<div class="news-item">- {item}</div>'
    else:
        newsfeed_container += '<div class="news-item">No news items available.</div>'

    newsfeed_container += "</div>"
    st.markdown(newsfeed_container, unsafe_allow_html=True)

    # Partner Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Our Collaborators")

    partners = [
        {
            "name": "ORMIR",
            "logo": str(Path(__file__).with_name("webapp_files")) + "/ormir_logo.png",
            "link": "https://ormir.org/",
        },
        {
            "name": "University of Basel",
            "logo": str(Path(__file__).with_name("webapp_files")) + "/unibas_logo.png",
            "link": "https://www.unibas.ch/",
        },
        {
            "name": "University of Padova",
            "logo": str(Path(__file__).with_name("webapp_files")) + "/unipd_logo.png",
            "link": "https://www.unipd.it/",
        },
        {
            "name": "University of Jyväskylä",
            "logo": str(Path(__file__).with_name("webapp_files")) + "/jyu_logo.png",
            "link": "https://www.jyu.fi/",
        },
        {
            "name": "Norwegian School of Sport Sciences",
            "logo": str(Path(__file__).with_name("webapp_files")) + "/nih_logo.png",
            "link": "https://www.nih.no/",
        },
    ]

    # Display partner logos in columns with hover effects
    cols = st.columns(len(partners))
    for col, partner in zip(cols, partners):
        with col:
            st.markdown(
                f"<a href='{partner['link']}' target='_blank'>", unsafe_allow_html=True
            )
            st.image(partner["logo"], use_column_width=True)
            st.markdown("</a>", unsafe_allow_html=True)

    # Closing message
    st.markdown(
        """
    <div style="text-align: center;">
        <h3></h3>
        <h4>Thank you for visiting the UMUD Repository!</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )


elif selected_tab == "Datasets":

    # Horizontal line separator
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
        with st.form("entry_form", clear_on_submit=True):

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
            st.warning("By submitting, you agree to the Data Usage Agreement.")

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

                dataset_links = [result["DATASET_LINK"] for result in results]
                dataset_descriptions = results.distinct("SHORT_DESCRIPTION")

                if dataset_links:
                    st.markdown("##### Dataset Links:")
                    for link in dataset_links:
                        st.markdown(f"- [{link}]({link})")

                    if dataset_descriptions:
                        st.markdown(f"  {', '.join(dataset_descriptions)}")
                    else:
                        st.write(
                            "No dataset descriptions found for the selected criteria."
                        )
                else:
                    st.write("No datasets found for the selected criteria.")


elif selected_tab == "Database":

    # Horizontal line separator
    st.markdown("---")

    # Intro section with concise and readable text
    st.markdown(
        """
        <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px">
            <h4 style="text-align: center;">Database Exploration Tool</h4>
            <p style="text-align: center;">
                In this tab, you can explore the entire musculoskeletal ultrasonography datasets stored in the database. Select the relevant filters, input the values, and retrieve datasets that meet your criteria.
                You can filter the data, visualize different aspects of the dataset through interactive charts, and download the filtered data for further analysis. 
            </p>
        </div>

        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Data Usage Agreement"):
        st.warning("You must agree to the Data Usage Agreement before proceeding.")
        st.markdown(load_dua())  # Display DUA content

        st.text(
            "By proceeding, you agree to the terms and conditions of the Data Usage Agreement."
        )

    agreement = st.checkbox("ACCEPT TO CONTINUE.")

    if agreement:
        items = get_data()
        df = pd.DataFrame(items.find({}))

        if df.empty:
            st.write("No data available in the database.")

        # Clean the dataframe
        df = clean_dataframe(df)

        # Display filtered dataframe with filtering capabilities
        st.markdown("##### Dataset Overview")
        filtered_df = filter_dataframe(df)

        with st.expander("Download Filtered Datasets...", expanded=False):
            st.write(filtered_df)
            # Add download button for the filtered dataframe
            get_download_button(filtered_df)

        "---"

        # Dropdown for plot selection
        st.markdown("##### Interactive Charts")
        plot_options = [
            "Muscle Distribution",
            "Age Distribution",
            "Data Type Distribution",
        ]
        selected_plots = st.multiselect(
            "Select Plots to Display",
            plot_options,
            default=["Muscle Distribution"],
            help="Select which plots you want to display to get a better understanding of the data. So far, only three plots are available. You can select multiple plots.",
        )

        # Dropdown for grouping selection
        categorical_columns = get_categorical_columns(df)
        group_by_column = st.selectbox(
            "Select Column to Group By",
            options=categorical_columns,
            help="Select which column you want to group the data by.",
        )

        # Display interactive charts
        display_charts(df, selected_plots, group_by_column)

elif selected_tab == "Challenge":

    # Horizontal line separator
    st.markdown("---")

    # Intro section with concise and readable text
    st.markdown(
        """
    <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px;">
        <h4 style="text-align: center;">UMUD Community Challenge</h4>
        <p style="text-align: center;">
        <strong>⚠️ The challenge is currently not active ⚠️</strong>
        </p>
        <p style="text-align: center;">
        This challenge will be designed to engage the community in developing models or 
        analysis scripts to predict muscle geometrical parameters in an unseen test set of lower limb ultrasonography images. Participants are encouraged to use any tools or 
        techniques at their disposal to create the best predictions possible.
        </p>
        <p style="text-align: center;">
        The format of the challenge is inspired by <a href="https://www.kaggle.com/competitions" target="_blank">Kaggle</a> competitions, where participants can submit their data analysis predictions, 
        and a leaderboard will track the top results.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # st.subheader("Challenge Outline")

    # st.write("...TBD...")

    # st.subheader("How to participate")
    # st.write(
    #     """
    #     1. **Download the Dataset**: Download the training and test datasets from the [UMUD Repository](#).
    #     2. **Develop Your Analysis Code**: Use the training dataset to develop and train your predictive models/code.
    #     3. **Make Predictions**: Apply your model/analysis script to the test dataset to make predictions on muscle parameters.
    #     4. **Submit Your Predictions and Code**: Submit your predictions using the submission file below and include a link to your trained code or models for evaluation.
    #     5. **Check the Leaderboard**: Track your performance on the leaderboard and see how you rank against other participants.
    #     6. **Win the Challenge!**: If you are among the top 3 participants, there may be (as of yet undetermined) prizes!
    #     """
    # )

    # st.subheader("Challenge Instructions")
    # instructions = str(Path(__file__).with_name("webapp_files"))
    # instructions_path = instructions + "/challenge_instructions.txt"
    # if os.path.exists(instructions_path):
    #     with open(instructions_path, "r") as file:
    #         instructions_content = file.read()
    #     st.download_button(
    #         label="📜 Download Challenge Instructions",
    #         data=instructions_content,
    #         file_name="challenge_instructions.txt",
    #         mime="text/plain",
    #     )

    # st.subheader("Sample Submission File")
    # sample_submission_path = "templates/sample_submission.csv"
    # if os.path.exists(sample_submission_path):
    #     with open(sample_submission_path, "r") as file:
    #         sample_submission_content = file.read()
    #     st.download_button(
    #         label="📄 Download Sample Submission File",
    #         data=sample_submission_content,
    #         file_name="sample_submission.csv",
    #         mime="text/csv",
    #     )

    # st.subheader("Scoreboard")
    # scoreboard_df = (
    #     load_scoreboard()
    # )  # Define this function to load the scoreboard data
    # display_scoreboard(scoreboard_df)  # Define this function to display the scoreboard

    # st.subheader("Submit Your Results")
    # st.write(
    #     """
    #     Please submit your prediction results using the form below. Ensure that your submission file follows the specified format
    #     outlined in the challenge instructions and matches the sample submission file. Since UMUD is devised according to the open science principles,
    #     we encourage you to submit a link to your models and code for evaluation as well. The link will be listed in the scoreboard as well.
    #     """
    # )

    # prediction_file = st.file_uploader(
    #     "Choose a CSV file for predictions", type=["csv"], accept_multiple_files=False
    # )

    # if prediction_file:
    #     filenames = [prediction_file.name]
    #     if code_file:
    #         filenames.append(code_file.name)
    #     st.write(f"Files ready for submission: {', '.join(filenames)}")

    #     # Validate the uploaded prediction file
    #     try:
    #         df = pd.read_csv(prediction_file)
    #         # Check if required columns exist
    #         required_columns = [
    #             "_id",
    #             "_fascicle_length",
    #             "_pennation_angle",
    #             "_muscle_thickness",
    #         ]
    #         if all(column in df.columns for column in required_columns):
    #             st.success(
    #                 "Prediction file format is correct and ready for submission!"
    #             )
    #         else:
    #             st.error(
    #                 f"Prediction file is missing required columns. Expected columns: {required_columns}"
    #             )

    #         st.subheader("Submit via Email")
    #         recipient_email = "umudrepository@gmail.com"
    #         subject = "UMUD Challenge Submission"
    #         body = "Please find attached my submission for the UMUD Challenge."

    #         mailto_link = create_email_link(
    #             subject, body, recipient_email, filenames
    #         )  # Define this function to create mailto link
    #         st.markdown(f"[Send Email](mailto:{mailto_link})", unsafe_allow_html=True)

    #     except Exception as e:
    #         st.error(f"An error occurred while processing the file: {e}")

    # st.write(
    #     """
    #     Alternatively, you can send your submission files directly to [umudrepository@gmail.com](mailto:umudrepository@gmail.com).
    #     """
    # )

elif selected_tab == "Benchmarks":

    "---"

    st.write(
        """
        The benchmark tab is designed to support the development and evaluation of automatic analysis algorithms for muscle architecture and anatomical cross-sectional area (ACSA) analysis in ultrasonography images. Accurate and reliable automatic analysis tools are essential for advancing
         research and clinical practices, particularly for training purposes.

        Muscle architecture analysis includes parameters such as muscle fascicle length, pennation angle, and muscle thickness. These parameters are crucial for understanding muscle function and adaptations to training or rehabilitation.
        As we can all agree, manual ultrasonography image analysis is time-consuming and subjective, especially for large-scale studies. Yet, it is still deemed to gold-standard. So far, no common ground exists where researchers can compare and benchmark their manual analyses/automated algorithms.
        In addition to manual analysis, several automated analysis algorithms exist. Automated analysis algorithms can significantly reduce the time and effort required for manual analysis, enabling faster and more objective results.

        Below is a list of available automatic analysis algorithms along with short descriptions and links to their documentation pages. This list is not exhaustive and may be updated as new algorithms are developed.
        """
    )

    st.subheader("Benchmark Image Dataset")

    st.write(
        """
        To support operator training and the development and validation of automated image analysis algorithms, we provide a downloadable image dataset with corresponding manual analyses by five expert raters. 
        The dataset contains images of cross-sectional area (ACSA) as well as images of muscle architecture. The dataset can be downloaded from the [UMUD Repository](#TODO). 
        There, a detailed descripion of the dataset is provided as well.
 
        You can use this dataset to train and evaluate your own models or compare the performance of different automatic analysis algorithms.  Furthermore, we encourage you to use the dataset to check whether your own manual analysis falls within bounds of the expert-annotations.
        """
    )

    st.subheader("Benchmark Models")

    st.write(
        """
        We have developed benchmark models for muscle architecture and muscle ACSA analysis. The models are those from two published papers. [Ritsche et al. (2022) MSSE](https://journals.lww.com/acsm-msse/fulltext/2022/12000/deepacsa__automatic_segmentation_of.21.aspx) for the ACSA analysis models and [Ritsche et al.(2024) UMD](https://www.sciencedirect.com/science/article/abs/pii/S0301562923003423) for muscle architecture analysis. The specifities of the models can be viewed in the respective papers. 
        The models are implemented in Python and can be easily integrated into your own analysis pipeline. Note that we did not choose our own models for prestige or publicity, but rather because they are the only openly available deep neural networs for this kind of analysis. We will add more benchmarks models for other segmentation tasks in the future.
        
        Performance tables are being developed at the moment...
        """
    )

    st.subheader("Available Automatic Analysis Algorithms")

    st.write(
        """
        We believe that automated image analysis algorithms are essential for advancing our understanding of muscle function and adaptation.
        Therefore we have compiled a list of available automatic analysis algorithms. 
        """
    )

    algorithms = [
        {
            "name": "DeepACSA",
            "description": "DeepACSA utilizes deep learning techniques to automatically analyze muscle ACSA in ultrasound images, providing quick and reliable measurements.",
            "link": "https://deepacsa.readthedocs.io/en/latest/",
        },
        {
            "name": "ACSAuto",
            "description": "ACSAuto is an automatic analysis tool focused on muscle ACSA measurement, offering a user-friendly interface and high precision.",
            "link": "https://github.com/PaulRitsche/ACSAuto",
        },
        {
            "name": "DL_Track_US",
            "description": "DL_Track_US employs deep learning models for tracking muscle fascicles and architecture in ultrasound images, designed for high accuracy and reproducibility.",
            "link": "https://dltrack.readthedocs.io/en/latest/index.html",
        },
        {
            "name": "UltraTrack",
            "description": "UltraTrack is a software tool for tracking muscle fascicles in ultrasound images. It provides robust and accurate tracking of muscle architecture parameters.",
            "link": "https://sites.google.com/site/ultratracksoftware/home",
        },
        {
            "name": "SMA",
            "description": "SMA (Semi-automated Muscle Analysis) offers a semi-automated approach for analyzing muscle architecture, balancing automation with user control for higher accuracy.",
            "link": "https://github.com/oseynnes/SMA",
        },
    ]

    for algo in algorithms:
        st.markdown(f"**[{algo['name']}]({algo['link']})**: {algo['description']}")

    dataset_path = "webapp_files/muscle_benchmark_dataset.zip"
    if os.path.exists(dataset_path):
        with open(dataset_path, "rb") as file:
            dataset_content = file.read()
        st.download_button(
            label="📦 Download Muscle Benchmark Dataset",
            data=dataset_content,
            file_name="muscle_benchmark_dataset.zip",
            mime="application/zip",
        )

elif selected_tab == "Contributing":
    "---"
    st.header("Contributing")

    st.write(
        "We welcome contributions from the community to help improve and expand UMUD. Here's how you can get involved:"
    )

    st.subheader("1. Contributing Data")
    st.write(
        """
    **Want to Contribute Your Muscle Ultrasound Data to UMUD?**

    If you have muscle ultrasound datasets that you would like to share with the scientific community, you can contribute them to the UMUD database. 
    **Important:** Make sure you have permission to share the data openly. UMUD is not responsible for any ethical or legal issues that may arise from sharing your data.

    **Why Contribute?**  
    By sharing your data, you help create a valuable resource for researchers and developers. Your contribution can lead to new discoveries and advancements in muscle research.

    **How to Contribute Your Data - Step by Step:**

    1. **Prepare Your Data:**
        - Make sure your data is properly labeled and formatted according to UMUD standards.  
        - Use the metadata dictionary template provided below to organize your data.  
        - You need a tool that can open Python files, such as [VSCode](https://code.visualstudio.com/), to use the template.  
        - Upload your data to a reliable repository like [Zenodo](https://zenodo.org/) or [OSF](https://osf.io/). Include the link to your dataset in the metadata dictionary.
        - If your dataset includes different populations (e.g., young vs. old individuals), please upload each population as a separate dataset. This makes the data easier to reuse.
        - Organize your images into folders based on the muscle and muscle region they belong to (if possible). You can view our [sample dataset LINK](https://osf.io/xbawc/?view_only=f1b975a4ef554facb48b0a3236adddef) to see how this is done.

    2. **Submit Your Data:**
        - Email your filled-out template dictionary to [umudrepository@gmail.com](mailto:umudrepository@gmail.com).
        - Use the subject line "Dataset Contribution".
        - In the email, include a brief description of your dataset and any relevant publication links.

    3. **Data Review:**
        - Our team will review your submission to ensure it meets UMUD's quality standards.
        - We may contact you if we need more information or clarification.

    4. **Data Integration:**
        - Once your data is approved, it will be added to the UMUD database and made available to the community.
        - You will be credited for your contribution.

    **Thank you for helping us build a valuable resource for the research community!**
    """
    )

    # Add a button to download the template dictionary
    template_dict_content = json.dumps(template_data, indent=4)
    st.download_button(
        label="Download Template Dictionary",
        data=template_dict_content,
        file_name=str(Path(__file__).with_name("templates"))
        + "/template_dictionary.py",
        mime="application/json",
    )

    st.subheader("2. Providing Feedback")
    st.write(
        """
    Your feedback is invaluable in helping us improve UMUD. Whether you have suggestions for new features, improvements to existing functionalities, or general comments, we want to hear from you.
    
    - **Feature Requests**: If you have ideas for new features or enhancements, please email [umudrepository@gmail.com](mailto:umudrepository@gmail.com) with the subject line "Feature Request".
    - **Bug Reports**: If you encounter any issues or bugs, please report them by emailing [umudrepository@gmail.com](mailto:umudrepository@gmail.com) with the subject line "Bug Report". Include detailed information about the issue and steps to reproduce it.
    - **General Feedback**: For any other feedback or comments, you can also use the above email address.
    """
    )

    st.subheader("3. Contributing to the Codebase")
    st.write(
        """
    We encourage developers to contribute to the UMUD codebase. Whether you're fixing bugs, adding new features, or improving documentation, your contributions are welcome.
    
    - **Fork the Repository**: Start by forking the [UMUD Repository](https://github.com/PaulRitsche/UMUD) to your own GitHub account.
    - **Make Your Changes**: Clone your forked repository to your local machine and make the desired changes. Ensure your code follows our contribution guidelines and coding standards. You can take a look at the Readme file for more information on how to do this.
    - **Submit a Pull Request**: Once you've made your changes, push them to your forked repository and submit a pull request to the main repository. Provide a detailed description of your changes and reference any relevant issues or feature requests.
    - **Review and Merge**: Our team will review your pull request and provide feedback. Once approved, your changes will be merged into the main repository.
    """
    )


elif selected_tab == "About Us":

    "---"

    # Intro section with concise and readable text
    st.markdown(
        """
        <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px">
            <h4 style="text-align: center;">The Idea Behind UMUD </h4>
            <p style="text-align: center;">
                UMUD was conceived to provide researchers and developers with a comprehensive and accessible platform for musculoskeletal ultrasound image/video dataset metadata. 
                Existing  datasets often lack standardized metadata, making it challenging to find the datasets and compare data across different studies.
                The aim is to facilitate advancements in muscle research, biomechanics, and physiology by providing high-quality, labeled data for model training and analysis.
           </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("The Main Developers")
    # Neil Cronin
    images = str(Path(__file__).with_name("webapp_files"))
    st.image(
        images + "/neil_cronin.png", caption="Neil Cronin", width=150
    )  # Add the path to Neil Cronin's image
    st.write(
        """
    Neil Cronin is the main visionary behind the UMUD Repository. He had the original idea and has been instrumental in guiding the project. Neil is known for his expertise in biomechanics and musculoskeletal imaging research.
    """
    )
    st.write("[Read more about Neil](http://users.jyu.fi/~necronin/)")

    # Paul Ritsche
    images = str(Path(__file__).with_name("webapp_files"))
    st.image(
        images + "/paul_ritsche.png", caption="Paul Ritsche", width=150
    )  # Add the path to Paul Ritsche's image
    st.write(
        """
    Paul Ritsche is the lead developer who coded and maintains the UMUD Repository. Together with Neil, he finetuned to original idea of UMUD. Paul has a background in biomechanics and musculoskeletal imaging and a passion for software development and data science.
    """
    )
    st.write("[Read more about Paul](https://github.com/PaulRitsche)")

    # Fabio Sarto
    images = str(Path(__file__).with_name("webapp_files"))
    st.image(images + "/fabio_sarto.png", caption="Fabio Sarto", width=150)
    st.write(
        """
    Fabio Sarto is a developer of the UMUD Repository. He has been instrumental in developing and testing the UMUD Repository's data collection and labeling process. Fabio has a background in neuromuscular physiology and musculoskeletal imaging, and a passion for open-science
    """
    )
    st.write(
        "[Read more about Fabio](https://www.researchgate.net/profile/Fabio-Sarto-2)"
    )

    # Olivier Seynnes
    images = str(Path(__file__).with_name("webapp_files"))
    st.image(
        images + "/olivier_seynnes.png", caption="Olivier Seynnes", width=150
    )  # Add the path to Olivier Seynnes's image
    st.write(
        """
    Olivier Seynnes has been involved with the UMUD Repository from the beginning, providing valuable insights and support. Olivier is an expert in muscle physiology and musculoskeletal imaging has contributed significantly to the project's development.
    """
    )
    st.write(
        "[Read more about Olivier](https://www.nih.no/english/about/employees/oliviers/)"
    )

    # Contributers

    st.subheader("The Contributors")

    st.write(
        """
    [Francesco Santini](https://www.francescosantini.com/wp/)

    [Oliver Faude](https://www.researchgate.net/profile/Oliver-Faude)

    [Martino Franchi](https://www.researchgate.net/profile/Martino-Franchi)

    ...
    """
    )
