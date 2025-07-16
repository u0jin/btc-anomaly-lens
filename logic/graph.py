import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from io import BytesIO
import base64
from collections import deque

def generate_transaction_network(tx_list, max_hops=3, top_n=15, source_address=None):
    """
    트랜잭션 네트워크를 생성하고 시각화합니다.
    Args:
        tx_list: 트랜잭션 리스트
        max_hops: 최대 hop 수 (1-10 범위)
        top_n: 표시할 최대 노드 수
        source_address: 소스 주소 (None이면 tx_list[0]['from'] 사용)
    """
    if not tx_list:
        return None

    # 사용자가 지정한 주소가 있으면 그걸 source로, 없으면 tx_list[0]['from']
    if source_address is None:
        source_address = tx_list[0].get('from', 'source')

    print(f"🔍 Source address: {source_address}")
    print(f"🔍 Max hops: {max_hops}")

    # 트랜잭션 인덱싱: from_addr -> [tx, ...]
    from_index = {}
    for tx in tx_list:
        from_addr = tx.get('from')
        if from_addr:
            from_index.setdefault(from_addr, []).append(tx)

    print(f"🔍 Available from addresses: {len(from_index)}")
    print(f"🔍 Source in from_index: {source_address in from_index}")

    # source_address가 None이거나 from_index에 없으면, 해당 주소로 들어오는 트랜잭션을 찾아서 시작점으로 사용
    if source_address is None or source_address not in from_index:
        if source_address is None:
            print(f"⚠️ Source address is None, using first transaction's from")
            source_address = tx_list[0].get('from', 'source')
        else:
            print(f"⚠️ Source address '{source_address}' not found in from_index")
            # 해당 주소로 들어오는 트랜잭션 찾기
            incoming_txs = [tx for tx in tx_list if tx.get('to') == source_address]
            if incoming_txs:
                # 첫 번째 incoming 트랜잭션의 from을 새로운 source로 사용
                new_source = incoming_txs[0].get('from')
                print(f"🔍 Using new source: {new_source} (from incoming transaction)")
                if new_source is not None:
                    source_address = new_source
                else:
                    print(f"⚠️ New source is None, using first transaction's from")
                    source_address = tx_list[0].get('from', 'source')
            else:
                print(f"⚠️ No incoming transactions found for '{source_address}', using first transaction's from")
                source_address = tx_list[0].get('from', 'source')
    
    # 최종적으로 source_address가 None이면 안전한 기본값 사용
    if source_address is None:
        print(f"⚠️ Final source_address is None, using 'source' as default")
        source_address = 'source'

    G = nx.DiGraph()
    G.add_node(source_address)

    # BFS로 hop만큼만 따라가며 그래프 확장
    queue = deque([(source_address, 0)])
    visited = set([source_address])
    edge_set = set()
    
    nodes_at_hop = {0: [source_address]}  # hop별 노드 추적

    while queue:
        current, depth = queue.popleft()
        print(f"🔍 Processing {current} at depth {depth}")
        
        if depth >= max_hops:
            continue
            
        # 현재 노드에서 출발하는 트랜잭션들 찾기
        outgoing_txs = from_index.get(current, [])
        print(f"🔍 Found {len(outgoing_txs)} outgoing transactions from {current}")
        
        # hop 수에 따라 더 많은 연결을 보여주기
        max_connections_per_hop = min(max_hops * 5, 20)  # hop 수에 비례하여 연결 수 증가
        if len(outgoing_txs) > max_connections_per_hop:
            # 거래량 기준으로 정렬하여 중요한 트랜잭션 우선
            outgoing_txs = sorted(outgoing_txs, key=lambda x: x.get('amount', 0), reverse=True)[:max_connections_per_hop]
            print(f"🔍 Selected top {max_connections_per_hop} transactions for hop {depth + 1}")
        
        for tx in outgoing_txs:
            to_addr = tx.get('to')
            if to_addr:
                G.add_node(to_addr)
                # 중복 엣지 방지
                if (current, to_addr) not in edge_set:
                    G.add_edge(current, to_addr, weight=tx.get('amount', 0),
                               tx_hash=tx.get('tx_hash', ''),
                               timestamp=tx.get('timestamp', ''))
                    edge_set.add((current, to_addr))
                    
                if to_addr not in visited:
                    visited.add(to_addr)
                    queue.append((to_addr, depth + 1))
                    
                    # hop별 노드 추적
                    if depth + 1 not in nodes_at_hop:
                        nodes_at_hop[depth + 1] = []
                    nodes_at_hop[depth + 1].append(to_addr)
        
        # 더 많은 hop 확장을 위해 추가 연결 찾기
        if depth == 0 and len(outgoing_txs) > 0:
            # 첫 번째 hop에서 더 많은 연결을 찾기 위해 다른 주소들도 추가
            print(f"🔍 Expanding network with additional connections...")
            additional_connections = 0
            
            # 전체 트랜잭션에서 다른 주소들 찾기
            for tx in tx_list:
                if additional_connections >= max_hops * 3:  # 최대 추가 연결 수 제한
                    break
                    
                from_addr = tx.get('from')
                to_addr = tx.get('to')
                
                if from_addr and to_addr and from_addr != current and to_addr != current:
                    # 새로운 연결 추가
                    if from_addr not in visited:
                        G.add_node(from_addr)
                        visited.add(from_addr)
                        additional_connections += 1
                        
                        if 1 not in nodes_at_hop:
                            nodes_at_hop[1] = []
                        nodes_at_hop[1].append(from_addr)
                    
                    if to_addr not in visited:
                        G.add_node(to_addr)
                        visited.add(to_addr)
                        additional_connections += 1
                        
                        if 1 not in nodes_at_hop:
                            nodes_at_hop[1] = []
                        nodes_at_hop[1].append(to_addr)
                    
                    # 엣지 추가
                    if (from_addr, to_addr) not in edge_set:
                        G.add_edge(from_addr, to_addr, weight=tx.get('amount', 0),
                                   tx_hash=tx.get('tx_hash', ''),
                                   timestamp=tx.get('timestamp', ''))
                        edge_set.add((from_addr, to_addr))
            
            print(f"🔍 Added {additional_connections} additional connections")

    print(f"🔍 Final network: {len(G.nodes())} nodes, {len(G.edges())} edges")
    for hop, nodes in nodes_at_hop.items():
        print(f"🔍 Hop {hop}: {len(nodes)} nodes")

    # hop 수에 따라 동적으로 노드 수 조절
    dynamic_top_n = min(top_n, len(G.nodes()))
    if max_hops > 3:
        dynamic_top_n = min(dynamic_top_n + max_hops * 2, len(G.nodes()))
    
    print(f"🔍 Selected {dynamic_top_n} nodes for visualization (dynamic top_n: {dynamic_top_n})")

    # 노드 중요도 계산 (연결 수, 거래량 기준)
    node_importance = {}
    for node in G.nodes():
        if node == source_address:
            node_importance[node] = float('inf')  # 소스 노드는 최우선
        else:
            in_degree = len(list(G.predecessors(node)))
            out_degree = len(list(G.successors(node)))
            total_volume = sum(G[u][node]['weight'] for u in G.predecessors(node)) if list(G.predecessors(node)) else 0
            node_importance[node] = (in_degree + out_degree) * 0.5 + total_volume * 0.01

    # 중요도 순으로 노드 선택
    sorted_nodes = sorted(node_importance.items(), key=lambda x: x[1], reverse=True)
    selected_nodes = [node for node, _ in sorted_nodes[:dynamic_top_n]]

    # 서브그래프 생성
    subgraph = G.subgraph(selected_nodes).copy()
    
    print(f"🔍 Subgraph: {len(subgraph.nodes())} nodes, {len(subgraph.edges())} edges")

    # 시각화
    plt.figure(figsize=(14, 10))
    
    # 노드가 1개인 경우 특별 처리
    if len(subgraph.nodes()) == 1:
        pos = {list(subgraph.nodes())[0]: (0.5, 0.5)}
    elif len(subgraph.nodes()) == 2:
        # 2개 노드인 경우 좌우로 배치
        nodes_list = list(subgraph.nodes())
        pos = {nodes_list[0]: (0.2, 0.5), nodes_list[1]: (0.8, 0.5)}
    else:
        pos = nx.spring_layout(subgraph, k=3.0, iterations=150, seed=42)

    node_colors = []
    node_sizes = []
    node_labels = {}
    
    for node in subgraph.nodes():
        # 노드 라벨을 짧게 표시 (첫 8자만)
        short_label = node[:8] + "..." if len(node) > 8 else node
        node_labels[node] = short_label
        
        if node == source_address:
            node_colors.append('#FF6B6B')  # 빨간색 (소스)
            node_sizes.append(2000)
        else:
            pred_count = len(list(subgraph.predecessors(node)))
            succ_count = len(list(subgraph.successors(node)))
            if pred_count > succ_count:
                node_colors.append('#4ECDC4')  # 청록색 (수신)
                node_sizes.append(1200)
            else:
                node_colors.append('#45B7D1')  # 파란색 (중간)
                node_sizes.append(1000)

    edge_colors = []
    edge_widths = []
    
    # 엣지가 있는 경우에만 max_weight 계산
    if subgraph.edges():
        try:
            max_weight = max([subgraph[u][v]['weight'] for u, v in subgraph.edges()])
            for u, v in subgraph.edges():
                weight = subgraph[u][v]['weight']
                edge_colors.append('#FF6B6B')
                edge_widths.append(3 + (weight / max_weight) * 8)
        except:
            # 에러 발생 시 기본값 사용
            for u, v in subgraph.edges():
                edge_colors.append('#FF6B6B')
                edge_widths.append(3)
    else:
        # 엣지가 없는 경우
        edge_colors = []
        edge_widths = []

    # 그래프 그리기
    nx.draw(subgraph, pos,
            node_color=node_colors,
            node_size=node_sizes,
            edge_color=edge_colors,
            width=edge_widths,
            labels=node_labels,
            font_size=12,
            font_weight='bold',
            arrows=True,
            arrowsize=25,
            arrowstyle='->',
            edgecolors='black',
            linewidths=2)

    # 범례 추가
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF6B6B',
               markersize=15, label='Source Address'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4ECDC4',
               markersize=12, label='Recipient Addresses'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#45B7D1',
               markersize=10, label='Intermediate Addresses')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
    plt.title(f"Transaction Network Visualization\n(Max Hops: {max_hops}, Total Nodes: {len(G.nodes())}, Displayed: {len(subgraph.nodes())}, Edges: {len(subgraph.edges())})", 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    encoded_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return encoded_img

def get_network_stats(tx_list, max_hops=3):
    """
    네트워크 통계를 계산합니다.
    """
    if not tx_list:
        return None
    
    # 트랜잭션 인덱싱
    from_index = {}
    for tx in tx_list:
        from_addr = tx.get('from')
        if from_addr:
            from_index.setdefault(from_addr, []).append(tx)
    
    # 실제 네트워크 노드 수 계산
    all_nodes = set()
    for tx in tx_list:
        if tx.get('from'):
            all_nodes.add(tx.get('from'))
        if tx.get('to'):
            all_nodes.add(tx.get('to'))
    
    actual_node_count = len(all_nodes)
    
    return {
        'total_nodes': actual_node_count,
        'total_edges': len(tx_list),
        'unique_recipients': len(set(tx.get('to') for tx in tx_list if tx.get('to'))),
        'total_volume': sum(tx.get('amount', 0) for tx in tx_list),
        'max_available_nodes': actual_node_count
    }

def get_max_available_nodes(tx_list, max_hops=3):
    """
    현재 설정에서 사용 가능한 최대 노드 수를 계산합니다.
    """
    if not tx_list:
        return 15  # 기본값
    
    # 트랜잭션 인덱싱
    from_index = {}
    for tx in tx_list:
        from_addr = tx.get('from')
        if from_addr:
            from_index.setdefault(from_addr, []).append(tx)
    
    # 실제 네트워크 노드 수 계산
    all_nodes = set()
    for tx in tx_list:
        if tx.get('from'):
            all_nodes.add(tx.get('from'))
        if tx.get('to'):
            all_nodes.add(tx.get('to'))
    
    actual_node_count = len(all_nodes)
    
    # hop 수에 따라 동적으로 조정
    max_available = min(actual_node_count, 50)  # 최대 50개로 제한
    
    return max_available
