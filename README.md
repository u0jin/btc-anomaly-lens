# 🧠 BTC Anomaly Lens

> A real-time Bitcoin anomaly detection platform for blockchain forensic research, academic education, and cybersecurity intelligence.

[![Streamlit](https://img.shields.io/badge/🔗%20Portfolio%20Live%20App-btc--anomaly--lens.streamlit.app-orange)](https://btc-anomaly-lens.streamlit.app/)
[![Streamlit](https://img.shields.io/badge/🧪%20Research%20Lab%20Demo-korea--signal.streamlit.app-blue)](https://btc-anomaly-korea-signal.streamlit.app/)
[![GitHub](https://img.shields.io/badge/🔧%20Source%20Code-GitHub-gray)](https://github.com/u0jin/btc-anomaly-lens)
[![Resume](https://img.shields.io/badge/📄%20Resume-You%20Jin%20Kim-green)](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)

---

## 💡 About

**BTC Anomaly Lens** is a Bitcoin transaction anomaly detector that supports two versions:

- 🎯 **Portfolio Version**: Professional-grade, real-time detection tool with multi-logic scoring, dynamic visualizations, and blacklist matching.
- 📚 **Research Lab Version**: Lightweight educational version using free API only, designed for student use and open demonstrations.

Built by **You Jin Kim**, a cybersecurity researcher at Korea University.

---

## 🚀 Live Apps

| Version | Link | Description |
|--------|------|-------------|
| 🌐 **Portfolio** | [btc-anomaly-lens.streamlit.app](https://btc-anomaly-lens.streamlit.app/) | TRM Labs-ready professional UI with advanced logic |
| 🏫 **Lab Demo** | [btc-anomaly-korea-signal.streamlit.app](https://btc-anomaly-korea-signal.streamlit.app/) | Free version used for research and internal deployment |

---

## 🔍 Key Features

| Detection Module | Description |
|------------------|-------------|
| ⏱ Time Interval Anomaly | Detects repeated transfers within 60 seconds |
| 💰 Amount Outlier Detection | Uses IQR to flag outlier BTC amounts |
| 🔁 Repeated Receiver Pattern | Detects 3+ times repeated recipients |
| 📈 Time Gap Anomaly | Flags extreme timing gaps (<10s or >1h) |
| 🚨 Blacklist Matching | OFAC / TRM / internal addresses detection |

🧮 Risk Score is calculated by modular functions and visualized via:
- Radar charts
- Donut charts
- Box plots
- Histograms

---

## 📸 Screenshots

### 🧠 Real-Time Detection UI  
![Radar](docs/radar.png)

### 🧪 Educational Version  
![Lab UI](docs/lab.png)

---

## 🛠 Tech Stack

- Streamlit frontend (English + Korean)
- Python + NumPy + Pandas backend
- Plotly for visual analytics
- BlockCypher REST API
- GitHub Actions / Deployment Ready

---

## 📄 Resume

**You Jin Kim (김유진)**  
M.S. in Information Security, Korea University  
✉️ youjin.kim@korea.ac.kr  
📄 [Resume PDF](https://github.com/u0jin/btc-anomaly-lens/blob/main/docs/%F0%9F%93%84%20You%20Jin%20Kim%20%E2%80%94%20Resume.pdf)  
🔗 [GitHub Profile](https://github.com/u0jin)

---

## 📜 License

MIT License — fork or adapt freely, with credit.

---

## 🧠 Philosophy

> “This is not just a tool — it’s a reflection of research logic, product thinking, and cybersecurity insight.”

Every scoring function, blacklist detection rule, and visualization was custom-designed and explained.  
The project demonstrates not only academic skills but also real-world technical ownership.

---

## 🧭 Bonus

| Area | Use |
|------|-----|
| 🎓 Academic | Blockchain forensic research, reproducible scoring logic |
| 💼 Portfolio | Interview-ready, GitHub-linked, self-developed product |
| 🧪 Education | Free version for students with no paid API key |

