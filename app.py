import streamlit as st
from ui.layout import show_layout
from ui.language import get_text

def main():
    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    show_layout(lang)

if __name__ == "__main__":
    main()
