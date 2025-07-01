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

def generate_pdf_report(address, total_score, scores_dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='RiskGradeRed', textColor=colors.red, fontSize=12))
    styles.add(ParagraphStyle(name='RiskGradeOrange', textColor=colors.orange, fontSize=12))
    styles.add(ParagraphStyle(name='RiskGradeGreen', textColor=colors.green, fontSize=12))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=13, textColor=colors.HexColor('#003366'), spaceAfter=6, leading=14, fontName='Helvetica-Bold'))

    elements = []

    elements.append(Paragraph("<font size=20><b>BTC Anomaly Report</b></font>", styles['Title']))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph(f"<b>Analyzed Address:</b> {address}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Risk Score:</b> {total_score}/100", styles['Normal']))
    elements.append(Paragraph(f"<b>Report Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Normal']))

    if total_score >= 75:
        grade = "High Risk"
        grade_style = styles['RiskGradeRed']
        summary_text = "This address shows transaction patterns indicating HIGH RISK. Immediate investigation recommended."
    elif total_score >= 40:
        grade = "Moderate Risk"
        grade_style = styles['RiskGradeOrange']
        summary_text = "This address shows transaction patterns suggesting MODERATE RISK. Anomalies may indicate structuring, address reuse, or obfuscation techniques."
    else:
        grade = "Low Risk"
        grade_style = styles['RiskGradeGreen']
        summary_text = "This address shows transaction patterns consistent with LOW RISK behavior. No strong anomalies detected."

    elements.append(Paragraph(f"<b>Risk Grade:</b> {grade}", grade_style))
    elements.append(Spacer(1, 16))

    summary_paragraph = Paragraph(f"<b>Summary:</b> {summary_text}", styles['Normal'])
    summary_frame = KeepInFrame(450, 60, content=[summary_paragraph], hAlign='LEFT')
    summary_table = Table([[summary_frame]], colWidths=[450])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff4ce')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 16))

    data = [["Metric", "Score"]] + [[k, str(v)] for k, v in scores_dict.items()]
    table = Table(data, hAlign='LEFT', colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d0d0d0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Detection Criteria:", styles['SectionHeader']))
    elements.append(Paragraph(
        "• Short Interval: Detects repetitive transfers in short bursts.<br/>"
        "• Amount Outliers: Identifies transactions far exceeding the statistical average.<br/>"
        "• Repeated Recipients: Flags frequent reuse of the same recipient address.<br/>"
        "• Time Gaps: Highlights silent periods and activity bursts.<br/>"
        "• Blacklist Hits: Detects if the address appears in OFAC, TRM Labs, or other sanctions lists.", styles['BodyText']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Score Interpretation:", styles['SectionHeader']))
    elements.append(Paragraph(
        "• Scores near 25 indicate stronger anomalies and deserve closer inspection.<br/>"
        "• A high score in Blacklist implies direct association with known malicious actors.<br/>"
        "• Timing-based scores reflect bursty activity or latency obfuscation techniques.<br/>"
        "• Combined, they form a risk fingerprint used in forensic threat intelligence workflows.", styles['BodyText']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Example Scenarios:", styles['SectionHeader']))
    elements.append(Paragraph(
        "• A high Amount Outlier score may suggest obfuscation via large-value splitting.<br/>"
        "• Frequent Recipient Reuse can indicate mixer payouts or laundering routines.<br/>"
        "• Gaps and bursts may reflect automated bots or compromised wallets.", styles['BodyText']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Recommended Action:", styles['SectionHeader']))
    elements.append(Paragraph(
        "• Investigate clustering relationships and source transactions.<br/>"
        "• Cross-reference with external threat feeds (e.g., TRM, Chainalysis).<br/>"
        "• Monitor for future darknet or exchange appearances.", styles['BodyText']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Analyst Note:", styles['SectionHeader']))
    elements.append(Paragraph(
        "• This report is based on custom-defined detection rules integrating academic and applied blockchain research.<br/>"
        "• Radar score profiles assist in visual triage for SOC and forensic workflows.", styles['BodyText']))
    elements.append(Spacer(1, 20))

    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    values += values[:1]
    N = len(categories)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

    radar_color = 'red' if total_score >= 75 else 'orange' if total_score >= 40 else 'green'
    ax.plot(angles, values, linewidth=2, linestyle='solid', color=radar_color)
    ax.fill(angles, values, radar_color, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.grid(True)
    fig.patch.set_facecolor('white')

    tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmpfile.name, bbox_inches='tight')
    plt.close(fig)

    elements.append(Image(tmpfile.name, width=360, height=360))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Generated by <b>BTC Anomaly Lens</b>. Forensic toolkit for real-time Bitcoin threat simulation.", styles['Italic']))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    os.unlink(tmpfile.name)
    return BytesIO(pdf)
