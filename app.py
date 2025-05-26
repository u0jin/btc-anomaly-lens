import streamlit as st
from ui.layout import show_layout
from ui.language import get_text
from logic.detection import interval_anomaly_score

def main():
    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    t = get_text(lang)

    st.title(t["title"])
    st.caption(t["caption"])

    # 입력창 (실제 주소 대신 지금은 더미 데이터)
    st.subheader("Sample Transaction Analysis")
    if st.button("Run Interval Anomaly Detection"):
        # 더미 트랜잭션 리스트 (ISO format timestamps)
        tx_list = [
            {"timestamp": "2024-01-01T00:00:00"},
            {"timestamp": "2024-01-01T00:00:45"},
            {"timestamp": "2024-01-01T00:02:10"},
            {"timestamp": "2024-01-01T00:03:00"},
            {"timestamp": "2024-01-01T00:03:50"},
        ]
        score, details = interval_anomaly_score(tx_list)
        show_layout(lang, score, details)

if __name__ == "__main__":
    main()
