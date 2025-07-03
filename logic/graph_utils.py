# logic/graph_utils.py

import matplotlib.pyplot as plt
import tempfile
import os

def generate_similarity_bar_chart(scenario_matches):
    labels = [match["actor"] for match in scenario_matches]
    values = [match["similarity"] for match in scenario_matches]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(labels, values, color='skyblue')
    ax.set_title("Scenario Similarity Scores")
    ax.set_ylabel("Similarity (%)")
    ax.set_ylim(0, 100)

    for i, v in enumerate(values):
        ax.text(i, v + 2, f"{v}%", ha='center', fontsize=9)

    fig.tight_layout()
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmpfile.name, bbox_inches='tight')
    plt.close(fig)
    return tmpfile.name
