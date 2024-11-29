import streamlit as st


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