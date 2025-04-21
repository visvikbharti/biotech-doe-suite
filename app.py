import streamlit as st
from src.components import introduction, fundamentals, process, design_types, analysis, case_studies, summary

st.set_page_config(
    page_title="Biotech DOE Mastery Suite",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main navigation
st.sidebar.title("Biotech DOE Mastery Suite")
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "Select a module:",
    ["Introduction", "Fundamental Concepts", "Experimental Design Process", 
     "Design Types", "Analysis & Interpretation", "Case Studies", "Summary & Integration"]
)

# User profile settings in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("## User Settings")
user_focus = st.sidebar.selectbox(
    "Application Focus:",
    ["Academic", "Industry - Biopharma", "Industry - Industrial Biotech", "Regulatory"]
)

user_experience = st.sidebar.select_slider(
    "Experience Level:",
    options=["Beginner", "Intermediate", "Advanced", "Expert"]
)

# Add a sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 Vishal Bharti")
st.sidebar.markdown("Version 1.0.0")

# Display appropriate page based on selection
if page == "Introduction":
    introduction.show()
elif page == "Fundamental Concepts":
    fundamentals.show()
elif page == "Experimental Design Process":
    process.show()
elif page == "Design Types":
    design_types.show()
elif page == "Analysis & Interpretation":
    analysis.show()
elif page == "Case Studies":
    case_studies.show()
elif page == "Summary & Integration":
    summary.show()