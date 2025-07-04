import json
import os
import math

def load_scenarios(path="data/100_scenario_db_from_blacklist.json"):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load scenario DB: {e}")
        return []

def sigmoid_score(x, center, scale=1.0):
    """거리 기반 sigmoid 점수 함수. center에 가까울수록 점수 1, 멀수록 감쇠."""
    try:
        return 1 / (1 + math.exp(scale * (x - center)))
    except:
        return 0

def calculate_similarity(tx_stats, pattern):
    score = 0.0
    total_weight = 0.0
    debug_log = {}

    # 1. tx_count_min (높을수록 유사)
    if "tx_count_min" in pattern:
        val = tx_stats.get("tx_count", 0)
        target = pattern["tx_count_min"]
        weight = 0.3
        diff = abs(val - target)
        comp_score = sigmoid_score(diff, 0, scale=0.2)
        score += comp_score * weight
        total_weight += weight
        debug_log["tx_count"] = round(comp_score * weight, 3)

    # 2. avg_interval_max (낮을수록 유사)
    if "avg_interval_max" in pattern:
        val = tx_stats.get("avg_interval", 999999)
        target = pattern["avg_interval_max"]
        weight = 0.3
        diff = val - target
        comp_score = sigmoid_score(diff, 0, scale=0.0015)
        score += comp_score * weight
        total_weight += weight
        debug_log["avg_interval"] = round(comp_score * weight, 3)

    # 3. reused_address_ratio_min (높을수록 유사)
    if "reused_address_ratio_min" in pattern:
        val = tx_stats.get("reused_address_ratio", 0)
        target = pattern["reused_address_ratio_min"]
        weight = 0.2
        diff = abs(val - target)
        comp_score = sigmoid_score(diff, 0, scale=5)
        score += comp_score * weight
        total_weight += weight
        debug_log["reused_ratio"] = round(comp_score * weight, 3)

    # 4. high_fee_flag (정확히 일치할 때만 점수)
    if "high_fee_flag" in pattern:
        val = tx_stats.get("high_fee_flag", False)
        target = pattern["high_fee_flag"]
        weight = 0.2
        if val == target:
            score += weight
            debug_log["fee_flag"] = round(weight, 3)
        else:
            debug_log["fee_flag"] = 0.0
        total_weight += weight

    similarity = int((score / total_weight) * 100) if total_weight > 0 else 0
    debug_log["similarity"] = similarity
    return similarity, debug_log

def match_scenarios(tx_stats, scenarios, min_similarity=50):
    matched = []
    if not tx_stats or not isinstance(tx_stats, dict):
        return []

    for scenario in scenarios:
        pattern = scenario.get("pattern", {})
        similarity, log = calculate_similarity(tx_stats, pattern)

        if similarity >= min_similarity:
            matched.append({
                "id": scenario.get("id", "N/A"),
                "actor": scenario.get("actor", "Unknown"),
                "description": scenario.get("description", ""),
                "similarity": similarity,
                "pattern": pattern,
                "match_log": log
            })

    return sorted(matched, key=lambda x: x["similarity"], reverse=True)
