"""Compile hand-authored speech; never synthesize or repeat lines to satisfy a word quota."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/dialogues.json'
existing=json.loads(path.read_text(encoding='utf8'))
# Retain original scenes as distinct early/late conversations and all future-chapter writing.
base=[d for d in existing if d['id'] in {'D_'+c['id'] for c in json.loads((ROOT/'data/characters.json').read_text(encoding='utf8'))}]
positions={'station':[192,224],'station_hall':[352,208],'town':[384,208],'shop':[384,240],'hospital_lobby':[384,224],'hospital':[112,224],'home':[96,224],'home_entry':[384,240],'school':[320,208],'school_vestibule':[384,240],'school_class':[352,240],'school_teachers':[400,208],'school_broadcast':[368,224],'school_corridor':[480,208],'school_store':[416,256],'school_toilets':[112,240]}
baseconfig={'hiroshi':('station',[],0),'sachiko':('hospital',['P001'],0),'natsuki':('hospital_lobby',['P001'],0),'tomoko':('shop',['P002'],0),'yui':('town',['P003'],0),'ren':('home',['P004'],0),'kaori':('school_teachers',['P015'],1),'mio':('school_toilets',['P020'],1)}
# Anchors are editorial selections, not inferred from mere existence of an ID.
anchors={'hiroshi':[2,4],'sachiko':[7,4],'natsuki':[0,4],'tomoko':[0,4],'yui':[5,4],'ren':[1,2],'kaori':[4,5],'mio':[3,8],'haruto':[4,2],'sora':[3,3],'rei':[4,4],'haruka':[2,4],'masato':[2,6],'emi':[5,5],'yuji':[4,4],'ai':[2,4],'rika':[2,7],'kazuo':[2,2],'chihiro':[4,6],'shinji':[0,4],'akane':[4,6],'fumiko':[2,4],'daichi':[0,2],'mei':[2,5],'naoto':[2,4]}
for d in base:
    c=d['character'];d['order']=0;d['after_dialogues']=[]
    if c in baseconfig:
        room,requires,chapter=baseconfig[c];d.update(room=room,requires=requires,chapter=chapter,position=positions[room])
    else:d.update(requires=[],chapter=2 if c in ('akane','rika') else 3 if c in ('yuji','ai','daichi','mei') else 4 if c in ('fumiko','chihiro') else 5)
    # Avoid the same line standing for two clues; use meaningful distinct clauses where needed.
    idxs=anchors[c]
    d['clue_links']=[]
    for target,i in zip(d['links'],idxs):
        i=min(i,len(d['lines'])-1)
        d['clue_links'].append({'target':target,'line':i,'quote':d['lines'][i]['text'],'relationship':'Lời kể được đối chiếu với sự kiện trong câu đố.'})
    if c=='yui':d['clue_links'][0].update(line=5,quote=d['lines'][5]['text']);d['clue_links'][1].update(line=4,quote=d['lines'][4]['text'])
    repairs={
        'sora': 'Trong giấy hướng dẫn hỏi, em thấy cùng một câu mà cả lớp đều dùng. Có thể họ nhớ lời được hỏi hơn điều tự nhìn thấy.',
        'rei': 'Nếu hai lời kể cùng xác nhận hành động nhưng khác động cơ, em muốn giữ phần đã xác nhận và để phần chưa biết là câu hỏi.',
        'emi': 'Em không biết tại sao anh ấy đã lấy trang giấy. Em chỉ biết trang nằm trong đồ của anh ấy; biết một việc không làm em biết hết động cơ.',
        'yuji': 'Chú đi trung tâm việc làm. Điểm đến in trên vé xe vẫn còn, dù chú từng bảo mình đang trên đường tới xưởng.',
        'kazuo': 'Ba lời khai còn cùng một từ rất hiếm, và từ ấy có trong bản hướng dẫn tôi đọc trước khi họ trả lời. Tôi đã không ghi nguồn của nó.',
    }
    if c in repairs:
        quote=repairs[c]
        index=next((i for i,line in enumerate(d['lines']) if line['text']==quote),None)
        if index is None:index=len(d['lines']);d['lines'].append({'speaker':d['lines'][0]['speaker'],'text':quote})
        d['clue_links'][1].update(line=index,quote=quote)
    d['choice_effects']=[{'trust':1,'willingness':1},{'resentment':1,'rumor':True}]
rows=base[:]
for chapter,filename in enumerate(('prologue.vi.txt','hanako.vi.txt')):
    text=(ROOT/'data/story'/filename).read_text(encoding='utf8')
    for order,block in enumerate(re.split(r'\n(?=@)',text.strip()),1):
        header,*speech=[l for l in block.splitlines() if l.strip()]
        if not header.startswith('@'):raise ValueError(header)
        key,cid,room,requires,after,targets=header[1:].split('|')
        lines=[dict(speaker=l.split(': ',1)[0],text=l.split(': ',1)[1]) for l in speech]
        links=['P'+n.zfill(3) for n in targets.split(',')]
        # The author places two distinct, concrete details in the final two spoken lines.
        clues=[dict(target=target,line=len(lines)-2+i,quote=lines[-2+i]['text'],relationship='Chi tiết trong lời nói chuẩn bị hoặc đối chiếu cho '+target) for i,target in enumerate(links)]
        choices=[{'text':'Giữ lời kể trong phạm vi đã nói.','value':'listen'}, {'text':'Kể lại ngay, chưa hỏi người nói.','value':'repeat'}]
        if cid=='ren':choices=[{'text':'Ghi rõ điều biết và điều chưa rõ.','value':'listen'},{'text':'Chấp nhận ấn tượng đầu của mình.','value':'repeat'}]
        rows.append(dict(id='D_'+key,character=cid,room=room,position=positions[room],chapter=chapter,status='playable',requires=requires.split(',') if requires else [],after_dialogues=after.split(',') if after else [],order=order,important=True,links=links,clue_links=clues,lines=lines,choices=choices,choice_effects=[{'clarity':1} if cid=='ren' else {'trust':1,'willingness':1},{'guilt':1,'rumor':cid!='ren'}]))
for d in rows:
    if d['status']=='playable':
        if d['character']=='ren': d['position']=[72,256]
        elif d['character']=='masato': d['position']=[256,272]
        elif d['character']=='haruka' and d['room']=='school': d['position']=[448,224]
path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Compiled',len(rows),'conversations;',sum(len(l['text'].split()) for d in rows if d['status']=='playable' for l in d['lines']),'playable whitespace units')
