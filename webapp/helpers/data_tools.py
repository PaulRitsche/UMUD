import streamlit as st 
from io import BytesIO
import base64
import urllib.parse
from st_aggrid import AgGrid, GridOptionsBuilder

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