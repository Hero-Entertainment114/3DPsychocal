from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
puzzles=json.loads((ROOT/'data/puzzles.json').read_text(encoding='utf8'))
lines=['flowchart LR']
for p in puzzles:
    lines.append(f'  {p["id"]}["{p["id"]} · {p["title"]}"]')
    for dep in p['requires']:lines.append(f'  {dep} --> {p["id"]}')
lines += ['  classDef playable fill:#728777,color:#111b24','  class '+','.join(p['id'] for p in puzzles if p['status']=='playable')+' playable']
(ROOT/'docs/puzzle_graph.mmd').write_text('\n'.join(lines)+'\n',encoding='utf8')
with (ROOT/'docs/puzzle_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['id','title','chapter','category','status','room','dependencies','answer'])
    for p in puzzles:writer.writerow([p['id'],p['title'],p['chapter'],p['category'],p['status'],p['room'],','.join(p['requires']),'/'.join(p['answers'])])
print('Exported puzzle CSV and Mermaid graph')
