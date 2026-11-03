import json
from pathlib import Path
p=Path('senate/2026/kentucky/data/turnout/source/receipts')
rs=[json.loads(f.read_text()) for f in p.glob('*.json')]
print('receipt count',len(rs))
print([(r['role'],r['status']) for r in rs if 'recap' not in r['role'].lower()][:50])
