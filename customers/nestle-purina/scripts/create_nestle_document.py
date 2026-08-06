#!/usr/bin/env python3
import json
import urllib.request
import sys

API_KEY = "ntn_J4023294701b2YpwPwXEyhmeqZ6ggitQvcHKMoiuvth5G2"
PAGE_ID = "3490efce9aed80d28deaeb269991f3e6"

# Main content blocks
main_blocks = [
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Executive Summary"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Edge AI applications for pet nutrition and care products across manufacturing, retail, consumer devices, and veterinary care."}}]}},
    {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🏭 Manufacturing & Quality Control"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• Computer vision for defect detection (packaging, ingredients)"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• Predictive maintenance on production equipment"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• Real-time process monitoring for food safety"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• Inventory optimization using RFID + edge computing"}}]}}
]

def append_blocks(parent_block_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{parent_block_id}/children"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json"
    }
    
    # Append multiple blocks
    for block in blocks:
        payload = json.dumps(block)
        req = urllib.request.Request(url, data=payload.encode(), headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                print(json.dumps(response.read().decode(), indent=2))
        except Exception as e:
            print(f"Error: {e}")

def create_blocks(blocks):
    """Create blocks from top-level endpoint"""
    url = "https://api.notion.com/v1/blocks"  # This won't work, use PATCH instead
    return blocks

if __name__ == "__main__":
    print("Creating Edge AI document content...")
    
    # Test connection first
    test_url = "https://api.notion.com/v1/blocks"
    test_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(test_url, data=b"{}", headers=test_headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Connection successful: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}")
    except Exception as e:
        print(f"Error connecting: {e}")
        