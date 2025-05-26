import streamlit as st
from ui.layout import show_layout, render_interval_chart
from ui.language import get_text
from logic.detection import interval_anomaly_score, amount_anomaly_score

def main():
    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    t = get_text(lang)

    # Sidebar: About the Creator (세련된 구성)
    with st.sidebar.expander("🧑‍💻 About the Creator", expanded=False):
        st.markdown("""
        <div style='line-height: 1.7; font-size: 14px;'>
        <strong>You Jin Kim</strong><br>
        M.S. in Information Security, Korea University<br>
        Cybersecurity Researcher specializing in blockchain anomaly detection and threat intelligence.<br><br>

        🧪 <strong>Research Focus:</strong><br>
        - Bitcoin crime wallet clustering<br>
        - Time-series & topological modeling<br>
        - Real-time risk scoring engine<br><br>

        🛠 <strong>Technical Stack:</strong><br>
        Python, SQL, REST APIs, WebRTC, Git, Linux<br>
        Blockchain analysis, Static code analysis, Web security<br><br>

        📄 <a href='https://github.com/u0jin/btc-anomaly-lens//docs/ You Jin Kim — Resume.pdf' target='_blank'>View Resume (PDF)</a><br>
        🔗 <a href='https://github.com/u0jin' target='_blank'>GitHub Profile</a><br>
        📧 yujin5836@gmail.com
        </div>
        """, unsafe_allow_html=True)

    # 상단 소개 영역
    st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='color: #08BDBD;'>BTC Anomaly Lens</h2>
        <p style='color: #999;'>Developed by You Jin Kim ｜ Blockchain Security Researcher</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Sample Transaction Analysis")

    if st.button("Run Full Anomaly Analysis"):
        tx_list = [
            {"timestamp": "2024-01-01T00:00:00", "amount": 0.5},
            {"timestamp": "2024-01-01T00:00:45", "amount": 0.8},
            {"timestamp": "2024-01-01T00:02:10", "amount": 1.0},
            {"timestamp": "2024-01-01T00:03:00", "amount": 4.0},
            {"timestamp": "2024-01-01T00:03:50", "amount": 0.9}
        ]
        interval_score, short_intervals = interval_anomaly_score(tx_list)
        amount_score, outliers = amount_anomaly_score(tx_list)

        total_score = interval_score + amount_score
        show_layout(lang, total_score, short_intervals, outliers)
        render_interval_chart(short_intervals)

if __name__ == "__main__":
    main()
