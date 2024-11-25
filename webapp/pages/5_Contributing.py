import streamlit as st
import json
from pathlib import Path
from templates.template_dictionary import template_data
import ast
import streamlit_pydantic as sp
from helpers.pydantic_models import DatasetMetadata

st.set_page_config(page_title="Contributing", page_icon="📊")


st.markdown(
    "<h1 style='text-align: center; '>Universal Musculoskeletal Ultrasound Database</h1>",
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown(
    """
    <div style="padding: 20px; border: 2px solid #008080; border-radius: 10px;">
        <h3 style="text-align: center; color: #000000;">Want to Contribute Your Data to UMUD?</h3>
        <p>
            By sharing your datasets, you help create a valuable resource for researchers worldwide. Follow four steps to contribute: 1. Data Preparation,
            2. Metadata Submission, 3. Metadata Review, 4. Metadata Integration. These steps are explained in detail below.
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
    - Organize your images according to our [sample dataset LINK](https://osf.io/xbawc/?view_only=f1b975a4ef554facb48b0a3236adddef).
""")
# Pydantic form in a styled popover
with st.expander("📝 Fill Out Dataset Metadata", expanded=False):
    st.markdown(
        """
        <p style="color: #008080;">
            Use this form to enter your dataset metadata. Once completed, you can generate and download a JSON file
            for submission. Make sure all fields are correctly filled to comply with UMUD standards.
        </p>
        """,
        unsafe_allow_html=True,
    )
    validated_data = sp.pydantic_form(key="DatasetMetadata", model=DatasetMetadata)

# Generate and download JSON file
if validated_data and st.button("Generate JSON", type="primary"):
    json_data = json.dumps(validated_data.dict(), indent=4)
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="dataset_metadata.json",
        mime="application/json",
    )
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