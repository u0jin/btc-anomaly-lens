import streamlit as st
from ui.language import get_text

def show_layout(lang, score, details):
    t = get_text(lang)

    st.metric(label=t['risk_score'], value=f"{score} / 25", help=t['risk_help'])

    with st.expander(t['logic_title']):
        st.markdown(t['logic_description'])

    with st.expander("Short Interval Details"):
        st.write(details)
