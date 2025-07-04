import json
import os

def load_scenarios(path="data/100_scenario_db_from_blacklist.json"):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load scenario DB: {e}")
        return []

def match_scenarios(tx_stats, scenarios, min_similarity=50):
    matched = []
    if not tx_stats or not isinstance(tx_stats, dict):
        return []

    for scenario in scenarios:
        pattern = scenario.get("pattern", {})
        score = 0
        checks = 0

        if isinstance(pattern, dict):
            if "tx_count_min" in pattern:
                checks += 1
                if tx_stats.get("tx_count", 0) >= pattern["tx_count_min"]:
                    score += 1
            if "avg_interval_max" in pattern:
                checks += 1
                if tx_stats.get("avg_interval", 999999) <= pattern["avg_interval_max"]:
                    score += 1
            if "reused_address_ratio_min" in pattern:
                checks += 1
                if tx_stats.get("reused_address_ratio", 0.0) >= pattern["reused_address_ratio_min"]:
                    score += 1
            if "high_fee_flag" in pattern:
                checks += 1
                if tx_stats.get("high_fee_flag") == pattern["high_fee_flag"]:
                    score += 1

        if checks > 0:
            similarity = int((score / checks) * 100)
            if similarity >= min_similarity:
                matched.append({
                    "id": scenario.get("id", "N/A"),
                    "actor": scenario.get("actor", "Unknown"),
                    "description": scenario.get("description", ""),
                    "similarity": similarity,
                    "pattern": pattern
                })

    return sorted(matched, key=lambda x: x["similarity"], reverse=True)
