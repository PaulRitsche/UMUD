import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu

def setup_sidebar():
    """Sets up the sidebar with logo, navigation, and footer."""
    # Sidebar with custom CSS styling
    st.markdown(
        """
        <style>
            .css-1aumxhk {
                background-color: #008080 !important;
                padding: 20px !important;
                border-radius: 8px !important;
            }
            .css-1aumxhk img {
                margin-bottom: 20px;
            }
            .css-qri22k {
                color: white !important;
                font-weight: bold;
            }
            .css-qri22k:hover {
                background-color: #005959 !important;
                color: #ffffff !important;
                border-radius: 8px !important;
            }
            .footer {
                text-align: center;
                font-size: 12px;
                color: white;
                margin-top: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar content
    with st.sidebar:
        logo_image_path = str(Path(__file__).resolve().parent.parent / "webapp_files")
        st.image(logo_image_path + "/logo.png", use_column_width=True)

        # Navigation menu
        selected_tab = option_menu(
            menu_title="",  # Empty title
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

        # Footer section
        st.markdown(
            """
            <div class="footer">
                <p>© 2024 UMUD | Powered by Open Science</p>
                <p>
                    <a href="https://github.com/UMUD" target="_blank" style="color: white;">GitHub</a> | 
                    <a href="https://umud.org" target="_blank" style="color: white;">Website</a>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_tab