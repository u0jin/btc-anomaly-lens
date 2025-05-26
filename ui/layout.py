import streamlit as st
from ui.language import get_text
import plotly.graph_objects as go

def show_layout(lang, total_score, short_intervals, outliers):
    t = get_text(lang)

    st.metric(label=t['risk_score'], value=f"{total_score} / 50", help=t['risk_help'])

    with st.expander(t['logic_title']):
        st.markdown(t['logic_description'])

    with st.expander("Short Interval Details"):
        st.write(short_intervals)

    with st.expander("Amount Outliers Detected"):
        st.write(outliers)

def render_interval_chart(short_intervals):
    if not short_intervals:
        st.info("No short intervals to display.")
        return
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=short_intervals,
        nbinsx=10,
        marker_color="lightskyblue",
        name="Interval (sec)"
    ))
    fig.update_layout(
        title="Short Interval Distribution",
        xaxis_title="Interval (seconds)",
        yaxis_title="Frequency",
        bargap=0.2
    )
    st.plotly_chart(fig, use_container_width=True)
