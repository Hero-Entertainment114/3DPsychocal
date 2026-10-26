"""Story-gated conversations and one-time, scene-specific social consequences."""
def eligible(dialogue,state):
    return (dialogue['status']=='playable'
            and all(p in state.solved for p in dialogue.get('requires',[]))
            and all(d in state.heard for d in dialogue.get('after_dialogues',[])))

def available(content,state,room=None,character=None):
    return sorted((d for d in content.dialogues.values() if eligible(d,state)
                   and (room is None or d['room']==room)
                   and (character is None or d['character']==character)),key=lambda d:(d.get('order',0),d['id']))

def choose(content,state,room,character):
    rows=available(content,state,room,character)
    return next((d for d in rows if d['id'] not in state.heard),rows[-1] if rows else None)

def complete(content,state,did,choice):
    d=content.dialogues[did]
    if not eligible(d,state):return False
    key='dialogue_choice_'+did
    if key in state.flags:return False
    selected=next((i for i,c in enumerate(d['choices']) if c['value']==choice),None)
    if selected is None:return False
    state.flags[key]=choice
    if did not in state.heard:state.heard.append(did)
    state.journal.append('Đã trò chuyện: '+d['lines'][0]['speaker']+' — '+d['lines'][-1]['text'])
    effect=d.get('choice_effects',[{},{}])[selected]
    cid=d['character']
    if cid!='ren':
        r=state.relations.setdefault(cid,dict(trust=0,familiarity=0,resentment=0,dependence=0,knowledge=0,willingness=0))
        for k in r:r[k]=min(100,max(-100,r[k]+effect.get(k,0)))
        r['familiarity']=min(100,r['familiarity']+1);r['knowledge']=min(100,r['knowledge']+1)
    state.clarity+=effect.get('clarity',0);state.guilt+=effect.get('guilt',0)
    if effect.get('rumor'):state.flags['rumor_spread']=True
    return True
