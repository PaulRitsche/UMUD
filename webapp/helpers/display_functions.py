import streamlit as st
import ast
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder


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

    ax.bar(x - width / 2, val_iou_scores, width, label="Validation IoU", color="#008080")
    ax.bar(x + width / 2, val_dice_scores, width, label="Validation Dice", color="#00a1a1")

    # Chart Formatting
    ax.set_ylabel("Scores")
    ax.set_title("Model Performance Metrics")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()

    return fig