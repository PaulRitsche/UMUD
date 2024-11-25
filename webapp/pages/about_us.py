import streamlit as st
from pathlib import Path
from helpers.sidebar import setup_sidebar


def about_us():



    st.markdown(
        "<h1 style='text-align: center; '>Universal Musculoskeletal Ultrasound Database</h1>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

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

    st.markdown("---")

    st.subheader("The Main Developers")
    # Neil Cronin
    images = str(Path(__file__).resolve().parent.parent / "webapp_files")
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
