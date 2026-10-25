"""Pure progression rules shared by the UI and route tests."""
from copy import deepcopy

class Progression:
    def __init__(self, content, state):
        self.content, self.state = content, state
    def available(self, pid):
        p = self.content.puzzles[pid]
        return p['status'] == 'playable' and all(d in self.state.solved for d in p['requires'])
    def solve(self, pid, answer, assisted=False):
        p, s = self.content.puzzles[pid], self.state
        if pid in s.solved:
            return True
        if not self.available(pid):
            return False
        normalized = str(answer).strip().casefold()
        if normalized not in [str(a).casefold() for a in p['answers']] and not assisted:
            s.attempts[pid] = s.attempts.get(pid, 0) + 1
            s.fear = min(70, s.fear + 3)
            return False
        if assisted and s.attempts.get(pid, 0) < 3:
            return False
        s.solved.append(pid)
        s.flags[f'solved_{pid}'] = True
        s.choices[pid] = 'assisted' if assisted else normalized
        s.evidence.append(p['reward'])
        s.journal.append(p['resolution'])
        s.clarity += 1
        s.fear = max(0, s.fear - 5)
        if p.get('item') and p['item'] not in s.inventory:
            s.inventory.append(p['item'])
        if pid == 'P004':
            s.phase = 'evening'
        if pid == 'P008':
            s.chapter, s.phase = 1, 'night'
        if pid == 'P018':
            s.flags['heard_child'] = normalized == '2' or assisted
            s.guilt += int(normalized == '1')
        if pid == 'P022':
            s.flags['slice_complete'] = True
            s.phase = 'dawn'
        return True
    def relationship(self, cid, choice):
        s = self.state
        key = f'relationship_{cid}'
        if key in s.flags:
            return
        r = s.relations.setdefault(cid, dict(trust=0, familiarity=0, resentment=0, dependence=0, knowledge=0, willingness=0))
        if choice == 'listen':
            r['trust'] += 2
            r['willingness'] += 1
        else:
            r['resentment'] += 1
            s.guilt += 1
            s.flags['rumor_spread'] = True
        r['familiarity'] += 1
        r['knowledge'] += 1
        s.flags[key] = choice
    def combine(self, first, second):
        s = self.state
        if first == second or first not in s.evidence or second not in s.evidence:
            return False
        pair = set((first, second))
        correct = pair == {'E007', 'E015'} or pair == {'E011', 'E018'}
        note = 'Đối chiếu: ' + ' + '.join(sorted(pair))
        if correct:
            if note not in s.journal:
                s.journal.append(note)
                s.clarity += 2
                s.flags['corroborated'] = True
        elif note not in s.journal:
            s.journal.append(note + ' — giả thuyết chưa được xác nhận; có thể sửa.')
        return correct

def select_ending(state):
    """Full-campaign rules, previewable but not reachable from the release slice."""
    f = state.flags
    if not f.get('finale_ready'):
        return None
    allies = sum(r.get('willingness', 0) > 0 for r in state.relations.values())
    if f.get('sixth_name') and f.get('consent') and f.get('original_tape'):
        return 'D'
    if allies >= 5 and f.get('public_hearing') and f.get('corroborated'):
        return 'E'
    if f.get('corroborated') and f.get('responsibility') and f.get('consent'):
        return 'C'
    if state.clarity >= 12 and f.get('responsibility'):
        return 'B'
    return 'A'

def ending_fixture(which, state):
    s = deepcopy(state)
    s.flags = {'finale_ready': True}
    if which in 'BCDE': s.flags['responsibility'] = True; s.clarity = 15
    if which in 'CDE': s.flags.update(corroborated=True, consent=True)
    if which == 'D': s.flags.update(sixth_name=True, original_tape=True)
    if which == 'E':
        s.flags['public_hearing'] = True
        s.relations = {str(i): {'willingness': 1} for i in range(5)}
    return s
