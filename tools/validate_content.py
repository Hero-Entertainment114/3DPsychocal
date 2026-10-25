"""Validate design data separately from implemented content; never conflate their counts."""
import sys, json, re, hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.content import Content

def validate(content):
    errors=[];warnings=[];p=content.puzzles
    def check(ok,message):
        if not ok:errors.append(message)
    check(set(p)=={f'P{i:03}' for i in range(1,101)},'Puzzle IDs must be P001–P100.')
    check(len(content.characters)>=25,'At least 25 profiles required.')
    expected=[8,14,14,14,16,16,18]
    check([sum(x['chapter']==i for x in p.values()) for i in range(7)]==expected,'Chapter allocation mismatch.')
    visited=set();active=set()
    def visit(pid):
        if pid in active:errors.append('Dependency cycle: '+pid);return
        if pid in visited:return
        active.add(pid)
        for dep in p[pid]['requires']:
            if dep not in p:errors.append(f'{pid}: missing {dep}')
            else:visit(dep)
        active.remove(pid);visited.add(pid)
    for pid,item in p.items():
        visit(pid)
        for field in ('title','room','prompt','mechanic','answers','reward','resolution','effect','difficulty','test','softlock'):
            check(bool(item.get(field)),f'{pid}: missing {field}')
        check(len(item['hints'])==3,f'{pid}: needs three hints')
        check(len(item['clues'])>=2 and len(set(item['clues']))==len(item['clues']),f'{pid}: distinct clues required')
        if item['status']=='playable':
            check(item['room'] in content.maps,f'{pid}: missing map')
            check(all(p[d]['status']=='playable' for d in item['requires']),f'{pid}: depends on unimplemented content')
    cross=sum(len(x['cross_links']) for x in p.values())
    check(cross>=30,'Fewer than 30 designed cross-chapter links.')
    # Validate graph entries reference actual rewards, not an invented extra ID.
    for item in p.values():
        for link in item['cross_links']:check(link['puzzle'] in item['requires'] and bool(link['reason']),'Invalid cross link '+item['id'])
    all_text=[];live_words=0;written_words=0
    for d in content.dialogues.values():
        check(d['character'] in content.characters,d['id']+': unknown speaker profile')
        if d['important']:check(len(set(d['links']))>=2,d['id']+': requires two links')
        check(all(link in p for link in d['links']),d['id']+': dangling link')
        text=' '.join(l['text'] for l in d['lines']);check(text not in all_text,d['id']+': duplicated dialogue');all_text.append(text)
        count=len(re.findall(r'\S+',text));written_words+=count
        if d['status']=='playable':live_words+=count
    check(written_words>=3000,'Written dialogue below 3000 whitespace units.')
    for c in content.characters.values():
        for field in ('name','age','occupation','pixel_design','personality','fear','desire','secret','misbelief','past_action','arc','trust_condition','alienation_condition','mystery_link'):
            check(bool(c.get(field)),c['id']+': missing '+field)
        check(c['puzzle'] in p,c['id']+': invalid role')
        check(all(r in content.characters for r in c['relations']),c['id']+': unknown relationship')
        for f in (f'assets/sprites/{c["id"]}.png',f'assets/sprites/{c["id"]}_portraits.png'):check((content.root/f).exists(),'Missing '+f)
    for m in content.maps.values():
        check(len(m['tiles'])==m['height'] and all(len(row)==m['width'] for row in m['tiles']),m['id']+': malformed tile grid')
        for portal in m['portals']:check(portal['to'] in content.maps,m['id']+': dangling exit')
    for e in content.endings.values():
        check(len(e['scenes'])>=3 and len(e['epilogues'])>=10,e['id']+': incomplete preview')
    manifest=json.loads((content.root/'assets/manifest.json').read_text())
    for row in manifest:
        path=content.root/row['path']
        check(path.is_file(),'Missing asset '+row['path'])
        if path.is_file():check(hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],'Changed asset '+row['path'])
    warnings.extend(['9–12 hour runtime is NOT verified.','78 puzzles are design-only; do not count them as playable.','17 dialogues are written but not placed in playable scenes.','Five endings are previews, not earned campaign endings.','English/Japanese localization, later maps and production sound are pending.'])
    return dict(errors=errors,warnings=warnings,counts=dict(puzzles_designed=len(p),puzzles_playable=len(content.playable),characters=len(content.characters),characters_on_stage=sum(c['status']=='implemented' for c in content.characters.values()),dialogues_written=len(content.dialogues),dialogues_playable=sum(d['status']=='playable' for d in content.dialogues.values()),dialogue_whitespace_units=written_words,playable_dialogue_whitespace_units=live_words,cross_chapter_edges_designed=cross,maps_playable=len(content.maps),ending_previews=len(content.endings),assets=len(manifest)),categories=dict(Counter(x['category'] for x in p.values())))

def main():
    report=validate(Content());(ROOT/'reports/content_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return int(bool(report['errors']))
if __name__=='__main__':raise SystemExit(main())
