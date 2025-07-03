import pandas as pd
import json

# 1. 블랙리스트 주소 불러오기
with open("data/blacklist.txt", "r") as f:
    blacklist = [line.strip() for line in f if line.strip()]

import pandas as pd

df = pd.read_csv("data/hacker_data.csv")

# group별 100개씩 뽑기
top_10_each = df.groupby("report_type").head(10)
top_10_each = top_10_each.dropna(subset=["hacker_address"])
top_10_each.to_csv("10_selected_addresses.csv", index=False)
