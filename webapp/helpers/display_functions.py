import streamlit as st
import ast
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import seaborn as sns
from matplotlib.colors import ListedColormap


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

    df = pd.DataFrame(df)

    for plot in selected_plots:
        if plot == "Muscle Distribution" and "MUSCLE" in df.columns:
            fig, ax = plt.subplots()

            if group_by_column in df.columns:

                df["MUSCLE"] = df["MUSCLE"].apply(
                    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
                )

                # Ensure 'MUSCLE' column entries are lists and then explode them
                df_exploded = df.explode("MUSCLE")

                # Group by muscle name and count occurrences
                muscle_counts = (
                    df_exploded.groupby(group_by_column)["MUSCLE"]
                    .value_counts()
                    .unstack()
                )

                # Plotting the muscle distribution
                fig, ax = plt.subplots()
                muscle_counts.plot(kind="bar", ax=ax, stacked=True)
                ax.set_title("Muscle Distribution")
                ax.set_xlabel(group_by_column)
                ax.set_ylabel("Count")
                st.pyplot(fig)

            else:
                st.warning(
                    f"'{group_by_column}' column is not suitable for 'Muscle Distribution' plot."
                )

        elif plot == "Age Distribution" and "PARTICIPANT_AGE" in df.columns:
            fig, ax = plt.subplots()
            # Check if group_by_column is valid for grouping
            if group_by_column in df.columns:
                df_exploded.groupby(group_by_column)["PARTICIPANT_AGE"].plot(
                    kind="hist", bins=20, alpha=0.5, ax=ax
                )
                ax.set_title("Age Distribution")
                ax.set_xlabel("Age")
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
            else:
                st.warning(
                    f"'{group_by_column}' column is not suitable for 'Age Distribution' plot."
                )

        elif plot == "Data Type Distribution" and "DATA_TYPE" in df.columns:
            fig, ax = plt.subplots()
            if group_by_column in df.columns:
                datatype_count = (
                    df_exploded.groupby(group_by_column)["DATA_TYPE"]
                    .value_counts()
                    .unstack(fill_value=0)
                    .plot(kind="bar", stacked=True, ax=ax)
                )
                ax.set_title("Data Type Distribution")
                ax.set_xlabel("Type")
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
            else:
                st.warning(
                    f"'{group_by_column}' column is not suitable for 'Data Type Distribution' plot."
                )


# Corrently Not Used
def display_scoreboard(df):
    """
    Display the scoreboard using st_aggrid for better visualization.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the scoreboard data.
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


def display_training_metrics():
    """
    Display the algorithm training metrics in a table format with medals for the top three models.
    """
    # Metrics Data
    models = ["DeepACSA_VGG16Unet", "DLTrack_VGG16Unet"]
    task = ["ACSA", "Fascicles"]  # Keep naming constant
    val_iou_scores = [0.89, 0.87]
    val_dice_scores = [0.91, 0.88]
    loss_functions = ["Binary Cross Entropy", "Binary Cross Entropy"]
    training_epochs = [50, 60]
    optimizers = ["Adam", "Adam"]

    # Add medals for top three models
    medals = ["🥇", "🥈"]

    # Create DataFrame
    metrics_df = pd.DataFrame(
        {
            "Rank": medals,
            "Model": models,
            "Segmentation Task": task,
            "Validation IoU": val_iou_scores,
            "Validation Dice": val_dice_scores,
            "Loss Function": loss_functions,
            "Training Epochs": training_epochs,
            "Optimizer": optimizers,
        }
    )

    # Display the table in Streamlit
    st.markdown("### Model Performance Metrics")
    st.dataframe(metrics_df, hide_index=True)


# Currently not used
def display_training_metrics_barplot():
    """
    Display the algorithm training metrics based on entered data.

    Returns
    -------
    plt.fig
        The barchart displaying the performance scores.
    """
    # Metrics Data
    models = ["DeepACSA", "DL_Track_US", "Ultratrack", "SMA"]
    val_iou_scores = [0.89, 0.87, 0.81, 0.77]
    val_dice_scores = [0.91, 0.88, 0.84, 0.80]

    # Create Bar Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(models))
    width = 0.35

    ax.bar(
        x - width / 2, val_iou_scores, width, label="Validation IoU", color="#008080"
    )
    ax.bar(
        x + width / 2, val_dice_scores, width, label="Validation Dice", color="#00a1a1"
    )

    # Chart Formatting
    ax.set_ylabel("Scores")
    ax.set_title("Model Performance Metrics")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()

    return fig


def display_data_warning():
    """
    Function to display warning about algorithm performance.
    """
    st.warning(
        """
        Analysis algorithms and neural networks are only as good as the data they are trained/tested on. **Poor data quality**, lack of diversity, or biases in training 
        datasets can result in models with limited generalizability and **unreliable outcomes**. 
        These factors directly impact algorithm performance, and **results may not always meet expectations on your specific data**.
        """,
        icon=":material/warning:",
    )


def display_comparability_statistics():
    """
    Display comparability statistics for muscle geometry models in an interactive Streamlit UI.

    Parameters:
    - data: dict
        The dataset containing models and metrics.
    """
    data = {
        "Model": ["DeepACSA", "DL_Track_US", "Ultratrack", "SMA"],
        "RF.ACSA_ICC": [0.99, None, None, None],
        "RF.ACSA_MD": [0.99, None, None, None],
        "RF.ACSA_CV%": [0.99, None, None, None],
        "FL_ICC": [None, 0.88, 0.85, 0.80],
        "FL_MD": [None, 1.5, 1.8, 2.0],
        "FL_CV%": [None, 5.0, 5.5, 6.0],
        "PA_ICC": [None, 0.87, 0.84, 0.78],
        "PA_MD": [None, 2.3, 2.5, 2.7],
        "PA_CV%": [None, 5.5, 6.0, 6.5],
        "MT_ICC": [None, 0.89, 0.86, 0.81],
        "MT_MD": [None, 1.2, 1.4, 1.6],
        "MT_CV%": [None, 4.0, 4.2, 4.5],
    }
    df = pd.DataFrame(data)

    st.markdown("#### Select Filters")
    selected_models = st.multiselect(
        "Select Models/Algorithms to Compare",
        options=df["Model"],
        default=df["Model"],
        help="Choose the models you want to compare.",
    )
    selected_metric = st.selectbox(
        "Select Metric",
        ["ICC", "MD", "CV%"],
        help="Choose a performance metric to compare.",
    )
    selected_variable = st.selectbox(
        "Select Variable",
        ["FL", "PA", "MT", "RF.ACSA"],
        help="Choose a variable (Fascicle Length, Pennation Angle, Muscle Thickness).",
    )

    # Filter data based on selected models
    filtered_df = df[df["Model"].isin(selected_models)]

    # Define metric column based on the selected variable and metric
    metric_column = f"{selected_variable}_{selected_metric}"

    # Filter and rename the table
    table_data = (
        filtered_df[["Model", metric_column]]
        .rename(columns={metric_column: selected_metric})
        .sort_values(by=selected_metric, ascending=False)
    )

    # Assign medals to the top three rows
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    table_data.insert(0, "Rank", [medals.get(i, "") for i in range(len(table_data))])

    # Display the table with medals
    st.markdown(f"#### Comparability for **{selected_variable} - {selected_metric}**")
    st.dataframe(table_data, use_container_width=True, hide_index=True)

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
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap=ListedColormap(["#D3D3D3"]),
        ax=ax,
        mask=mask,
        linewidths=0.5,
        linecolor="#008080",
        cbar=False,
    )
    ax.set_title(f"All Metrics for {selected_variable}")
    st.pyplot(fig)
