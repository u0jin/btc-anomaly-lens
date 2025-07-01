# BTC Anomaly Lens — Whitepaper

## 1. Overview

**BTC Anomaly Lens** is a forensic-grade Bitcoin anomaly detection system designed for real-time threat simulation. This tool leverages live blockchain APIs to analyze suspicious activity patterns, produce quantifiable risk scores, and generate interactive visualizations and downloadable PDF reports.

* **Developer**: You Jin Kim
* **Institution**: Korea University, Graduate School of Information Security
* **Tech Stack**: Python, Streamlit, Plotly, REST API, Graphviz, PDFKit, base64

The system is optimized for security researchers, blockchain analysts, and intelligence teams working with high-volume UTXO-based transaction data.

---

## 2. System Architecture

### 2.1 Data Collection Layer

* **Free Mode**: Fetches address-based transaction history using `BlockCypher` API.
* **Premium Mode**: Ingests live mempool transaction data and dynamic fee histogram via `mempool.space` API.

📄 Implemented in: [`api/fetch.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/api/fetch.py)

### 2.2 Transaction Parsing

* Parses transaction timestamps, output addresses, and BTC values into a standardized list format.
* Two parsing modes: `parse_blockcypher_transactions()` and `parse_mempool_transactions()`.

📄 Implemented in: [`api/parser.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/api/parser.py)

### 2.3 Preprocessing

* Sorts and filters transactions, normalizes timestamp formats, and deduplicates address data.

📄 Implemented in: [`logic/preprocess.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/preprocess.py)

---

## 3. Detection Logic

BTC Anomaly Lens evaluates a Bitcoin address based on five anomaly signals. Each signal is scored from 0 to 25, forming a cumulative Risk Score out of 100.

| Metric                 | Description                                                 | Function Used              |
| ---------------------- | ----------------------------------------------------------- | -------------------------- |
| Short Interval Score   | Detects bursts of transactions in short windows             | `interval_anomaly_score()` |
| Amount Outlier Score   | Identifies statistically abnormal transaction sizes         | `amount_anomaly_score()`   |
| Repeated Address Score | Flags repeated interactions with the same address           | `repeated_address_score()` |
| Time Gap Score         | Finds suspicious inactivity gaps or bursts                  | `time_gap_anomaly_score()` |
| Blacklist Score        | Checks against known sanctioned addresses (e.g., OFAC, TRM) | `blacklist_score()`        |

📄 Implemented in: [`logic/detection.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/detection.py)

---

## 4. Visualization Features

* **Abnormal Time Gaps**: Plotly bar chart highlighting suspicious time intervals.
* **Transaction Network Graph**: PNG image of transactional flow using Graphviz and PIL.
* **Dynamic PDF Reports**: Generated on-demand via Streamlit download button.
* **Multilingual Support**: Interface toggles between English and Korean.

📄 Layout/UI: [`ui/layout.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/ui/layout.py)

---

## 5. Mode Comparison

| Feature                     | Free Mode (BlockCypher)      | Premium Mode (mempool.space) |
| --------------------------- | ---------------------------- | ---------------------------- |
| Data Source                 | Historical address-based TXs | Real-time mempool TX stream  |
| Fee Histogram Visualization | Not supported                | Supported                    |
| Darknet/Blacklist Analysis  | Supported                    | Supported                    |
| Network Graph Visualization | Supported                    | Supported                    |
| PDF Export                  | Not supported                | Available                    |

---

## 6. Output & Reporting

* **Risk Score Summary**: Total score out of 100 with metric-level breakdown.
* **Flagged Transactions**: Highlighted anomalies by detection type.
* **Visual Analytics**: Graphs and charts embedded in UI.
* **Downloadable Report**: PDF format for offline investigation.

📄 PDF Generator: [`logic/report_generator.py`](https://github.com/u0jin/btc-anomaly-lens/blob/main/logic/report_generator.py)

---

## 7. Use Case Simulation

Imagine an analyst enters a suspicious Bitcoin address linked to potential ransomware activity. The system:

1. Fetches real-time transactions.
2. Applies anomaly scoring functions.
3. Detects 3 out of 5 indicators as suspicious.
4. Displays a total risk score of 72/100.
5. Offers network graph of all involved addresses.
6. Generates a downloadable PDF report with all metrics and visualizations.

This simulates a typical threat intelligence workflow used in TRM Labs or Chainalysis.

---

## 8. Detection Logic Justification

The scoring metrics are grounded in practical and academic precedent:

* **Burst Detection**: Used in detecting mixer patterns and scam bots.
* **Outlier Analysis**: Based on IQR and deviation from moving averages.
* **Blacklist Matching**: Cross-referenced with TRM Labs and OFAC datasets.
* **Time Gaps**: Exploited in fraud/malware campaigns to obfuscate activity.
* **Repeated Address Traces**: Indicates reuse behavior common in phishing campaigns.

Each function is modular and independently validated in `logic/detection.py`.

---

## 9. Future Work & Extensibility

* Support for Ethereum and ERC-20 anomaly flows.
* Custom rule creation via YAML or UI.
* Visual mempool map for real-time alerts.
* RESTful API for enterprise integrations.
* Darknet cluster graph expansion.

These extensions can position BTC Anomaly Lens as a lightweight, deployable node for blockchain SIEM systems.

---

## 10. Integration & Collaboration Readiness

* The system can be converted into a Dockerized microservice.
* Logic components are easily testable and independently callable.
* Report engine (`report_generator.py`) can integrate with CI/CD forensic pipelines.
* Built for analyst readability, not just developer control.
* PDF and graph exports follow static asset convention.

These features open collaboration potential with TRM Labs, Chainalysis, Elliptic, or government bodies.

---

## 11. Codebase Integrity

This whitepaper reflects the actual implementation without exaggeration or hypothetical claims. Every method, score logic, and visualization output is verifiably used within the codebase hosted at:
🔗 [https://github.com/u0jin/btc-anomaly-lens](https://github.com/u0jin/btc-anomaly-lens)

---

## 12. Author & Contact

**You Jin Kim**
M.S. Candidate in Information Security, Korea University
Cybersecurity Researcher specializing in:

* Blockchain anomaly detection
* Bitcoin wallet clustering
* UTXO-based behavioral modeling

📧 [yujin5836@gmail.com](mailto:yujin5836@gmail.com)
🔗 [GitHub Profile](https://github.com/u0jin)
📄 [Resume (PDF)](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)

---

**Last Updated**: July 2025
