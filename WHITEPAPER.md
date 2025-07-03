# BTC Anomaly Lens — Whitepaper

## 1. Overview

**BTC Anomaly Lens** is a forensic-grade Bitcoin anomaly detection system designed for real-time threat simulation and scenario pattern matching. It evaluates blockchain activity through behavioral heuristics, anomaly scoring, and visual reporting.

* **Developer**: You Jin Kim  
* **Institution**: Korea University, Graduate School of Information Security  
* **Tech Stack**: Python, Streamlit, Plotly, REST API, Graphviz, ReportLab, base64  

---

## 2. System Architecture

### 2.1 Data Collection Layer

- **Free Mode**: Retrieves address-based transaction history using the `BlockCypher` API.
- **Premium Mode**: Streams unconfirmed mempool data with fee histograms via `mempool.space`.

📄 [`api/fetch.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/api/fetch.py)

### 2.2 Transaction Parsing

- Parses transactions into a unified structure with timestamp, amount, fee, and recipient address.

📄 [`api/parser.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/api/parser.py)

### 2.3 Preprocessing

- Normalizes time, deduplicates data, prepares for scoring.

📄 [`logic/preprocess.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/preprocess.py)

---

## 3. Detection Logic

BTC Anomaly Lens evaluates an address using five scoring components. Each component contributes up to 25 points (total score: 100):

| Metric                 | Description                                                 | Function Used              |
| ---------------------- | ----------------------------------------------------------- | -------------------------- |
| Short Interval Score   | Detects bursts in transaction frequency                     | `interval_anomaly_score()` |
| Amount Outlier Score   | Flags unusually large/small transfers                       | `amount_anomaly_score()`   |
| Repeated Address Score | Detects reuse of the same recipient                         | `repeated_address_score()` |
| Time Gap Score         | Finds inactivity spikes or silent bursts                    | `time_gap_anomaly_score()` |
| Blacklist Score        | Matches known malicious addresses (e.g., OFAC, TRM)         | `blacklist_score()`        |

📄 [`logic/detection.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/detection.py)

---

## 4. Scenario Similarity Matching

A newly introduced engine compares transaction patterns against predefined criminal scenarios such as:

- Darknet Market Flows
- Sextortion Campaigns
- Mixing / Tumbler Automation
- Blackmail Fraud

### Matching Criteria:
- `tx_count`, `avg_interval`, `reused_address_ratio`, `high_fee_flag`

📌 Similarity threshold is **user-controlled** in the UI (default: 50%).

📄 [`logic/scenario_matcher.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/scenario_matcher.py)

---

## 5. Visualization Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Abnormal Time Gaps            | Plotly bar chart for suspicious inactivity bursts                          |
| Transaction Flow Graph        | Graphviz-based network diagram for flow reconstruction                     |
| Radar Risk Profile            | Matplotlib radar chart with 5 anomaly signals                              |
| Scenario Similarity Bar Chart | Auto-generated bar chart of matched scenarios and similarity percentages   |
| PDF Report with Embedded Visuals | All of the above visuals embedded into downloadable PDF                    |

📄 [`logic/report_generator.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/report_generator.py)  
📄 [`logic/graph_utils.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/graph_utils.py)

---

## 6. User Interface (Streamlit)

- Multilingual support (🇺🇸 English / 🇰🇷 Korean)
- Sidebar configuration:
  - Premium mode toggle
  - Similarity threshold slider
  - Creator info section
- Real-time parsing, scoring, visual output

📄 [`app.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/app.py)

---

## 7. PDF Report Structure

Each address analysis includes:

- 🧾 Risk Summary (Score, Grade, Reason)
- 📌 Metric Table (5 detection components)
- 📊 Radar Chart (visual anomaly fingerprint)
- 📉 Scenario Similarity Bar Chart (if matches exist)
- 📄 Matching Summary:
  - Threshold value used (e.g., “Matches ≥ 50% similarity”)
  - Explanation of each pattern justification
- 🧠 Analyst Notes + Actionable Recommendations

---

## 8. Use Case Simulation

> Suppose an analyst inspects a suspicious address linked to phishing:

1. Address is analyzed with a 30% similarity threshold.
2. System detects 4 anomaly metrics, scoring 78/100.
3. 3 known attacker patterns matched with ≥50% similarity.
4. Graph of matched scenarios is rendered inside the PDF report.
5. Final report exported as `BTC_Anomaly_Report.pdf`.

---

## 9. Technical Soundness

- All graphs use non-interactive image formats (PIL, base64, PNG).
- Temporary files auto-cleaned after PDF generation.
- Code strictly avoids use of external JS or browser-dependent libraries for report output.
- Each anomaly function is self-contained and independently testable.

---

## 10. Future Work

- Ethereum layer support (ERC-20 anomaly modeling)

---

## 11. Repository & Verification

> All implementation details mentioned here are verifiably used in the public repo:

🔗 [https://github.com/u0jin/btc-anomaly-lens](https://github.com/u0jin/btc-anomaly-lens)

---

## 12. Author & Contact

**You Jin Kim**  
M.S. Candidate in Information Security, Korea University  
Focus: Bitcoin wallet clustering, behavioral forensics, UTXO analysis  

📧 [yujin5836@gmail.com](mailto:yujin5836@gmail.com)  
🔗 [GitHub](https://github.com/u0jin)  
📄 [Resume (PDF)](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)

---

**Last Updated**: July 2025
