import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import Counter

def generate_transaction_network(tx_list, top_n=15):
    G = nx.DiGraph()
    counts = Counter(tx['to'] for tx in tx_list if tx.get('to'))

    for tx in tx_list:
        to_addr = tx.get("to")
        if not to_addr:
            continue
        G.add_node(to_addr)
        G.add_edge("source", to_addr, weight=tx["amount"])

    # 가장 많이 등장한 수신 주소 중심으로만 출력
    most_common = set([addr for addr, _ in counts.most_common(top_n)])
    subgraph = G.subgraph(["source"] + list(most_common)).copy()

    pos = nx.spring_layout(subgraph, k=0.5, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=8)
    plt.title("Transaction Flow Network (Top Recipients)")
    plt.tight_layout()

    # base64로 인코딩된 이미지 반환
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return encoded_img
