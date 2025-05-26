import streamlit as st
from ui.language import get_text

def show_layout(lang):
    t = get_text(lang)
    st.markdown(f"### {t['title']}")
    st.caption(t['caption'])
    st.metric(label=t['risk_score'], value="86 / 100", delta="+20", help=t['risk_help'])

    with st.expander(t['logic_title']):
        st.markdown(t['logic_description'])
