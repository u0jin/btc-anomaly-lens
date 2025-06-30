import streamlit as st
import pandas as pd
import plotly.express as px
from ui.layout import show_layout, render_interval_chart
from ui.language import get_text
from logic.detection import (
    interval_anomaly_score,
    amount_anomaly_score,
    repeated_address_score,
    time_gap_anomaly_score,
    blacklist_score
)
from logic.graph import generate_transaction_network
from api.fetch import get_transaction_data, fetch_fee_histogram
from api.parser import parse_blockcypher_transactions, parse_mempool_transactions
from logic.preprocess import preprocess

# 💎 버튼 스타일 전역 적용
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

def main():
    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    t = get_text(lang)

    # 🔒 프리미엄 모드 설정
    st.sidebar.markdown("---")
    premium_mode = st.sidebar.checkbox("🔐 Enable Premium Mode", value=False)
    st.sidebar.markdown(t["premium_on"] if premium_mode else t["premium_off"])

    # 사이드 목적 설명
    st.sidebar.markdown("""
    <span style='font-size:13px; color:gray'>
    🔍 Developed for real-world blockchain forensic simulation.
    </span>
    """, unsafe_allow_html=True)

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

    # 🔷 인트로 섹션 강화
    st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='color: #08BDBD;'>BTC Anomaly Lens</h2>
        <p style='color: #555;'>Real-time Bitcoin Threat Intelligence Toolkit ｜ Developed by You Jin Kim</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🧠 About This Tool"):
        st.markdown("""
        **BTC Anomaly Lens** is a forensic-grade Bitcoin anomaly detection tool designed for real-time threat simulation. This tool integrates:

        - 📡 Live mempool transaction analysis
        - 🧠 Custom anomaly scoring algorithms
        - 🕸 Forensic clustering and network visualization
        - 📊 Dynamic fee analysis (Premium Mode)

        Built with a deep understanding of blockchain structures (UTXO) and cybercrime patterns.
        """)

    # 🧪 주소 입력
    st.subheader("Live Transaction Analysis")
    address = st.text_input("Enter a Bitcoin address for live analysis")

    if st.button("Analyze Address"):
        with st.spinner("Fetching and analyzing transactions..."):
            raw_data = get_transaction_data(address, mode="premium" if premium_mode else "free")
            tx_list = (
                parse_mempool_transactions(raw_data)
                if premium_mode else
                parse_blockcypher_transactions(raw_data)
            )

            if not tx_list:
                st.error("No valid transactions found or address is invalid.")
                return

            tx_list = preprocess(tx_list)

            st.success(f"✅ Real blockchain data successfully retrieved via {'mempool.space' if premium_mode else 'BlockCypher'}")

            # 점수 계산
            interval_score, short_intervals = interval_anomaly_score(tx_list)
            amount_score, outliers = amount_anomaly_score(tx_list)
            address_score, flagged_addresses = repeated_address_score(tx_list)
            time_score, abnormal_gaps = time_gap_anomaly_score(tx_list)
            blacklist_flag, blacklist_score_val = blacklist_score(tx_list)
            total_score = interval_score + amount_score + address_score + time_score + blacklist_score_val

            # 🔍 결과 시각화 출력
            show_layout(
                lang, total_score,
                interval_score, short_intervals,
                amount_score, outliers,
                address_score, flagged_addresses,
                time_score, abnormal_gaps,
                blacklist_score_val, blacklist_flag
            )

            # 🕸 네트워크 그래프 (프리미엄 전용)
            if premium_mode:
                encoded_img = generate_transaction_network(tx_list)
                if encoded_img:
                    with st.expander("🕸 Transaction Flow Network", expanded=False):
                        st.image(f"data:image/png;base64,{encoded_img}", use_column_width=True)

            # API 호출 정보
            with st.expander("🔍 API Access Info"):
                source = "mempool.space" if premium_mode else "BlockCypher.com"
                endpoint = (
                    f"GET /address/{address}/txs" if premium_mode
                    else f"GET /addrs/{address}/full?token=****"
                )
                st.markdown(f"**Access Mode:** {'Premium' if premium_mode else 'Free'} (Live API)\n\n**Source:** {source}")
                st.code(endpoint, language="http")

    # 📊 프리미엄 기능 안내 및 시각화
    if premium_mode:
        st.markdown("### 📊 Premium Features")
        st.info("Advanced clustering visualization and darknet address correlation are under development.")
        st.markdown("""
        - Real-time mempool anomaly map (Coming Soon)<br>
        - Address graph network visualization ✅<br>
        - Dynamic fee risk estimation (Coming Soon)
        """, unsafe_allow_html=True)

        with st.expander("💸 Fee Rate Distribution (mempool.space)", expanded=False):
            fee_data = fetch_fee_histogram()
            if fee_data:
                df_fee = pd.DataFrame(fee_data)
                df_fee["fee_label"] = df_fee["feeRange"].apply(lambda r: f"{r[0]}-{r[1]} sat/vB")
                y_col = "nTx" if "nTx" in df_fee.columns else "totalFees"
                fig_fee = px.bar(df_fee, x="fee_label", y=y_col, title="💸 Fee Rate Distribution in Mempool")
                st.plotly_chart(fig_fee, use_container_width=True)
            else:
                st.warning("❌ Failed to fetch mempool fee histogram.")

        if st.button("📝 Export Analysis Report (PDF)"):
            st.warning("PDF export is a premium-only feature. Subscribe or enable enterprise mode to access this.")
    else:
        st.caption("Premium features such as PDF export and darknet detection are unavailable in free mode.")

if __name__ == "__main__":
    main()