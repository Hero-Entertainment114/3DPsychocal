import json
from core.paths import ROOT

class Content:
    def __init__(self, root=ROOT):
        self.root = root
        for name in ('puzzles', 'dialogues', 'characters', 'maps', 'endings', 'quests', 'observations', 'chapters'):
            with (root / 'data' / f'{name}.json').open(encoding='utf-8') as f:
                rows = json.load(f)
            setattr(self, name, {row['id']: row for row in rows})
    @property
    def playable(self):
        return [p for p in self.puzzles.values() if p['status'] == 'playable']
