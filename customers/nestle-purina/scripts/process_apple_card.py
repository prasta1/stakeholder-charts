import csv
import io
from collections import defaultdict
from datetime import datetime
import json
import sys
import os

def parse_apple_csv(file_path):
    """Parses Apple Card CSV and extracts ONLY 'Purchase' transactions."""
    purchases = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
                
            parts = line.split('|', 1)
            if len(parts) < 2:
                continue
                
            csv_content = parts[1]
            reader = csv.reader(io.StringIO(csv_content))
            try:
                row = next(reader)
                if len(row) < 7:
                    continue
                if row[0] == "Transaction Date":
                    continue
                    
                type_ = row[5].strip()
                if type_ == 'Purchase':
                    merchant = row[3].strip()
                    category = row[4].strip()
                    date_str = row[0].strip()
                    amount = float(row[6].strip().replace('"', ''))
                    dt = datetime.strptime(date_str, '%m/%d/%Y')
                    purchases.append({
                        'date': dt,
                        'merchant': merchant,
                        'category': category,
                        'amount': amount,
                        'month': dt.strftime('%Y-%m')
                    })
            except Exception:
                continue
    return purchases

def generate_spending_report(purchases, output_path):
    total_spend = sum(p['amount'] for p in purchases)
    
    category_totals = defaultdict(float)
    merchant_totals = defaultdict(float)
    monthly_totals = defaultdict(float)
    
    for p in purchases:
        category_totals[p['category']] += p['amount']
        merchant_totals[p['merchant']] += p['amount']
        monthly_totals[p['month']] += p['amount']

    summary = {
        "total_spending": round(total_spend, 2),
        "monthly_spend": dict(sorted(monthly_totals.items())),
        "category_spend": dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True)),
        "top_merchants": sorted([[m, round(v, 2)] for m, v in merchant_totals.items()], 
                                key=lambda x: x[1], reverse=True)[:10]
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    return summary

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        sys.exit(1)
        
    p_data = parse_apple_csv(input_file)
    report = generate_spending_report(p_data, output_file)
    print(json.dumps(report, indent=2))
