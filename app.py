import streamlit as st
import pandas as pd
import plotly.express as px
from ui.layout import show_layout
from ui.language import get_text
from logic.detection import (
    interval_anomaly_score,
    amount_anomaly_score,
    repeated_address_score,
    time_gap_anomaly_score,
    blacklist_score,
    mixer_detection_score,
    cross_chain_detection_score,
    money_laundering_risk_score,
    exchange_detection_score
)
from logic.graph import generate_transaction_network, get_network_stats
from api.fetch import get_transaction_data
from api.parser import parse_mempool_transactions
from logic.preprocess import preprocess
from logic.report_generator import generate_pdf_report
from logic.scenario_matcher import load_scenarios, match_scenarios
import base64
import streamlit as st
import os
from logic.exchange_identifier import identify_exchange_comprehensive

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

# ✅ 헤더 영역 시각적 강조
st.markdown("""
<div style='text-align: center; padding: 12px 0;'>
    <h1 style='color: #08BDBD; font-size: 40px;'>BTC Anomaly Lens</h1>
    <p style='color: #aaa; font-size: 16px;'>Real-time Bitcoin Threat Intelligence Toolkit ｜ Developed by You Jin Kim</p>
</div>
<div style='text-align: center; padding: 10px 0 20px 0; border-bottom: 1px solid #444;'>
    <h3 style='color: #00E1E1;'>🛡️ Real-Time Bitcoin Threat Intelligence</h3>
    <p style='color: #ccc; font-size: 15px; max-width: 800px; margin: auto;'>
        This system simulates field-grade blockchain forensics with real-time anomaly scoring, clustering logic, and interactive reporting. 
        Designed for analysts, researchers, and security platforms seeking to identify suspicious Bitcoin activity through custom behavioral signals.
    </p>
</div>
""", unsafe_allow_html=True)

# ✅ About This Tool
with st.expander("🧠 About This Tool"):
    st.markdown("""
    <div style='font-size:15px;'>
    <b style='color:#08BDBD;'>BTC Anomaly Lens</b> is a forensic-grade Bitcoin anomaly detection platform designed for practical use in threat intelligence and cybercrime investigations.<br><br>

    <b style='color:#00FFFF;'>Core Capabilities:</b>
    <ul style='padding-left:1.2em;'>
        <li><b>Live mempool transaction parsing:</b> Fetches and analyzes unconfirmed Bitcoin transactions in real-time via REST APIs</li>
        <li><b>Custom anomaly scoring engine:</b> Flags abnormal patterns across time intervals, transaction amounts, repeated addresses, and blacklist hits</li>
        <li><b>Semi-heuristic clustering & network visualization:</b> Groups behaviorally linked addresses (e.g., timing, output reuse) and visualizes interactions using on-chain flows</li>
        <li><b>Dynamic fee analysis (Premium Mode):</b> Analyzes mempool fee histograms to detect urgency-driven anomalies or potential obfuscation tactics</li>
        <li><b>PDF report generation:</b> Produces structured, exportable reports suitable for compliance, internal documentation, or regulatory communication</li>
    </ul>

    <p>This system was developed by a researcher specializing in blockchain forensics and anomaly modeling based on UTXO structures. It was originally built for academic validation and has been adapted for field-grade analyst use.</p>

    🔗 <a href='https://github.com/u0jin/btc-anomaly-lens/blob/main/WHITEPAPER.md' target='_blank'><b>📘 View Full Whitepaper</b></a>
    </div>
    """, unsafe_allow_html=True)

def get_dynamic_top_nodes(tx_list, max_hops):
    from logic.graph import get_max_available_nodes
    max_available_nodes = get_max_available_nodes(tx_list, max_hops)
    current_top_nodes = st.session_state.get('top_nodes_slider', 15)
    if current_top_nodes > max_available_nodes:
        current_top_nodes = max_available_nodes
        st.session_state.top_nodes_slider = current_top_nodes
    return max_available_nodes, current_top_nodes

def main():

    st.set_page_config(page_title="BTC Anomaly Lens", layout="wide")
    lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])
    t = get_text(lang)

    st.sidebar.markdown("---")
    premium_mode = st.sidebar.checkbox("🔐 Enable Premium Mode", value=False)
    
    # 🔧 Scenario Matching Threshold 설정
    st.sidebar.markdown(f"#### 🧠 {t['scenario_matching_settings']}")
    min_similarity = st.sidebar.slider(
        f"📊 {t['matching_threshold']}",
        min_value=0,
        max_value=100,
        value=st.session_state.get('min_similarity', 50),
        step=10,
        help=t['matching_threshold_help'],
        key="min_similarity_slider"
    )
    
    # 시나리오 매칭 설정 저장 버튼
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button(f"💾 {t['save_scenario_settings']}", key="save_scenario_settings"):
            st.session_state.min_similarity = min_similarity
            st.session_state.scenario_settings_saved = True
            st.sidebar.success(f"✅ {t['scenario_settings_saved']}")
    
    with col2:
        if st.button(f"🔄 {t['reset_scenario_settings']}", key="reset_scenario_settings"):
            st.session_state.scenario_settings_saved = False
            if 'min_similarity' in st.session_state:
                del st.session_state.min_similarity
            st.sidebar.info(f"🔄 {t['scenario_settings_reset']}")
    
    # 저장된 설정이 있으면 그것을 사용
    final_min_similarity = st.session_state.get('min_similarity', min_similarity) if st.session_state.get('scenario_settings_saved', False) else min_similarity

    st.sidebar.markdown(t["premium_on"] if premium_mode else t["premium_off"])

    st.sidebar.markdown("""
    <span style='font-size:13px; color:gray'>
    🔍 Developed for real-world blockchain forensic simulation.
    </span>
    """, unsafe_allow_html=True)

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
        📄 <a href='https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/📄%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf' target='_blank'>View Resume (PDF)</a><br>
        🔗 <a href='https://github.com/u0jin' target='_blank'>GitHub Profile</a><br>
        📧 yujin5836@gmail.com
        </div>
        """, unsafe_allow_html=True)
    

    st.subheader("Live Transaction Analysis")
    address = st.text_input("Enter a Bitcoin address for live analysis")

    # 분석 버튼
    if st.button("Analyze Address"):
        # 분석 결과를 세션에 저장
        st.session_state.analysis_completed = True
        st.session_state.analysis_address = address.strip() if address else ""
        
        if not st.session_state.analysis_address:
            st.warning("비트코인 주소를 입력해주세요.")
            return
        # 주소 정규화 (앞뒤 공백 제거)
        address = address.strip() if address else ""
        
        if not address:
            st.warning("비트코인 주소를 입력해주세요.")
            return
            
        with st.spinner("Fetching and analyzing transactions..."):
            # 거래소 식별 먼저 실행 (트랜잭션 없어도 주소만으로 결과 반환)
            exchange_result = identify_exchange_comprehensive(address)
            final_result = exchange_result.get('final_result', {})
            description = final_result.get('description', '')
            method = final_result.get('method', '')
            
            # 🏦 거래소 인식 결과 - 깔끔하게 정리
            st.markdown("---")
            st.markdown("### 🏦 거래소 인식 결과")
            
            if final_result.get('exchange'):
                exchange = final_result.get('exchange')
                confidence = final_result.get('confidence', '')
                
                # 신뢰도에 따른 색상 결정
                if confidence == 'very_high':
                    color = "#00BFAE"
                    confidence_text = "매우 높음"
                elif confidence == 'high':
                    color = "#00CED1"
                    confidence_text = "높음"
                elif confidence == 'medium':
                    color = "#FFD700"
                    confidence_text = "보통"
                else:
                    color = "#FFA07A"
                    confidence_text = "낮음"
                
                st.markdown(f"""
                <div style='border: 2px solid {color}; border-radius: 12px; background: {color}22; padding: 20px; margin: 10px 0;'>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 36px;'>🏦</div>
                        <div>
                            <div style='font-size: 24px; font-weight: bold; color: {color}; margin-bottom: 8px;'>
                                {exchange}
                            </div>
                            <div style='font-size: 16px; color: #666; margin-bottom: 8px;'>
                                신뢰도: <span style='color: {color}; font-weight: bold;'>{confidence_text}</span>
                            </div>
                            <div style='font-size: 14px; color: #888;'>
                                {description}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 분석 방법 표시
                if method:
                    method_names = {
                        'official_address': '공식 주소 매칭',
                        'external_label': '외부 라벨링',
                        'cluster_analysis': '클러스터링 분석',
                        'pattern_analysis': '패턴 분석',
                        'address_pattern': '주소 패턴',
                        'address_format_check': '주소 형식 확인'
                    }
                    st.caption(f"🔍 **분석 방법:** {method_names.get(method, method)}")
                    
            else:
                confidence = final_result.get('confidence', '')
                if confidence == 'genesis_block':
                    st.markdown("""
                    <div style='border: 2px solid #FFD700; border-radius: 12px; background: #FFD70022; padding: 20px; margin: 10px 0;'>
                        <div style='display: flex; align-items: center; gap: 15px;'>
                            <div style='font-size: 36px;'>🏛️</div>
                            <div>
                                <div style='font-size: 24px; font-weight: bold; color: #FFD700; margin-bottom: 8px;'>
                                    Genesis 블록 주소
                                </div>
                                <div style='font-size: 16px; color: #666;'>
                                    비트코인 최초 블록 (사토시 나카모토의 지갑)
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                elif confidence == 'valid_btc_address':
                    st.info("✅ 유효한 비트코인 주소 (거래소 주소가 아닐 가능성이 높습니다)")
                elif confidence == 'invalid_address':
                    st.error("❌ 비트코인 주소 형식이 아닙니다")
                else:
                    st.warning("❓ 알 수 없는 주소")

            # 🔎 View Logic 버튼/expander로 상세 근거 및 출처 표시
            with st.expander("🔎 View Logic (근거/출처/로직 상세 보기)"):
                st.markdown("""
                <div style='font-size:15px; color:#08BDBD; font-weight:600;'>
                📚 <b>거래소 인식 근거 및 출처</b>
                </div>
                """, unsafe_allow_html=True)
                # 공식 DB/하드코딩 매칭
                official = exchange_result.get('official_address', {})
                if official.get('found'):
                    st.markdown(f"- <b>공식 DB/하드코딩 매칭</b>: <span style='color:#00BFAE'>{official.get('exchange','')}</span> (출처: {official.get('source','')})", unsafe_allow_html=True)
                # 외부 공개 DB
                public_db = exchange_result.get('public_db', {})
                if public_db.get('found'):
                    tags = ', '.join(public_db.get('exchanges', []))
                    sources = ', '.join(public_db.get('sources', []))
                    st.markdown(f"- <b>외부 공개 DB</b>: <span style='color:#00BFAE'>{tags}</span> (출처: {sources})", unsafe_allow_html=True)
                    # Blockchair 등 외부 링크 제공 (BlockCypher 링크는 제공하지 않음)
                    if 'Blockchair' in sources:
                        st.markdown(f"  - [Blockchair에서 주소 확인](https://blockchair.com/bitcoin/address/{address})")
                # 패턴 분석
                pattern = exchange_result.get('pattern_analysis', {})
                if pattern:
                    st.markdown(f"- <b>패턴 분석</b>: 신뢰도 <span style='color:#00BFAE'>{pattern.get('confidence','')}</span>, 점수: {pattern.get('score','')}", unsafe_allow_html=True)
                    st.markdown(f"  - 주요 패턴: {pattern.get('patterns',{})}")
                # 클러스터 분석
                cluster = exchange_result.get('cluster_analysis', {})
                if cluster:
                    st.markdown(f"- <b>클러스터 분석</b>: 신뢰도 <span style='color:#00BFAE'>{cluster.get('confidence','')}</span>, 클러스터 수: {len(cluster.get('clusters',[]))}", unsafe_allow_html=True)
                # 교차 검증
                cross = exchange_result.get('cross_validation', {})
                if cross:
                    st.markdown(f"- <b>교차 검증</b>: 최종 신뢰도 <span style='color:#00BFAE'>{cross.get('final_confidence','')}</span> (score: {cross.get('validation_score','')}/{cross.get('total_methods','')})", unsafe_allow_html=True)
                # 전체 JSON 보기(디버깅용)
                with st.expander("🔬 Raw Logic JSON (디버깅용)"):
                    import json
                    st.code(json.dumps(exchange_result, ensure_ascii=False, indent=2))
            
            # 트랜잭션 데이터 가져오기
            raw_data = get_transaction_data(address, mode="premium")
            tx_list = parse_mempool_transactions(raw_data)

            if not tx_list:
                st.warning("트랜잭션 데이터를 찾을 수 없습니다. (주소는 유효하지만 거래 내역이 없을 수 있습니다)")
                return

            tx_list = preprocess(tx_list)
            st.success(f"✅ Real blockchain data successfully retrieved via mempool.space")

            interval_score, short_intervals = interval_anomaly_score(tx_list)
            amount_score, outliers = amount_anomaly_score(tx_list)
            address_score, flagged_addresses = repeated_address_score(tx_list)
            time_score, abnormal_gaps = time_gap_anomaly_score(tx_list)
            blacklist_flag, blacklist_score_val = blacklist_score(tx_list)
            mixer_score_val, mixer_indicators = mixer_detection_score(tx_list)
            cross_chain_score_val, cross_chain_indicators = cross_chain_detection_score(tx_list)
            money_laundering_score_val, laundering_indicators = money_laundering_risk_score(tx_list)
            total_score = interval_score + amount_score + address_score + time_score + blacklist_score_val + mixer_score_val + cross_chain_score_val + money_laundering_score_val

            # 거래소 탐지 + 패턴 분석 (새로운 종합 식별 시스템으로 대체)
            exchange_hits, exchange_details, pattern_analysis = exchange_detection_score(tx_list, address)

            scores_dict = {
                "Short Interval Score": interval_score,
                "Amount Outlier Score": amount_score,
                "Repeated Address Score": address_score,
                "Time Gap Score": time_score,
                "Blacklist Score": blacklist_score_val,
                "Mixer Score": mixer_score_val,
                "Cross-chain Score": cross_chain_score_val,
                "Money Laundering Risk Score": money_laundering_score_val
            }

            # 분석 결과를 세션에 저장
            st.session_state.analysis_results = {
                'lang': lang,
                'total_score': total_score,
                'interval_score': interval_score,
                'short_intervals': short_intervals,
                'amount_score': amount_score,
                'outliers': outliers,
                'address_score': address_score,
                'flagged_addresses': flagged_addresses,
                'time_score': time_score,
                'abnormal_gaps': abnormal_gaps,
                'blacklist_score_val': blacklist_score_val,
                'blacklist_flag': blacklist_flag,
                'mixer_score_val': mixer_score_val,
                'mixer_indicators': mixer_indicators,
                'cross_chain_score_val': cross_chain_score_val,
                'cross_chain_indicators': cross_chain_indicators,
                'money_laundering_score_val': money_laundering_score_val,
                'laundering_indicators': laundering_indicators,
                'pattern_analysis': pattern_analysis,
                'tx_list': tx_list,
                'scores_dict': scores_dict
            }

            show_layout(
                lang, total_score,
                interval_score, short_intervals,
                amount_score, outliers,
                address_score, flagged_addresses,
                time_score, abnormal_gaps,
                blacklist_score_val, blacklist_flag,
                mixer_score_val, mixer_indicators,
                cross_chain_score_val, cross_chain_indicators,
                money_laundering_score_val, laundering_indicators,
                exchange_pattern_analysis=pattern_analysis
            )

            if premium_mode:
                scenario_db = load_scenarios()
                tx_stats = {
                    "tx_count": len(tx_list),
                    "avg_interval": sum(short_intervals)/len(short_intervals) if short_intervals else 9999,
                    "reused_address_ratio": len(flagged_addresses) / len(tx_list) if tx_list else 0,
                    "high_fee_flag": any(tx.get("fee", 0) > 500 for tx in tx_list)
                }
                # 시나리오 매칭 임계값 로그 추가
                print(f"🔍 Scenario matching threshold: {final_min_similarity}%")
                scenario_matches = match_scenarios(tx_stats, scenario_db, min_similarity=final_min_similarity)
                print(f"🔍 Found {len(scenario_matches)} matching scenarios")
                
                # 시나리오 매칭 결과도 세션에 저장
                st.session_state.scenario_matches = scenario_matches


                with st.expander("🧠 Scenario Similarity Detection", expanded=True):
                    if scenario_matches:
                        st.markdown("<h5 style='color:#08BDBD;'>🔗 Top Matched Scenarios</h5>", unsafe_allow_html=True)
                        df_match = pd.DataFrame(scenario_matches[:3])
                        fig_sim = px.bar(df_match, x="actor", y="similarity", color="actor", text="similarity",
                                         title="Similarity Scores of Matched Scenarios")
                        st.plotly_chart(fig_sim, use_container_width=True)

                        for match in scenario_matches[:3]:
                            pattern = match.get('pattern', {})  # 이 줄 추가
                            st.markdown(f"""
                            <div style='padding: 10px; border: 1px solid #444; border-radius: 8px; margin-bottom: 10px; font-size:14px;'>
                            <b>ID:</b> {match['id']}<br>
                            <b>Actor:</b> <span style='color:#FFA07A'>{match['actor']}</span><br>
                            <b>Similarity:</b> <span style='color:#00CED1'>{match['similarity']}%</span><br>
                            <b>Description:</b> {match['description']}<br><br>
                            <b style='color:#00E1E1;'>🔍 Pattern Justification</b><br>
                            {"• <b>tx_count ≥ {}</b> → High volume suggests automation<br>".format(pattern['tx_count_min']) if 'tx_count_min' in pattern else ''}
                            {"• <b>avg_interval ≤ {}s</b> → Indicates rapid succession (likely scripts)<br>".format(pattern['avg_interval_max']) if 'avg_interval_max' in pattern else ''}
                            {"• <b>reused_address_ratio ≥ {}</b> → Clustered control signal<br>".format(pattern['reused_address_ratio_min']) if 'reused_address_ratio_min' in pattern else ''}
                            {"• <b>high_fee_flag = {}</b> → May indicate urgency or obfuscation<br>".format(pattern['high_fee_flag']) if 'high_fee_flag' in pattern else ''}
                            </div>
                            """, unsafe_allow_html=True)

                    else:
                        st.info("No matching attack scenarios were detected for this transaction pattern.")

            # 네트워크 시각화 설정
            st.markdown("---")
            st.markdown(f"### 🌐 {t['network_visualization']}")
            
            # 설정 컨테이너
            with st.container():
                st.markdown(f"#### ⚙️ {t['network_settings']}")
                
                # 설정을 2열로 배치
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🔗 Hop 수 설정**")
                    max_hops = st.slider(
                        f"{t['max_hops_setting']}",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.get('max_hops_slider', 3),
                        step=1,
                        help=t['max_hops_help'],
                        key="max_hops_slider"
                    )
                
                with col2:
                    st.markdown("**📊 노드 수 설정**")
                    max_available_nodes, current_top_nodes = get_dynamic_top_nodes(tx_list, max_hops)
                    top_nodes = st.slider(
                        f"{t['max_nodes_setting']}",
                        min_value=5,
                        max_value=max_available_nodes,
                        value=current_top_nodes,
                        step=5,
                        help=f"{t['max_nodes_help']} (최대 {max_available_nodes}개 노드 사용 가능)",
                        key="top_nodes_slider"
                    )
                
                # 현재 설정값 표시
                st.info(f"🎯 {t['current_settings']}: 최대 {max_hops} hop, 상위 {top_nodes}개 노드")
            
            # 네트워크 통계 표시
            network_stats = get_network_stats(tx_list, max_hops)
            if network_stats:
                st.markdown(f"#### 📈 {t['network_stats']}")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(t['total_nodes'], network_stats.get('total_nodes', 0))
                with col2:
                    st.metric(t['total_edges'], network_stats.get('total_edges', 0))
                with col3:
                    st.metric(t['unique_recipients'], network_stats.get('unique_recipients', 0))
                with col4:
                    st.metric(t['total_volume'], f"{network_stats.get('total_volume', 0):.2f} BTC")
            
            # 네트워크 시각화 생성 및 표시
            with st.spinner(f"네트워크 시각화 생성 중... (Hop: {max_hops}, 노드: {top_nodes})"):
                encoded_img = generate_transaction_network(tx_list, max_hops=max_hops, top_n=top_nodes, source_address=address)
                if encoded_img:
                    with st.expander(f"🔸 {t['network_visualization_title']}", expanded=True):
                        st.image(f"data:image/png;base64,{encoded_img}", use_container_width=True)
                        st.caption(t['network_visualization_help'].format(max_hops=max_hops, top_nodes=top_nodes))
                else:
                    st.warning(t['network_visualization_error'])

            if premium_mode:
                pdf_io = generate_pdf_report(address, total_score, scores_dict, scenario_matches, similarity_threshold=min_similarity).getvalue()

                pdf_bytes = generate_pdf_report(address, total_score, scores_dict, scenario_matches=scenario_matches, similarity_threshold=final_min_similarity)
                st.download_button(
                    label="📄 Download Full PDF Report",
                    data=pdf_bytes,
                    file_name="BTC_Anomaly_Report.pdf",
                    mime="application/pdf",
                    help="Download the full anomaly analysis report as a PDF"
                )

            if abnormal_gaps:
                df_gaps = pd.DataFrame(abnormal_gaps, columns=["tx_hash", "gap_seconds"])
                fig_gaps = px.bar(df_gaps, x="tx_hash", y="gap_seconds", title="⏱ Abnormal Time Gaps Detected")
                st.plotly_chart(fig_gaps, use_container_width=True)

    # 분석이 완료된 경우 결과 표시
    elif st.session_state.get('analysis_completed', False):
        # 저장된 분석 결과 사용
        results = st.session_state.analysis_results
        tx_list = results['tx_list']
        scores_dict = results['scores_dict']
        
        # 시나리오 매칭 임계값이 변경되었는지 확인하고 재계산
        current_threshold = st.session_state.get('min_similarity', 50) if st.session_state.get('scenario_settings_saved', False) else min_similarity
        stored_threshold = st.session_state.get('stored_scenario_threshold', None)
        
        # 임계값이 변경되었거나 처음인 경우 시나리오 매칭 재실행
        if stored_threshold != current_threshold:
            print(f"🔍 Recalculating scenarios with new threshold: {current_threshold}%")
            # 저장된 tx_stats와 scenario_db 사용
            tx_stats = results.get('tx_stats', {})
            scenario_db = load_scenarios()
            scenario_matches = match_scenarios(tx_stats, scenario_db, min_similarity=current_threshold)
            st.session_state.scenario_matches = scenario_matches
            st.session_state.stored_scenario_threshold = current_threshold
            print(f"🔍 Found {len(scenario_matches)} matching scenarios")
        else:
            scenario_matches = st.session_state.get('scenario_matches', [])
        
        # 네트워크 시각화 설정
        st.markdown("---")
        st.markdown(f"### 🌐 {t['network_visualization']}")
        
        # 설정 컨테이너
        with st.container():
            st.markdown(f"#### ⚙️ {t['network_settings']}")
            
            # 설정을 2열로 배치
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔗 Hop 수 설정**")
                max_hops = st.slider(
                    f"{t['max_hops_setting']}",
                    min_value=1,
                    max_value=10,
                    value=st.session_state.get('max_hops_slider', 3),
                    step=1,
                    help=t['max_hops_help'],
                    key="max_hops_slider"
                )
            
            with col2:
                st.markdown("**📊 노드 수 설정**")
                max_available_nodes, current_top_nodes = get_dynamic_top_nodes(tx_list, max_hops)
                top_nodes = st.slider(
                    f"{t['max_nodes_setting']}",
                    min_value=5,
                    max_value=max_available_nodes,
                    value=current_top_nodes,
                    step=5,
                    help=f"{t['max_nodes_help']} (최대 {max_available_nodes}개 노드 사용 가능)",
                    key="top_nodes_slider"
                )
            
            # 현재 설정값 표시
            st.info(f"🎯 {t['current_settings']}: 최대 {max_hops} hop, 상위 {top_nodes}개 노드")
        
        # 네트워크 통계 표시
        network_stats = get_network_stats(tx_list, max_hops)
        if network_stats:
            st.markdown(f"#### 📈 {t['network_stats']}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(t['total_nodes'], network_stats.get('total_nodes', 0))
            with col2:
                st.metric(t['total_edges'], network_stats.get('total_edges', 0))
            with col3:
                st.metric(t['unique_recipients'], network_stats.get('unique_recipients', 0))
            with col4:
                st.metric(t['total_volume'], f"{network_stats.get('total_volume', 0):.2f} BTC")
        
        # 네트워크 시각화 생성 및 표시
        with st.spinner(f"네트워크 시각화 생성 중... (Hop: {max_hops}, 노드: {top_nodes})"):
            encoded_img = generate_transaction_network(tx_list, max_hops=max_hops, top_n=top_nodes, source_address=address)
            if encoded_img:
                with st.expander(f"🔸 {t['network_visualization_title']}", expanded=True):
                    st.image(f"data:image/png;base64,{encoded_img}", use_container_width=True)
                    st.caption(t['network_visualization_help'].format(max_hops=max_hops, top_nodes=top_nodes))
            else:
                st.warning(t['network_visualization_error'])

    if premium_mode:
        st.markdown("### 📊 Premium Features")
        

        # (fee histogram expander 및 관련 코드 전체 삭제)
    else:
        st.caption("Premium features such as PDF export and darknet detection are unavailable in free mode.")

if __name__ == "__main__":
    main()
