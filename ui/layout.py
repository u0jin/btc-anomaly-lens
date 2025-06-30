import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ui.language import get_text

# 💎 프리미엄 UI 스타일 적용
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #08BDBD;
    color: white;
    font-weight: 600;
    padding: 0.6em 1.2em;
    border-radius: 8px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #0a9a9a;
}
</style>
""", unsafe_allow_html=True)

# 사이드바에 툴 목적 명시
st.sidebar.markdown("""
<span style='font-size:13px; color:gray'>
🔍 This tool is developed as part of a real-world blockchain forensic system, simulating TRM-style risk detection.
</span>
""", unsafe_allow_html=True)

def show_layout(
    lang, total_score,
    interval_score, short_intervals,
    amount_score, outliers,
    address_score, flagged_addresses,
    time_score, abnormal_gaps,
    blacklist_score_val, blacklist_flag
):
    t = get_text(lang)

    display_score = min(total_score, 100)

    with st.expander("📊 Risk Score Breakdown (Donut Chart)", expanded=False):
        score_parts = {
            "Interval": interval_score,
            "Amount": amount_score,
            "Address": address_score,
            "TimeGap": time_score,
            "Blacklist": blacklist_score_val
        }
        fig_donut = px.pie(
            names=list(score_parts.keys()),
            values=list(score_parts.values()),
            hole=0.5,
            title="Risk Score Composition"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown(f"<h4>{t['total_score']}: <span style='color:#FF4B4B'>{display_score:.1f} / 100</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-weight:500; color:#ccc;'>This score is calculated from multiple behavioral anomaly metrics designed to reflect forensic risk in live BTC traffic.</p>", unsafe_allow_html=True)
    if total_score > 100:
        st.caption("⚠️ One or more critical anomalies detected. Total score capped at 100.")

    with st.expander("📊 Radar Chart"):
        radar_data = {
            "항목": ["간격", "금액", "주소", "시계열", "블랙리스트"],
            "점수": [
                interval_score / 25 * 100,
                amount_score / 25 * 100,
                address_score / 25 * 100,
                time_score / 15 * 100,
                blacklist_score_val
            ]
        }
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_data["점수"],
            theta=radar_data["항목"],
            fill='toself',
            name='Risk Profile'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    def score_section(title, logic_md, score_val, max_score, none_msg, chart_fn=None):
        with st.container():
            st.markdown(f"### {title}")
            with st.popover(t['view_logic']):
                st.markdown(logic_md, unsafe_allow_html=True)
            st.markdown(f"**{t['score']}:** {score_val:.1f} / {max_score}")
            if chart_fn:
                chart_fn()
            else:
                st.info(none_msg)

    def interval_chart():
        if short_intervals:
            df = pd.DataFrame(short_intervals, columns=[t['interval_chart_label']])
            fig = px.histogram(df, x=t['interval_chart_label'], nbins=20, title=t['interval_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['interval_none'])

    def amount_chart():
        if outliers:
            df = pd.DataFrame(outliers, columns=[t['amount_chart_label']])
            fig = px.box(df, y=t['amount_chart_label'], title=t['amount_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['amount_none'])

    def address_chart():
        if flagged_addresses:
            df = pd.DataFrame(flagged_addresses, columns=[t['address_chart_label']])
            fig = px.histogram(df, x=t['address_chart_label'], title=t['address_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['address_none'])

    def timegap_chart():
        if abnormal_gaps:
            df = pd.DataFrame(abnormal_gaps, columns=[t['timegap_chart_label']])
            fig = px.histogram(df, x=t['timegap_chart_label'], nbins=20, title=t['timegap_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['timegap_none'])

    score_section("⏱️ " + t['interval_title'], t['interval_logic_md'], interval_score, 25, t['interval_none'], interval_chart)
    score_section("💰 " + t['amount_title'], t['amount_logic_md'], amount_score, 25, t['amount_none'], amount_chart)
    score_section("🔁 " + t['address_title'], t['address_logic_md'], address_score, 25, t['address_none'], address_chart)
    score_section("📉 " + t['timegap_title'], t['timegap_logic_md'], time_score, 15, t['timegap_none'], timegap_chart)

    with st.container():
        st.markdown(f"### 🚫 {t['blacklist_title']}")
        with st.popover(t['view_logic']):
            st.markdown(t['blacklist_logic_md'], unsafe_allow_html=True)
        st.markdown(f"**{t['score']}:** {blacklist_score_val:.1f} / 100")
        if blacklist_flag:
            st.error(t['blacklist_flagged'])
            st.caption("⚠️ This address is associated with known sanctioned or darknet entities.")
        else:
            st.success(t['blacklist_safe'])
            st.caption("✅ No critical blacklist match found. Address appears clean.")

        if total_score >= 75:
            st.warning("🔍 This address exhibits highly suspicious behavior and matches several risk factors including timing, repetition, and potential sanctioning.")
        elif total_score >= 50:
            st.info("⚠️ This address has moderate anomalies that may warrant further investigation.")
        else:
            st.success("🟢 No significant anomalies detected. Address shows normal transaction behavior.")

# 🔧 확장용 placeholder
def render_interval_chart(data):
    pass