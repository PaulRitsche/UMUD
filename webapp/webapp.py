import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pathlib import Path
import os
import json
from templates.template_dictionary import template_data
import streamlit_pydantic as sp
from helpers.loading_functions import load_dua, read_newsfeed, get_data
from helpers.display_functions import display_charts, display_training_metrics
from helpers.data_tools import *
from helpers.pydantic_models import DatasetMetadata 
from helpers.footer import add_footer
import numpy as np
import seaborn as sns

# TODO upload other dicts
# TODO include benchmark zip and complete benchmark Tab
# TODO discuss how we actually approach this? Should we refer to the training images of DLTrack/DeepACSA and the report the training data?
# I mean, we do not even know that ML models are superior, but other algorithms cannot report this?
# TODO update links of benchmark models. 
# TODO complete the algorithm list

# ----- Settings -----
page_title = "UMUD"
page_icon = ":mechanical_arm:"
layout = "centered"
# --------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.markdown(
    "<h1 style='text-align: center; '>Universal Musculoskeletal Ultrasound Database</h1>",
    unsafe_allow_html=True,
)

# Specify tabs
with st.sidebar:
    logo_image_path = str(Path(__file__).with_name("webapp_files"))
    st.image(logo_image_path + "/logo.png", use_container_width=True)

    "---"
    selected_tab = option_menu(
        "",
        options=[
            "Home",
            "Datasets",
            "Database",
            "Challenge",
            "Benchmarks",
            "Image Analysis",
            "Contributing",
            "About Us",
        ],
        icons=[
            "house",
            "file-earmark-bar-graph",
            "archive",
            "trophy",
            "stars",
            "magic",
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
        **⚠️ This is a beta version of the UMUD repository, no functionality is guaranteed yet. We are currently testing first dataset inclusions. ⚠️**

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
            st.image(partner["logo"], use_container_width=True)
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
            <h4 style="text-align: center;">📈 Explore Muscle Ultrasound Datasets</h4>
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


elif selected_tab == "Database":

    # Horizontal line separator
    st.markdown("---")

    # Intro section with concise and readable text
    st.markdown(
        """
        <div style="padding: 10px; border: 2px solid #008080; border-radius: 10px; border-width: 3px">
            <h4 style="text-align: center;">💾 Database Exploration Tool</h4>
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
        df_clean = clean_dataframe(df)

        # Display filtered dataframe with filtering capabilities
        st.markdown("##### Dataset Overview")
        filtered_df = filter_dataframe(df_clean)

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
        <h4 style="text-align: center;">🏆 UMUD Community Challenge</h4>
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

    st.markdown("---")

    # Benchmark Tab Header
    st.markdown(
    """
    <div style="padding: 15px; border: 2px solid #008080; border-radius: 10px; background-color: #f9f9f9;">
        <h3 style="text-align: center; color: #008080;">✨ Benchmarking Muscle Ultrasound Analysis</h3>
        <p style="text-align: center;">
            The Benchmark tab helps evaluate <b>muscle geometry analysis algorithms</b> in ultrasonography. Key parameters include 
            <b>anatomical cross-sectional area, fascicle length, pennation angle, and muscle thickness</b>, essential for understanding muscle function 
            and adaptation. Manual analysis, though a gold standard, is labor-intensive and subjective.  
        </p>
        <p style="text-align: center;">
            This platform provides a <b>common ground for comparing and benchmarking</b> manual and automated methods, advancing research with standardized evaluations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
    )


    st.markdown("---")

    # Benchmark Image Dataset Section
    st.markdown(
        """
        ### 📂 Benchmark Image Dataset
        To support operator training and the development of automated image analysis algorithms, we provide a downloadable dataset 
        with manual analyses by **five expert raters**. The dataset includes:
        - **Cross-sectional area (ACSA) images**
        - **Muscle architecture images**

        This dataset allows you to:
        - Evaluate your models/algorithm agains a common geound truth.
        - Compare your manual analysis with expert annotations.
        - Learn how to analyse muscle geometry in ultrasonography images.

        📥 **[Download the Dataset from the UMUD Repository](#TODO)**  

        The dataset contains original muscle geometry ultrasound images, the analysed images and the corresponding manual analysis results:
        - **35 architectural images** from the vastus lateralis, gastrocnemius medialis and tibialis anterior acquired with different devices are included.
        - **30 panoramic images of rectus femoris anatomical cross-sectional area** acquired with different devices and at different muscle regions are included as well.

        🔍 We are **continuously inlcuding more images and muscles** in our benchmark datasets.
        """
    )

    # Benchmark Models Section
    st.markdown("---")
    
    st.markdown(
        """
        ### 🧠 Benchmark Models
        We offer benchmark models for muscle architecture and ACSA analysis, implemented in Python and integrated with 
        openly available datasets. These models are derived from published research:
        - **ACSA Analysis Models**: [Ritsche et al. (2022) MSSE](https://journals.lww.com/acsm-msse/fulltext/2022/12000/deepacsa__automatic_segmentation_of.21.aspx)
        - **Muscle Architecture Models**: [Ritsche et al. (2024) UMD](https://www.sciencedirect.com/science/article/abs/pii/S0301562923003423)

        These models are selected to serve as reliable benchmarks, not for publicity but to encourage collaboration and improvement. 
        Additional benchmark models for other segmentation tasks are under development.
        """
    )

    # Performance Metrics Section
    st.markdown("---")
    
    st.markdown(
        """
        ### 📊 Performance Metrics
        Benchmarking and scoring performance is essential for transparency and reproducibility. The performance metrics are dependent on the dataset
        which is why we chose them represent the current best practices. Here is a short description of the metrics:
        - **IoU (Intersection over Union)**: Measures overlap between predicted and ground truth areas.
        - **Dice Coefficient**: Measures similarity between two sets of data.
        By expanding the fields below, you can take a detailed look at the model/algorithm performance on our test images.
        """
    )

    with st.expander("🤗 Algorithm Training Metrics"):

        st.markdown("#### Algorithm Training Metrics")
        # Description of Calculation
        st.markdown("""
                    All metrics are calculated during model training...
                    """)

        fig = display_training_metrics()
        st.pyplot(fig)

    # Example data for models, metrics, and variables
    data = {
        "Model": ["DeepACSA", "DL_Track_US", "Ultratrack", "SMA"],
        "RF.ACSA_ICC": [0.99, None, None, None],
        "RF.ACSA_MD": [0.99, None, None, None],
        "RF.ACSA_CV%": [0.99, None, None, None],
        "RF.ACSA_SEM": [None, None, None, None],
        "FL_ICC": [None, 0.88, 0.85, 0.80],
        "FL_MD": [None, 1.5, 1.8, 2.0],
        "FL_CV%": [None, 5.0, 5.5, 6.0],
        "FL_SEM": [None, 0.9, 1.0, 1.1],
        "PA_ICC": [None, 0.87, 0.84, 0.78],
        "PA_MD": [None, 2.3, 2.5, 2.7],
        "PA_CV%": [None, 5.5, 6.0, 6.5],
        "PA_SEM": [None, 1.0, 1.1, 1.2],
        "MT_ICC": [None, 0.89, 0.86, 0.81],
        "MT_MD": [None, 1.2, 1.4, 1.6],
        "MT_CV%": [None, 4.0, 4.2, 4.5],
        "MT_SEM": [None, 0.8, 0.9, 1.0],
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Dropdowns for model selection and metric filtering
    # TODO Should we do this muscle specific? Because at least for ACSA it is relevant...
    with st.expander("📐 Muscle Geometry Comparability Metrics", expanded=False):
        st.markdown("#### Select Filters")
        selected_models = st.multiselect(
            "Select Models/Algorithms to Compare", 
            options=df["Model"], 
            default=df["Model"],
            help="Choose the models you want to compare."
        )
        selected_metric = st.selectbox(
            "Select Metric", 
            ["ICC", "MD", "CV%", "SEM"], 
            help="Choose a performance metric to compare."
        )
        selected_variable = st.selectbox(
            "Select Variable", 
            ["FL", "PA", "MT", "RF.ACSA"], 
            help="Choose a variable (Fascicle Length, Pennation Angle, Muscle Thickness)."
        )

        # Filter data based on selected models
        filtered_df = df[df["Model"].isin(selected_models)]

        # Dynamic Table for Selected Metric and Variable
        st.markdown(f"#### Comparability for **{selected_variable} - {selected_metric}**")
        metric_column = f"{selected_variable}_{selected_metric}"
        table_data = filtered_df[["Model", metric_column]].rename(
            columns={metric_column: selected_metric}
        )
        st.table(table_data)

        # Heatmap for All Metrics of a Selected Variable
        st.markdown(f"#### Comparability Map for **{selected_variable}**")
        heatmap_data = filtered_df[
            [col for col in df.columns if selected_variable in col]
        ].set_index(filtered_df["Model"])
        heatmap_data.columns = [col.split("_")[1] for col in heatmap_data.columns]

        # Ensure numeric data
        heatmap_data = heatmap_data.apply(pd.to_numeric, errors="coerce")

        # Create a mask for NaN values
        mask = heatmap_data.isnull()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=ListedColormap(['#D3D3D3']), ax=ax, mask=mask, linewidths=0.5, linecolor="#008080", cbar=False,)
        ax.set_title(f"All Metrics for {selected_variable}")
        st.pyplot(fig)

elif selected_tab == "Image Analysis":
    st.markdown("---")
    st.markdown(
        """
        <div style="padding: 15px; border: 2px solid #008080; border-radius: 10px; background-color: #f9f9f9;">
            <h3 style="color: #000000; text-align: center;">🧙‍♂️ Automatic Analysis Algorithms</h3>
            <p style="text-align: center;">
                Automated image analysis algorithms are pivotal for driving progress in the understanding of muscle function, 
                adaptation, and structural assessments. At UMUD, we aim to empower researchers with state-of-the-art tools 
                that enhance analysis efficiency and accuracy. Below, you’ll find a curated list of available automatic 
                analysis algorithms that have been widely used and validated in the field.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
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
            "description": "SMA (Simple Muscle Analysis) offers a semi-automated approach for analyzing muscle architecture, balancing automation with user control for higher accuracy.",
            "link": "https://github.com/oseynnes/SMA",
        },
    ]

    for algo in algorithms:
        st.markdown(f"**[{algo['name']}]({algo['link']})**: {algo['description']}")

    dataset_path = str(Path(__file__).with_name("webapp_files"))
    if os.path.exists(dataset_path):
        with open(dataset_path + "/muscle_benchmark_dataset.zip", "rb") as file:
            dataset_content = file.read()
        st.download_button(
            label="📦 Download Muscle Benchmark Dataset",
            data=dataset_content,
            file_name="muscle_benchmark_dataset.zip",
            mime="application/zip",
        )


elif selected_tab == "Contributing":

    st.markdown("---")

    st.markdown(
        """
        <div style="padding: 20px; border: 2px solid #008080; border-radius: 10px;">
            <h3 style="text-align: center; color: #000000;">💕 Contribute Your Data to UMUD</h3>
            <p>
                By sharing your datasets, you help create a valuable resource for researchers worldwide. <b>Follow four steps to contribute: Data Preparation,
                Metadata Submission, Metadata Review, Metadata Integration.</b> These steps are explained in detail below.
                Moreover, you can also give feedback and contribute to the codebase. Thank you for helping us build a resource for the research community!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("Contributing Data")
    st.write(
        """
    If you have muscle ultrasound datasets that you would like to share with the scientific community, you can contribute them to the UMUD database. 
    **Important:** Make sure you have permission to share the data openly. UMUD is not responsible for any ethical or legal issues that may arise from sharing your data.

    **Why Contribute?**  
    By sharing your data, you help create a valuable resource for researchers and developers. Your contribution can lead to new discoveries and advancements in muscle research.

    **How to Contribute Your Data - Step by Step:**

    1. **Prepare Your Data:**
        - Make sure your data is properly labeled and formatted according to UMUD standards.  
        - Use the metadata entryfields below to create a metadata .json file for your data.   
        - Upload your data to a reliable repository like [Zenodo](https://zenodo.org/) or [OSF](https://osf.io/). Include the link to your dataset in the metadata dictionary.
        - If your dataset includes different populations (e.g., young vs. old individuals), please upload each population as a separate dataset. This makes the data easier to reuse.
        - Organize your images according to our [sample dataset](https://osf.io/xbawc/?view_only=f1b975a4ef554facb48b0a3236adddef).
    """)
    # Pydantic form in a styled popover
    with st.expander("📝 Fill Out Dataset Metadata", expanded=False):
        st.markdown(
            """
            <p style="color: #008080;">
                Use this form to enter your dataset metadata. Once completed, you can generate and download a JSON file
                for submission. Not all fields are required, take a look at the description.
            </p>
            """,
            unsafe_allow_html=True,
        )
        
        validated_data = sp.pydantic_form(key="DatasetMetadataForm", model=DatasetMetadata)

        if validated_data:
            st.success("Form validated successfully!")
            
            # Convert set fields to list before serialization
            validated_dict = dict(validated_data)
            for key, value in validated_dict.items():
                if isinstance(value, set):
                    validated_dict[key] = list(value)

            json_data = json.dumps(validated_dict, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="dataset_metadata.json",
                mime="application/json",
            )
        else:
            st.warning("Please complete all required fields.")

    st.write("""
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

    st.subheader("Providing Feedback")
    st.write(
        """
    Your feedback is invaluable in helping us improve UMUD. Whether you have suggestions for new features, improvements to existing functionalities, or general comments, we want to hear from you.

    - **Feature Requests**: If you have ideas for new features or enhancements, please email [umudrepository@gmail.com](mailto:umudrepository@gmail.com) with the subject line "Feature Request".
    - **Bug Reports**: If you encounter any issues or bugs, please report them by emailing [umudrepository@gmail.com](mailto:umudrepository@gmail.com) with the subject line "Bug Report". Include detailed information about the issue and steps to reproduce it.
    - **General Feedback**: For any other feedback or comments, you can also use the above email address.
    """
    )

    st.subheader("Contributing to the Codebase")
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
            <h4 style="text-align: center;">💡 The Idea Behind UMUD </h4>
            <p style="text-align: center;">
                UMUD was conceived to provide researchers and developers with a comprehensive and accessible platform for musculoskeletal ultrasound image/video dataset metadata. 
                Existing  datasets often lack standardized metadata, making it challenging to find the datasets and compare data across different studies.
                The aim is to facilitate advancements in muscle research, biomechanics, and physiology by providing high-quality, labeled data for model training and analysis.
           </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

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
