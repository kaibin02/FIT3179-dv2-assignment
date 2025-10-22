import csv
import json
from statistics import mean
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
inc_path = ROOT / 'income.csv'
cpi_path = ROOT / 'cpi.csv'

years = ['2016','2019','2022']

# Read income medians by state and year
inc = {}
with open(inc_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        date = r['date'].strip()
        # parse year from m/d/YYYY or YYYY-MM-DD
        if '/' in date:
            parts = date.split('/')
            year = parts[-1]
        else:
            year = date.split('-')[0]
        med = r['income_median'].strip()
        if med == '':
            continue
        try:
            medv = float(med)
        except:
            continue
        state = r['state'].strip()
        inc.setdefault(year, []).append(medv)

# compute national median as mean of state medians (unweighted)
national_income = {}
for y in years:
    vals = inc.get(y, [])
    if vals:
        national_income[y] = mean(vals)
    else:
        national_income[y] = None

# Read CPI overall
cpi = {}
with open(cpi_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        date = r['date'].strip()
        year = date.split('-')[0]
        division = r['division'].strip()
        if division != 'overall':
            continue
        try:
            idx = float(r['index'])
        except:
            continue
        cpi[year] = idx

# Build dataset
base_income = national_income.get('2016')
base_cpi = cpi.get('2016')

rows = []
for y in years:
    inc_val = national_income.get(y)
    cpi_val = cpi.get(y)
    if inc_val is None or cpi_val is None:
        continue
    inc_index = (inc_val / base_income) * 100 if base_income else None
    cpi_index = (cpi_val / base_cpi) * 100 if base_cpi else None
    rows.append({
        'year': int(y),
        'income_median': round(inc_val, 2),
        'income_index': round(inc_index, 2),
        'cpi_index': round(cpi_index, 2),
        'cpi_raw': round(cpi_val, 4)
    })

out_path = ROOT / 'line_indexed_income_cpi_data.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(rows, f, indent=2)

print('Wrote', out_path)
print(json.dumps(rows, indent=2))
