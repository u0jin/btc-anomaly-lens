import streamlit as st
from ui.layout import show_layout, render_interval_chart
from ui.language import get_text
from logic.detection import (
    interval_anomaly_score,
    amount_anomaly_score,
    repeated_address_score,
    time_gap_anomaly_score,
    blacklist_score
)

def main():
    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    t = get_text(lang)

    # 🔒 프리미엄 모드 설정
    st.sidebar.markdown("---")
    premium_mode = st.sidebar.checkbox("🔐 Enable Premium Mode", value=False)
    st.sidebar.markdown(t["premium_on"] if premium_mode else t["premium_off"])

    # 🧑‍💻 개발자 소개
    with st.sidebar.expander(f"🧑‍💻 {t['creator_section']}", expanded=False):
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
        📄 <a href='https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf' target='_blank'>View Resume (PDF)</a><br>
        🔗 <a href='https://github.com/u0jin' target='_blank'>GitHub Profile</a><br>
        📧 yujin5836@gmail.com
        </div>
        """, unsafe_allow_html=True)

    # 🪧 상단 제목
    st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='color: #08BDBD;'>BTC Anomaly Lens</h2>
        <p style='color: #999;'>Developed by You Jin Kim ｜ Blockchain Security Researcher</p>
    </div>
    """, unsafe_allow_html=True)

    # 🧪 사용자 주소 입력
    st.subheader("Live Transaction Analysis")
    address = st.text_input("Enter a Bitcoin address for live analysis")

    if st.button("Analyze Address"):
        from api.fetch import get_transaction_data
        from api.parser import parse_blockcypher_transactions

        with st.spinner("Fetching and analyzing transactions..."):
            raw_data = get_transaction_data(address, mode="premium" if premium_mode else "free")
            tx_list = parse_blockcypher_transactions(raw_data)

            if not tx_list:
                st.error("No valid transactions found or address is invalid.")
            else:
                st.success("✅ Real blockchain data successfully retrieved via BlockCypher token")

                # 점수 계산
                interval_score, short_intervals = interval_anomaly_score(tx_list)
                amount_score, outliers = amount_anomaly_score(tx_list)
                address_score, flagged_addresses = repeated_address_score(tx_list)
                time_score, abnormal_gaps = time_gap_anomaly_score(tx_list)
                blacklist_flag, blacklist_score_val = blacklist_score(tx_list)

                # 총합 점수 계산
                total_score = interval_score + amount_score + address_score + time_score + blacklist_score_val

                # 🔍 결과 출력
                show_layout(
                    lang, total_score,
                    interval_score, short_intervals,
                    amount_score, outliers,
                    address_score, flagged_addresses,
                    time_score, abnormal_gaps,
                    blacklist_score_val, blacklist_flag
                )

                # API 요청 정보
                with st.expander("🔍 API Access Info"):
                    st.markdown(f"""
                    **Access Mode:** {'Premium' if premium_mode else 'Free'} (Token-authenticated)  
                    **Source:** BlockCypher.com
                    """, unsafe_allow_html=True)
                    st.code(f"GET /addrs/{address}/full?token=****", language="http")

    # 🔒 프리미엄 기능 안내
    if premium_mode:
        st.markdown("### 📊 Premium Features")
        st.info("Advanced clustering visualization and darknet address correlation are under development.")
        st.markdown("""
        - Real-time mempool anomaly map (Coming Soon)  
        - Address graph network visualization (Coming Soon)  
        - Dynamic fee risk estimation (Coming Soon)
        """, unsafe_allow_html=True)

        if st.button("📝 Export Analysis Report (PDF)"):
            st.warning("PDF export is a premium-only feature. Subscribe or enable enterprise mode to access this.")
    else:
        st.caption("Premium features such as PDF export and darknet detection are unavailable in free mode.")

if __name__ == "__main__":
    main()
