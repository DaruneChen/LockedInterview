import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(page_title="LockedInterview", layout="wide")

# Load CSS
css_path = Path("frontend.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Load your existing HTML (the big file with mic + camera + JS)
html_path = Path("frontend.html")
if not html_path.exists():
    st.error("frontend.html not found in this folder.")
else:
    html_code = html_path.read_text()
    # Render the whole app inside Streamlit
    components.html(html_code, height=900, scrolling=True)
