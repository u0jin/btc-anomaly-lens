# 🧠 BTC Anomaly Lens

> A real-time Bitcoin anomaly detection and forensic visualization platform built for threat intelligence, portfolio demonstration, and cybersecurity education.

[![Live Demo](https://img.shields.io/badge/🔗%20Portfolio%20App-btc--anomaly--lens.streamlit.app-orange)](https://btc-anomaly-lens.streamlit.app/)
[![Lab Demo](https://img.shields.io/badge/🧪%20Research%20Version-korea--signal.streamlit.app-blue)](https://btc-anomaly-korea-signal.streamlit.app/)
[![GitHub](https://img.shields.io/badge/🔧%20Source%20Code-GitHub-gray)](https://github.com/u0jin/btc-anomaly-lens)
[![Resume](https://img.shields.io/badge/📄%20Resume-You%20Jin%20Kim-green)](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)

---

## 🔍 What is BTC Anomaly Lens?

BTC Anomaly Lens is a forensic-grade Bitcoin transaction analysis system that simulates real-world threat environments. It allows users to:

* Detect abnormal transaction behavior across key heuristics
* Visualize address interaction networks
* Generate analyst-style PDF reports
* Explore address-level risk through modular scores

The system supports **dual deployments**:

| Version                  | Description                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------- |
| 🎯 **Portfolio Version** | Interactive demo with real-time scoring, multilingual UI, and full functionality        |
| 🧪 **Lab Version**       | Lightweight academic tool using free APIs, designed for classroom and research settings |

---

## 💡 Key Use Cases

* **Threat Intelligence Simulation**: Flagging high-risk wallets via score-based patterns
* **Blockchain Forensics Training**: Teaching risk indicators using real Bitcoin datasets
* **Portfolio Presentation**: Demonstrating technical depth in cybercrime detection and UI logic design

---

## 🧠 Detection Logic Overview

| Category               | Logic                                    | Purpose                                             |
| ---------------------- | ---------------------------------------- | --------------------------------------------------- |
| ⏱ Time Interval        | Detects bursts of repeated sends in <60s | Exposes transaction automation or bot activity      |
| 💰 Amount Outliers     | IQR-based outlier flagging               | Identifies high-value anomalies against normal flow |
| 🔁 Repeated Recipients | ≥3 transfers to same address             | Indicates possible laundering / service funneling   |
| 📈 Time Gap Deviation  | <10s or >1h gap patterns                 | Reveals time-series inconsistency                   |
| 🚨 Blacklist Match     | Matches OFAC / threat lists              | Detects sanctioned / darknet-linked addresses       |

Each logic returns a **modular risk score (0-25)** and contributes to a total **Risk Index (0–100)**. All values are visualized with radar charts, score tables, and dynamic warnings.

---

## 📊 Visualization Features

* 📡 Radar chart for anomaly breakdown
* 🔍 Donut charts per logic group
* 📉 Box plots and outlier tables
* 🕸 Address graph visualization (Premium)
* 📄 PDF Report generator with full score & visuals

---

## 🏗️ System Architecture

```plaintext
Input (BTC Address)
       ↓
Data Fetch
  ↳ Free: BlockCypher API
  ↳ Premium: mempool.space API (JSON mempool stream)
       ↓
Preprocessing (tx flattening, sorting, UTXO mapping)
       ↓
Anomaly Detection (5 logics)
       ↓
Score Calculation & Visualization
       ↓
Optionally: Network Graph + PDF Export
```

---

## ⚙️ Tech Stack

* **Framework**: Streamlit (multi-language UI)
* **Core Language**: Python 3.10+
* **Visualization**: Plotly
* **Realtime API**: mempool.space (Premium), BlockCypher (Free)
* **Export**: PDF (via HTML + BytesIO)

---

## 📁 File Structure

```
btc-anomaly-lens/
├── app.py                 ← Streamlit app entry
├── logic/
│   ├── detection.py       ← All scoring logics
│   ├── preprocess.py      ← Cleans & flattens tx data
│   └── report_generator.py← PDF exporter
├── api/
│   ├── fetch.py           ← Handles API calls
│   └── parser.py          ← Normalizes raw tx JSON
├── ui/
│   ├── layout.py          ← Visual component renderers
│   └── language.py        ← Multilingual support
├── data/
│   └── blacklist.txt      ← Sanctioned addresses
├── docs/
│   ├── preview_ui_dashboard.png
│   ├── preview_lab_ui.png
│   └── You Jin Kim — Resume.pdf
└── requirements.txt       ← Dependencies
```

---

## 👤 Creator Profile

**You Jin Kim (김유진)**
M.S. in Information Security @ Korea University
Blockchain Security | Threat Detection | UI Engineering
📧 [yujin.kim@korea.ac.kr](mailto:yujin.kim@korea.ac.kr)
🔗 [GitHub](https://github.com/u0jin)
📄 [Resume (PDF)](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)

---

## 🧭 Vision

> This project is more than a tool — it’s a reflection of initiative, system design thinking, and cybersecurity storytelling.

* 🎯 Designed to match portfolio needs for roles at TRM Labs, Chainalysis, and similar firms
* 🧠 Reproducible for academic and training contexts
* 🛠 Shows real understanding of UTXO structures, risk modeling, and UI/UX interplay

---

## 📜 License

MIT License — Free to use, study, and adapt. Attribution required.
