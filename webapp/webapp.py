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


def read_newsfeed(filepath):
    """
    Reads news items from a text file and returns them as a list of strings.

    Args:
        filepath (str): The path to the newsfeed text file.

    Returns:
        list: A list of news items.
    """
    try:
        with open(filepath, "r") as file:
            news_items = file.readlines()
        return [item.strip() for item in news_items]
    except Exception as e:
        st.error(f"Error reading newsfeed: {e}")
        return []


def load_scoreboard():
    # This function should be modified to load data from your database if needed.
    results = pd.DataFrame(
        {
            "Name": ["Neil", "Olivier", "Paul"],
            "SEM Fascicle Length (cm)": [0.1, 0.5, 0.7],
            "SEM Pennation Angle (cm)": [0.1, 0.5, 0.7],
            "SEM Muscle Thickness (cm)": [0.1, 0.5, 0.7],
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


def add_footer():
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
        <p>Contact: <a href="mailto:support@umudrepository.org">support@umudrepository.org</a></p>
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
    "<h1 style='text-align: center; '>Universal Muscle Ultrasound Database</h1>",
    unsafe_allow_html=True,
)


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
with st.sidebar:
    logo_image_path = str(Path(__file__).with_name("webapp_files"))
    st.image(logo_image_path + "/logo.png", use_column_width=True)
    # st.markdown(
    #     """
    # <div style="text-align: center;">
    #     <h2>Navigation</h2>
    # </div>
    # """,
    #     unsafe_allow_html=True,
    # )
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
            "License",
        ],
        icons=[
            "house",
            "file-earmark-bar-graph",
            "archive",
            "trophy",
            "stars",
            "person-hearts",
            "info-circle",
            "key",
        ],
        default_index=0,
        orientation="vertical",
    )

    "---"

    add_footer()

if selected_tab == "Home":

    "---"

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
    The **UMUD repository** is a comprehensive database hosted on MongoDB Atlas. It contains metadata for a wide range of datasets, including images, videos, and 3D ultrasound (3DUS) data. Our mission is to provide an accessible platform for researchers and developers to access and utilize this data for various purposes, including model training and medical research. Moreover, we aim to create analysis standards by providing benchmark datasets analysed by experts in the field and benchmark models for automated image analysis. 
    
    We are continuously working on expanding the repository and making it publicly accessible. Be sure to check out the Newsfeed below!
    """
    )

    st.markdown(
        """

    ### Features
    - 📁 **Variety of Data**: Includes images, videos, and 3DUS data.
    - 🏷️ **Labeled Datasets**: Focus on datasets that include labels for better training and validation.
    - 🔍 **Metadata Indexing**: Comprehensive indexing of metadata for easy search and retrieval.
    - ✨ **Analysis Standards**: Provide benchmark datasets and models analysed by experts in the field.
    """
    )

    news_items = read_newsfeed("webapp_files/newsfeed.txt")
    st.markdown("### 📰 Newsfeed")
    newsfeed_container = """
    <style>
    .news-container {
        max-height: 300px;
        overflow-y: scroll;
        border: 1px solid #e6e6e6;
        padding: 10px;
        background-color: #f9f9f9;
    }
    .news-item {
        padding: 5px 0;
        border-bottom: 1px solid #ddd;
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

    # License section with GPL-3.0 license

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

    "---"
    st.header("Enter Metadata to Query Datasets")

    st.write(
        "In this tab, you can query the muscle ultrasound datasets by providing specific metadata filters. "
        "Select the filters you want to apply, provide the values, and submit the query to retrieve relevant datasets."
    )

    # Allow users to select which filters they want to use
    st.markdown("#### Select Filters to Apply")
    filter_options = list(template_data[0].keys())
    selected_filters = st.multiselect(
        "",
        filter_options,
        help="Select which filters you want to apply to get the dataset you want. Filters are based on the metadata fields and contain all values present in the datasets of the database.",
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


elif selected_tab == "Database":

    "---"

    st.header("Database")

    st.write(
        "In this tab, you can explore the entire muscle ultrasound dataset stored in the database. "
        "You can filter the data, visualize different aspects of the dataset through interactive charts, "
        "and download the filtered data for further analysis."
    )

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

    "---"

    # Dropdown for plot selection
    st.subheader("Interactive Charts")
    plot_options = ["Muscle Distribution", "Age Distribution"]
    selected_plots = st.multiselect(
        "Select Plots to Display",
        plot_options,
        default=["Muscle Distribution"],
        help="Select which plots you want to display to get a better understanding of the data. So far, only two plots are available.",
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

    "---"

    st.header("UMUD Community Challenge")

    st.write(
        """
        Welcome to the UMUD Community Challenge! This challenge is designed to engage the community in developing models or 
        analysis scripts to predict muscle parameters in an unseen test set. Participants are encouraged to use any tools or 
        techniques at their disposal to create the best predictive models possible.

        The format of the challenge is inspired by Kaggle competitions, where participants can submit their predictions, 
        and a leaderboard will track the top-performing models.
        """
    )

    st.subheader("How to Participate")
    st.write(
        """
        1. **Download the Dataset**: Download the training and test datasets from the [UMUD Repository](#).
        2. **Develop Your Analysis Code**: Use the training dataset to develop and train your predictive models/code.
        3. **Make Predictions**: Apply your model to the test dataset to make predictions on muscle parameters.
        4. **Submit Your Predictions and Code**: Submit your predictions using the submission file below and include a linke to your trained code or models for evaluation.
        5. **Check the Leaderboard**: Track your performance on the leaderboard and see how you rank against other participants.
        6. **Win the Challenge!**: If you are among the top 3 participants, there may be (as of yet undetermined) prizes!
        """
    )

    st.subheader("Challenge Instructions")
    instructions_path = "webapp_files/challenge_instructions.txt"
    if os.path.exists(instructions_path):
        with open(instructions_path, "r") as file:
            instructions_content = file.read()
        st.download_button(
            label="📜 Download Challenge Instructions",
            data=instructions_content,
            file_name="challenge_instructions.txt",
            mime="text/plain",
        )

    st.subheader("Sample Submission File")
    sample_submission_path = "webapp_files/sample_submission.csv"
    if os.path.exists(sample_submission_path):
        with open(sample_submission_path, "r") as file:
            sample_submission_content = file.read()
        st.download_button(
            label="📄 Download Sample Submission File",
            data=sample_submission_content,
            file_name="sample_submission.csv",
            mime="text/csv",
        )

    st.subheader("Scoreboard")
    scoreboard_df = (
        load_scoreboard()
    )  # Define this function to load the scoreboard data
    display_scoreboard(scoreboard_df)  # Define this function to display the scoreboard

    st.subheader("Submit Your Results")
    st.write(
        """
        Please submit your prediction results using the form below. Ensure that your submission file follows the specified format 
        outlined in the challenge instructions and matches the sample submission file. Since UMUD is devised according to the open science principles,
        we encourage you to submit a link to your models and code for evaluation as well. The link will be listed in the scoreboard as well. 
        """
    )

    prediction_file = st.file_uploader(
        "Choose a CSV file for predictions", type=["csv"], accept_multiple_files=False
    )

    if prediction_file:
        filenames = [prediction_file.name]
        if code_file:
            filenames.append(code_file.name)
        st.write(f"Files ready for submission: {', '.join(filenames)}")

        # Validate the uploaded prediction file
        try:
            df = pd.read_csv(prediction_file)
            # Example validation: Check if required columns exist
            required_columns = [
                "_id",
                "_fascicle_lengt",
                "_pennation_angle",
                "_muscle_thickness",
            ]
            if all(column in df.columns for column in required_columns):
                st.success(
                    "Prediction file format is correct and ready for submission!"
                )
            else:
                st.error(
                    f"Prediction file is missing required columns. Expected columns: {required_columns}"
                )

            st.subheader("Submit via Email")
            recipient_email = "support@umudchallenge.org"
            subject = "UMUD Challenge Submission"
            body = "Please find attached my submission for the UMUD Challenge."

            mailto_link = create_email_link(
                subject, body, recipient_email, filenames
            )  # Define this function to create mailto link
            st.markdown(f"[Send Email](mailto:{mailto_link})", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

    st.write(
        """
        Alternatively, you can send your submission files directly to [support@umudchallenge.org](mailto:support@umudchallenge.org).
        """
    )

elif selected_tab == "Benchmarks":

    "---"
    st.header("Benchmarks for Muscle Architecture and ACSA Analysis")

    st.write(
        """
        This benchmark is designed to support the development and evaluation of automatic analysis algorithms for muscle architecture and anatomical cross-sectional area (ACSA) analysis in ultrasonography images. Accurate and reliable automatic analysis tools are essential for advancing research and clinical practices, particularly for training purposes.

        Muscle architecture analysis includes parameters such as muscle fascicle length, pennation angle, and muscle thickness. These parameters are crucial for understanding muscle function and adaptations to training or rehabilitation.
        As we can all agree, manual ultrasonography image analysis is time-consuming and subjective, especially for large-scale studies. So far, no common ground exists where researchers can compare and benchmark their manual analyses/algorithms.
        In addition to manual analysis, several automated analysis algorithms exist. Automated analysis algorithms can significantly reduce the time and effort required for manual analysis, enabling faster and more accurate results.

        Below is a list of available automatic analysis algorithms along with short descriptions and links to their documentation pages. This list is not exhaustive and may be updated as new algorithms are developed.
        """
    )

    st.subheader("Benchmark Image Dataset")

    st.write(
        """
        To support operator training and the development and validation of automated image analysis algorithms, we provide a downloadable image dataset with corresponding manual analyses by five expert raters. 
        The dataset contains images of cross-sectional area (ACSA) as well as images of muscle architecture. The dataset can be downloaded from the following link: [Dataset](https://drive.google.com/drive/folders/13Lq803fK96w4U45K062RH29875565663?usp=sharing).
 
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
            "link": "file:///C:/Users/admin/Documents/DeepACSA/DeepACSA/docs/build/html/index.html",
        },
        {
            "name": "ACSAuto",
            "description": "ACSAuto is an automatic analysis tool focused on muscle ACSA measurement, offering a user-friendly interface and high precision.",
            "link": "https://github.com/PaulRitsche/ACSAuto",
        },
        {
            "name": "DL_Track_US",
            "description": "DL_Track_US employs deep learning models for tracking muscle fascicles and architecture in ultrasound images, designed for high accuracy and reproducibility.",
            "link": "file:///C:/Users/admin/Documents/DL_Track/DL_Track_US/docs/build/html/index.html",
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
        "We welcome contributions from the community to help improve and expand the UMUD Repository. Here's how you can get involved:"
    )

    st.subheader("1. Contributing Data")
    st.write(
        """
    If you have muscle ultrasound datasets that you would like to share, you can contribute them to the UMUD Repository. 
    **Please make sure, that you have permission to share the data openly. UMUD does not cover any potential ethical or legal issues associated with sharing data.**
    By contributing your data, you help create a richer resource for researchers and developers. Here's how you can add your data:
    
    - **Prepare Your Data**: Ensure your data is properly labeled and formatted according to the UMUD standards. This includes metadata such as muscle type, imaging device, participant details, and file formats.
    - **Submit Your Data**: Email your dataset to [contribute@umudrepository.org](mailto:contribute@umudrepository.org) with the subject line "Dataset Contribution". Include a brief description of the dataset and any relevant publication links.
    - **Data Review**: Our team will review your submission to ensure it meets our quality standards. We may contact you for additional information or clarification if needed.
    - **Data Integration**: Once approved, your dataset will be integrated into the UMUD Repository and made available to the community. You will be credited for your contribution.
    """
    )

    # Add a button to download the template dictionary
    template_dict_content = json.dumps(template_data, indent=4)
    st.download_button(
        label="Download Template Dictionary",
        data=template_dict_content,
        file_name="templates/template_dictionary.py",
        mime="application/json",
    )

    st.subheader("2. Providing Feedback")
    st.write(
        """
    Your feedback is invaluable in helping us improve the UMUD Repository. Whether you have suggestions for new features, improvements to existing functionalities, or general comments, we want to hear from you.
    
    - **Feature Requests**: If you have ideas for new features or enhancements, please email [feedback@umudrepository.org](mailto:feedback@umudrepository.org) with the subject line "Feature Request".
    - **Bug Reports**: If you encounter any issues or bugs, please report them by emailing [support@umudrepository.org](mailto:support@umudrepository.org) with the subject line "Bug Report". Include detailed information about the issue and steps to reproduce it.
    - **General Feedback**: For any other feedback or comments, you can also use the above email addresses.
    """
    )

    st.subheader("3. Contributing to the Codebase")
    st.write(
        """
    We encourage developers to contribute to the UMUD Repository's codebase. Whether you're fixing bugs, adding new features, or improving documentation, your contributions are welcome.
    
    - **Fork the Repository**: Start by forking the [UMUD Repository GitHub repository](https://github.com/UMUD-repo) to your own GitHub account.
    - **Make Your Changes**: Clone your forked repository to your local machine and make the desired changes. Ensure your code follows our contribution guidelines and coding standards.
    - **Submit a Pull Request**: Once you've made your changes, push them to your forked repository and submit a pull request to the main repository. Provide a detailed description of your changes and reference any relevant issues or feature requests.
    - **Review and Merge**: Our team will review your pull request and provide feedback. Once approved, your changes will be merged into the main repository.
    """
    )


elif selected_tab == "About Us":

    "---"
    st.header("About Us")

    st.subheader("The Idea Behind UMUD")
    st.write(
        """
    The UMUD (Ultrasound Muscle Data) Repository was conceived to provide researchers and developers with a comprehensive and accessible platform for muscle ultrasound datasets. 
    The aim is to facilitate advancements in muscle research, biomechanics, and medical applications by providing high-quality, labeled data for model training and analysis.
    """
    )

    st.subheader("The Main Developers")
    # Neil Cronin
    st.image(
        "webapp_files/neil_cronin.png", caption="Neil Cronin", width=150
    )  # Add the path to Neil Cronin's image
    st.write(
        """
    Neil Cronin is the main visionary behind the UMUD Repository. He had the original idea and has been instrumental in guiding the project. Neil is known for his expertise in biomechanics and muscle research.
    """
    )
    st.write(
        "[Read more about Neil Cronin](https://scholar.google.com/citations?user=neil_cronin)"
    )

    # Paul Ritsche
    st.image(
        "webapp_files/paul_ritsche.png", caption="Paul Ritsche", width=150
    )  # Add the path to Paul Ritsche's image
    st.write(
        """
    Paul Ritsche is the lead developer who coded and maintains the UMUD Repository. Together with Neil, he finetuned to original idea of UMUD. Paul has a background in biomechanics and muscle physiolohy and a passion for software development and data science.
    """
    )
    st.write(
        "[Read more about Paul Ritsche](https://www.linkedin.com/in/paul-ritsche/)"
    )

    # Fabio Sarto
    st.image("webapp_files/fabio_sarto.png", caption="Fabio Sarto", width=150)
    st.write(
        """
    Fabio Sarto is a developer of the UMUD Repository. He has been instrumental in developing and testing the UMUD Repository's data collection and labeling process. Fabio has a background in biomechanics and muscle physiology and a passion for open-science
    """
    )

    # Olivier Seynnes
    st.image(
        "webapp_files/olivier_seynnes.png", caption="Olivier Seynnes", width=150
    )  # Add the path to Olivier Seynnes's image
    st.write(
        """
    Olivier Seynnes has been involved with the UMUD Repository from the beginning, providing valuable insights and support. Olivier is an expert in muscle physiology and has contributed significantly to the project's development.
    """
    )
    st.write(
        "[Read more about Olivier Seynnes](https://scholar.google.com/citations?user=olivier_seynnes)"
    )

    # Contributers

    st.subheader("The Contributors")

    st.write(
        """
    Francesco Santini

    Oliver Faude

    Martino Franchi
    
    ...
    """
    )

elif selected_tab == "License":

    "---"

    st.markdown(
        """
    ### License
    The UMUD repository is licensed under the **[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)**. You are free to:
    - **Share**: Copy and redistribute the material in any medium or format.
    - **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially.

    Under the following terms:
    - **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
    - **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

    Each dataset is licensed on its own. Please refer to the each dataset page for more information. 
    """
    )
# TODO check out PyGWalker as well
