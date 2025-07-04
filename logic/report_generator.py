from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepInFrame
from reportlab.lib import colors
from io import BytesIO
import matplotlib.pyplot as plt
import tempfile
import os
import numpy as np
from datetime import datetime
from logic.graph_utils import generate_similarity_bar_chart

def generate_pdf_report(address, total_score, scores_dict, scenario_matches, similarity_threshold):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='RiskGradeRed', textColor=colors.red, fontSize=12))
    styles.add(ParagraphStyle(name='RiskGradeOrange', textColor=colors.orange, fontSize=12))
    styles.add(ParagraphStyle(name='RiskGradeGreen', textColor=colors.green, fontSize=12))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=13, textColor=colors.HexColor('#003366'),
                              spaceAfter=6, leading=14, fontName='Helvetica-Bold'))

    elements = []

    # Header
    elements.append(Paragraph("<font size=20><b>BTC Anomaly Report</b></font>", styles['Title']))
    elements.append(Spacer(1, 16))
    elements.append(Paragraph(f"<b>Analyzed Address:</b> {address}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Risk Score:</b> {total_score}/100", styles['Normal']))
    elements.append(Paragraph(f"<b>Report Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Normal']))

    # Risk Grade
    if total_score >= 75:
        grade, grade_style = "High Risk", styles['RiskGradeRed']
        summary_text = "This address shows transaction patterns indicating HIGH RISK. Immediate investigation recommended."
    elif total_score >= 40:
        grade, grade_style = "Moderate Risk", styles['RiskGradeOrange']
        summary_text = "This address shows transaction patterns suggesting MODERATE RISK. Anomalies may indicate structuring, address reuse, or obfuscation techniques."
    else:
        grade, grade_style = "Low Risk", styles['RiskGradeGreen']
        summary_text = "This address shows transaction patterns consistent with LOW RISK behavior. No strong anomalies detected."

    elements.append(Paragraph(f"<b>Risk Grade:</b> {grade}", grade_style))
    elements.append(Spacer(1, 16))

    summary_frame = KeepInFrame(450, 80, content=[
        Paragraph(f"<b>Summary:</b> {summary_text}", styles['Normal'])
    ], hAlign='LEFT')
    elements.append(Table([[summary_frame]], colWidths=[450], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff4ce')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(Spacer(1, 16))

    # Similarity chart
    similarity_chart_path = None
    if scenario_matches:
        similarity_chart_path = generate_similarity_bar_chart(scenario_matches[:3])
        if similarity_chart_path and os.path.exists(similarity_chart_path):
            elements.append(Paragraph("Scenario Similarity Visualization:", styles['SectionHeader']))
            elements.append(Image(similarity_chart_path, width=450, height=260))
            elements.append(Spacer(1, 10))

    # Scenario Matches
    for i, match in enumerate(scenario_matches[:3], 1):
        elements.append(Paragraph(f"<b>Scenario #{i}: {match['actor']}</b>", styles['SectionHeader']))
        elements.append(Paragraph(f"<b>Similarity:</b> {match['similarity']}%", styles['Normal']))
        elements.append(Paragraph(match['description'], styles['Normal']))
        elements.append(Spacer(1, 6))

        if "match_log" in match:
            logs = match["match_log"]
            log_table = [["Metric", "Score Contribution"]]
            for k, v in logs.items():
                if k != "similarity":
                    label = {
                        "tx_count": "Tx Count Match",
                        "avg_interval": "Interval Match",
                        "reused_ratio": "Reused Address Match",
                        "fee_flag": "High Fee Match"
                    }.get(k, k)
                    log_table.append([label, f"{round(v * 100, 1)} / 100"])
            table = Table(log_table, colWidths=[240, 120], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
            ]))
            elements.append(table)
        elements.append(Spacer(1, 12))

    # Risk Score Table
    score_table = [["Metric", "Score"]] + [[k, str(v)] for k, v in scores_dict.items()]
    table = Table(score_table, hAlign='LEFT', colWidths=[260, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#a0a0a0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Radar Chart
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    radar_color = 'red' if total_score >= 75 else 'orange' if total_score >= 40 else 'green'
    ax.plot(angles, values, color=radar_color, linewidth=2)
    ax.fill(angles, values, color=radar_color, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    fig.patch.set_facecolor('white')

    radar_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    plt.savefig(radar_path, bbox_inches='tight')
    plt.close(fig)

    elements.append(Paragraph("Anomaly Risk Radar Chart", styles['SectionHeader']))
    elements.append(Image(radar_path, width=360, height=360))
    elements.append(Spacer(1, 24))

    # Interpretation & Notes
    sections = [
        ("Detection Criteria:", [
            "Short Interval: Detects repetitive transfers in short bursts.",
            "Amount Outliers: Identifies transactions far exceeding the statistical average.",
            "Repeated Recipients: Flags frequent reuse of the same recipient address.",
            "Time Gaps: Highlights silent periods and activity bursts.",
            "Blacklist Hits: Detects if the address appears in OFAC or other sanctions lists."
        ]),
        ("Score Interpretation:", [
            "Scores near 25 indicate stronger anomalies and deserve closer inspection.",
            "A high score in Blacklist implies direct association with known malicious actors.",
            "Timing-based scores reflect bursty activity or latency obfuscation techniques.",
            "Combined, they form a risk fingerprint used in forensic threat intelligence workflows."
        ]),
        ("Recommended Action:", [
            "Investigate clustering relationships and source transactions.",
            "Cross-reference with external threat feeds (e.g., TRM, Chainalysis).",
            "Monitor for future darknet or exchange appearances."
        ]),
        ("Analyst Note:", [
            "This report is based on custom-defined detection rules integrating academic and applied blockchain research.",
            "Radar score profiles assist in visual triage for SOC and forensic workflows."
        ])
    ]
    for title, bullets in sections:
        elements.append(Paragraph(title, styles['SectionHeader']))
        for line in bullets:
            elements.append(Paragraph(f"• {line}", styles['Normal']))
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("Generated by <b>BTC Anomaly Lens</b>. Forensic toolkit for real-time Bitcoin threat simulation.", styles['Italic']))

    doc.build(elements)

    # Clean up temp files
    if similarity_chart_path and os.path.exists(similarity_chart_path):
        os.unlink(similarity_chart_path)
    if radar_path and os.path.exists(radar_path):
        os.unlink(radar_path)

    pdf = buffer.getvalue()
    buffer.close()
    return BytesIO(pdf)
