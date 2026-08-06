#!/usr/bin/env python3
import json
import urllib.request

# Fetch current page content
API_KEY = "ntn_J4023294701b2YpwPwXEyhmeqZ6ggitQvcHKMoiuvth5G2"
PAGE_ID = "3490efce9aed80d28deaeb269991f3e6"

url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

count = 0
for block in data["results"]:
    if block.get("type") == "paragraph" and "🎯" in str(block):
        count = 1
        print(f"Found Roadmap section! Current total blocks: {count}")
        break

if not count:
    print("Need to add roadmap section")
