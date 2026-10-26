"""Measure spoken content and enforce the user's full-release gates separately from a batch."""
from pathlib import Path
from collections import Counter
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core.content import Content

def words(text):return len(re.findall(r'\S+',text))
def audit(c):
    errors=[];live=[d for d in c.dialogues.values() if d['status']=='playable'];by_chapter=Counter();all_words=0;unique_lines={};duplicate_words=0
    for d in c.dialogues.values():
        for line in d['lines']:
            all_words+=words(line['text'])
            if d['status']=='playable':
                by_chapter[d['chapter']]+=words(line['text'])
                normalized=' '.join(line['text'].casefold().split())
                if normalized in unique_lines:duplicate_words+=words(line['text'])
                unique_lines[normalized]=words(line['text'])
        clues=d.get('clue_links',[])
        if len(clues)<2 or len({x['target'] for x in clues})<2:errors.append(d['id']+': needs two distinct linked clues')
        if len({x['quote'] for x in clues})<2:errors.append(d['id']+': repeated clue quote')
        for clue in clues:
            if clue['target'] not in c.puzzles:errors.append(d['id']+': unknown clue target')
            if not 0<=clue['line']<len(d['lines']) or clue['quote'] not in d['lines'][clue['line']]['text']:errors.append(d['id']+': clue not anchored in speech')
        for parent in d.get('after_dialogues',[]):
            if parent not in c.dialogues:errors.append(d['id']+': missing predecessor')
    # Story-gate reachability: all authored live scenes must be reachable once prerequisite puzzles are solved.
    from core.state import State
    from systems.dialogue import eligible
    state=State(solved=[p['id'] for p in c.playable]);remaining={d['id'] for d in live}
    while remaining:
        ready={did for did in remaining if eligible(c.dialogues[did],state)}
        if not ready:errors.append('Unreachable dialogue chain: '+','.join(sorted(remaining)));break
        state.heard.extend(sorted(ready));remaining-=ready
    maps=Counter(m['chapter'] for m in c.maps.values())
    unique_word_count=sum(unique_lines.values())
    gates={
        'eight_chapters_playable':sum(ch['status']=='playable' for ch in c.chapters.values())==8,
        'eight_maps_each_chapter':all(maps[i]>=8 for i in range(8)),
        '45000_playable_nonduplicate_spoken_units':unique_word_count>=45000,
        '25_character_biographies':len(c.characters)>=25 and all(ch.get('arc') and ch.get('past_action') and ch.get('mystery_link') for ch in c.characters.values()),
        '100_playable_connected_puzzles':len(c.playable)>=100 and all(p['requires'] or p['id']=='P001' for p in c.playable),
        'five_campaign_endings':sum(e['status']=='campaign' for e in c.endings.values())>=5,
        'two_anchored_clues_every_conversation':not errors,
    }
    return {'counting_rule':'Whitespace-delimited spoken Vietnamese units; excludes speaker names, UI, descriptions, notes, code, and repeated playback. Not linguistic Vietnamese word segmentation. Full release gate also excludes duplicate lines.',
            'errors':errors,'spoken_units_written':all_words,'spoken_units_playable':sum(by_chapter.values()),'spoken_units_playable_unique_lines':unique_word_count,'duplicate_spoken_units':duplicate_words,'playable_conversations':len(live),'written_conversations':len(c.dialogues),'per_chapter_spoken_units':dict(sorted(by_chapter.items())),'per_chapter_maps':dict(sorted(maps.items())),'dialogue_budget':sum(ch['dialogue_budget'] for ch in c.chapters.values()),'release_gates':gates,'full_release_ready':all(gates.values())}
if __name__=='__main__':
    report=audit(Content());(ROOT/'reports/narrative_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(1 if report['errors'] or ('--release' in sys.argv and not report['full_release_ready']) else 0)
