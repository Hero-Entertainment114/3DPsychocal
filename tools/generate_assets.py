"""Deterministic, low-resolution pixel artwork and synthesized PCM audio.
No raster photos, resampling filters, paid APIs, or external runtime downloads.
Run from any directory; Pillow is a development dependency only.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math, random, wave, struct, shutil
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
PAL={'ink':'#111b24','deep':'#182733','blue':'#293f4b','fog':'#4b6970','sage':'#728777','paper':'#d1c5a5','amber':'#d6ad68','red':'#8d4447','skin':'#ba9a80','white':'#e2ddc3'}
rng=random.Random(444)
def save(im,name):
    p=A/name;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def rect(d,box,c):d.rectangle(box,fill=PAL.get(c,c))
font_path=Path('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf')
if not (A/'fonts/NotoSans-Regular.ttf').exists():
    if not font_path.exists(): raise SystemExit('Copy NotoSans-Regular.ttf and its SIL OFL license to assets/fonts first.')
    shutil.copy(font_path,A/'fonts/NotoSans-Regular.ttf')
    shutil.copy('/usr/share/doc/fonts-noto-core/copyright',A/'fonts/NOTO-LICENSE.txt')
F=ImageFont.truetype(str(A/'fonts/NotoSans-Regular.ttf'),9)
# Consistent character proportions; six frames x four directions.
chars=json.loads((ROOT/'data/characters.json').read_text())
coats=['#6a7a65','#728580','#4a6071','#b29458','#465a70','#c2c7ba','#7d6a5e','#536e7a','#7d6879','#4a6665','#985d53','#a15c51','#5b7774','#465a72','#d1ac61','#a58c72','#405b70','#7a627b','#676f72','#647179','#84735f','#6b7770','#ba8b55','#8c3d43','#596f67']
for ci,c in enumerate(chars):
    sheet=Image.new('RGBA',(192,192)); d=ImageDraw.Draw(sheet)
    for direction in range(4):
        for frame in range(6):
            ox=frame*32; oy=direction*48; bob=1 if frame in (1,4) else 0; yy=oy+bob
            d.ellipse((ox+6,oy+40,ox+27,oy+45),fill=(0,0,0,70))
            # Outline follows silhouette, not a single rectangle.
            d.polygon([(ox+11,yy+9),(ox+20,yy+9),(ox+23,yy+13),(ox+22,yy+22),(ox+25,yy+25),(ox+25,yy+33),(ox+21,yy+35),(ox+21,yy+42),(ox+16,yy+42),(ox+15,yy+36),(ox+14,yy+42),(ox+9,yy+42),(ox+10,yy+34),(ox+7,yy+32),(ox+8,yy+25),(ox+10,yy+22),(ox+9,yy+14)],fill=PAL['ink'])
            rect(d,(ox+11,yy+14,ox+21,yy+22),'skin')
            rect(d,(ox+10,yy+10,ox+20,yy+15),'ink');rect(d,(ox+10,yy+13,ox+12,yy+20),'ink')
            if direction!=3:
                ex=ox+(19 if direction==2 else 13)
                rect(d,(ex,yy+17,ex+1,yy+18),'ink')
                if direction==0:rect(d,(ox+19,yy+17,ox+20,yy+18),'ink')
                rect(d,(ox+16,yy+21,ox+18,yy+21),'#876d64')
            else:rect(d,(ox+11,yy+14,ox+21,yy+21),'ink')
            rect(d,(ox+10,yy+24,ox+22,yy+33),coats[ci]);rect(d,(ox+15,yy+24,ox+17,yy+28),'paper')
            rect(d,(ox+11,yy+26,ox+12,yy+31),'#52605b')
            step=[0,1,2,0,-1,-2][frame]
            rect(d,(ox+10,yy+34,ox+14,yy+40+step),'deep');rect(d,(ox+17,yy+34,ox+21,yy+40-step),'deep')
            rect(d,(ox+9,yy+40+step,ox+14,yy+42+step),'#5a4b42');rect(d,(ox+17,yy+40-step,ox+22,yy+42-step),'#5a4b42')
            rect(d,(ox+8,yy+27+step,ox+10,yy+32+step),'skin');rect(d,(ox+22,yy+27-step,ox+24,yy+32-step),'skin')
            if ci==0:rect(d,(ox+20,yy+29,ox+25,yy+35),'#80654d');d.line((ox+11,yy+23,ox+22,yy+30),fill='#a59368')
    save(sheet,f'sprites/{c["id"]}.png')
    # Portrait expressions: neutral / uneasy / sad, authored at 48 then nearest-neighbor to 96.
    out=Image.new('RGBA',(288,96))
    for expr in range(3):
        p=Image.new('RGBA',(48,48)); q=ImageDraw.Draw(p)
        q.polygon([(4,47),(6,36),(16,32),(31,32),(41,36),(45,47)],fill=coats[ci])
        q.polygon([(12,9),(16,4),(32,4),(36,10),(35,26),(29,34),(19,34),(12,27)],fill=PAL['ink'])
        q.polygon([(14,14),(33,13),(33,26),(28,32),(20,32),(15,26)],fill=PAL['skin'])
        q.polygon([(13,16),(13,7),(31,7),(35,14),(30,12),(27,16),(24,12),(20,17),(18,12)],fill=PAL['ink'])
        q.line((17,20-expr,21,20),fill=PAL['ink'],width=1);q.line((27,20,31,20-expr),fill=PAL['ink'])
        q.point((19,22),fill=PAL['ink']);q.point((29,22),fill=PAL['ink']);q.line((23,27+expr,27,27),fill='#765952')
        q.line((14,23,15,28),fill='#9c786b');q.line((25,22,25,25),fill='#a48370')
        out.paste(p.resize((96,96),Image.Resampling.NEAREST),(expr*96,0))
    save(out,f'sprites/{c["id"]}_portraits.png')
# Props, actual silhouettes and small highlights.
props=Image.new('RGBA',(32*8,48));d=ImageDraw.Draw(props)
for i in range(8):
    x=i*32
    if i==0: # Papers/books on a lectern
        rect(d,(x+3,26,x+28,31),'#6e5e4d');rect(d,(x+6,32,x+8,43),'#51483e');rect(d,(x+24,32,x+26,43),'#51483e')
        d.polygon([(x+7,16),(x+16,18),(x+25,16),(x+25,27),(x+16,29),(x+7,27)],fill=PAL['paper'])
        d.line((x+16,18,x+16,28),fill='#998c74')
        for j in (20,23,26):d.line((x+9,j,x+13,j+1),fill='#7e7b6b')
    elif i==1: # Cassette
        rect(d,(x+4,22,x+27,38),'ink');rect(d,(x+6,24,x+25,35),'sage');rect(d,(x+8,27,x+23,31),'deep')
        for xx in (x+10,x+21):d.ellipse((xx-2,27,xx+2,31),fill=PAL['paper'])
        d.line((x+9,33,x+22,33),fill=PAL['amber'])
    elif i==2: # School desk
        rect(d,(x+3,17,x+28,30),'#87775d');rect(d,(x+3,17,x+28,19),'#b2a17a');rect(d,(x+6,31,x+8,43),'fog');rect(d,(x+24,31,x+26,43),'fog');d.line((x+7,36,x+25,36),fill=PAL['blue'])
    elif i==3: # Locker
        rect(d,(x+5,7,x+26,44),'ink');rect(d,(x+7,9,x+24,42),'sage');d.line((x+16,10,x+16,41),fill=PAL['blue'])
        for y in (13,16,19):d.line((x+9,y,x+13,y),fill=PAL['fog']);d.line((x+19,y,x+22,y),fill=PAL['fog'])
        rect(d,(x+13,26,x+14,29),'amber')
    elif i==4: # CRT
        rect(d,(x+2,15,x+29,36),'ink');rect(d,(x+5,18,x+23,31),'fog');rect(d,(x+7,20,x+21,29),'#73958e')
        for y in range(20,30,3):d.line((x+7,y,x+21,y),fill='#516c6a')
        rect(d,(x+25,20,x+27,22),'amber');rect(d,(x+7,37,x+10,42),'ink');rect(d,(x+23,37,x+26,42),'ink')
    elif i==5: # Lamp
        rect(d,(x+15,10,x+17,44),'blue');d.polygon([(x+10,9),(x+13,3),(x+20,3),(x+23,9)],fill=PAL['deep']);rect(d,(x+12,10,x+21,17),'amber');rect(d,(x+10,9,x+23,11),'fog');rect(d,(x+10,18,x+23,19),'fog')
    elif i==6: # Potted plant
        rect(d,(x+11,33,x+23,43),'#806557');rect(d,(x+9,30,x+25,34),'#a2866b');d.line((x+17,15,x+17,31),fill=PAL['sage'])
        for xx,yy in [(13,14),(20,18),(12,23),(21,26)]:d.polygon([(xx-6,yy-4),(xx+3,yy-2),(xx+4,yy+4),(xx,yy+3)],fill=PAL['sage'])
    else: # Door
        rect(d,(x+2,0,x+29,46),'ink');rect(d,(x+5,3,x+26,45),'#626e68');rect(d,(x+7,5,x+24,22),'deep');rect(d,(x+9,7,x+22,20),'fog');rect(d,(x+23,30,x+25,32),'amber');rect(d,(x+8,37,x+23,40),'blue')
save(props,'sprites/props.png')
# Tileset: 5 themes, four tiles each.
tiles=Image.new('RGB',(64,80));td=ImageDraw.Draw(tiles)
for row,base in enumerate([(48,64,70),(45,58,64),(74,85,80),(76,71,59),(49,65,65)]):
    for tile in range(4):
        ox=tile*16;oy=row*16
        col=tuple(max(0,int(c*(0.72 if tile==1 else 1))) for c in base)
        td.rectangle((ox,oy,ox+15,oy+15),fill=col)
        if tile==0:
            td.line((ox,oy+15,ox+15,oy+15),fill=tuple(max(0,c-10) for c in col));td.line((ox,oy,ox,oy+15),fill=tuple(max(0,c-8) for c in col))
            for _ in range(10):
                px,py=rng.randrange(1,15),rng.randrange(1,15);td.point((ox+px,oy+py),fill=tuple(min(255,c+rng.randrange(-4,5)) for c in col))
        elif tile==1:
            td.line((ox,oy+9,ox+15,oy+9),fill=PAL['deep']);td.line((ox+8,oy,ox+8,oy+9),fill=PAL['deep'])
        elif tile==2:td.rectangle((ox+1,oy+1,ox+14,oy+14),outline=PAL['amber'])
        else:
            td.rectangle((ox+1,oy+1,ox+14,oy+11),fill='#806e56');td.rectangle((ox+1,oy+1,ox+14,oy+2),fill='#a28b66')
save(tiles,'tilesets/tsukimori.png')
# Saved world backgrounds generated from real map and collision data.
maps=json.loads((ROOT/'data/maps.json').read_text());puzzles=json.loads((ROOT/'data/puzzles.json').read_text())
for idx,m in enumerate(maps):
    im=Image.new('RGB',(m['width']*16,m['height']*16));d=ImageDraw.Draw(im)
    for y,row in enumerate(m['tiles']):
        for x,t in enumerate(row):im.paste(tiles.crop((t*16,idx*16,t*16+16,idx*16+16)),(x*16,y*16))
    for x in range(48,im.width-50,96):
        rect(d,(x,16,x+43,47),'ink');rect(d,(x+3,19,x+40,43),'blue');d.line((x+21,19,x+21,43),fill=PAL['fog']);d.line((x+3,31,x+40,31),fill=PAL['fog'])
        rect(d,(x,47,x+44,50),'#8d8b70')
        # Light streak, limited bands of the palette.
        d.polygon([(x,64),(x+42,64),(x+65,88),(x+8,88)],fill='#3c5153')
    if m['id']=='station':
        rect(d,(24,292,im.width-25,305),'ink')
        for y in (294,302):d.line((24,y,im.width-25,y),fill=PAL['fog'])
        for x in range(24,im.width-25,12):rect(d,(x,292,x+3,305),'#625c4f')
    if m['id']=='town':
        for x in (60,190,360,500):
            rect(d,(x,72,x+60,82),'#785d50');d.line((x,83,x+60,83),fill=PAL['amber'])
            im.alpha_composite if False else None
            prop=props.crop((160,0,192,48));im.paste(prop,(x+52,154),prop)
        for _ in range(80):
            x=rng.randrange(20,im.width-20);y=rng.randrange(270,im.height-20);d.line((x,y,x+4,y),fill='#415a61')
    if m['id']=='hospital':
        for x in (330,390):rect(d,(x,150,x+35,205),'#a6afa1');rect(d,(x+3,153,x+32,169),'paper');rect(d,(x+3,174,x+32,201),'#7d938d')
    if m['id']=='home':
        rect(d,(335,204,440,256),'#8e846a')
        for y in range(207,254,3):d.line((338,y,437,y),fill='#7d7964')
        rect(d,(357,213,413,238),'#6f5545');d.ellipse((367,218,377,226),fill=PAL['paper']);d.ellipse((393,218,403,226),fill=PAL['paper'])
    for p in puzzles:
        if p['status']=='playable' and p['room']==m['id']:
            x,y=p['position'];kind=1 if p['id'] in ('P006','P013') else 4 if p['id']=='P005' else 3 if p['id'] in ('P009','P016') else 7 if p['id'] in ('P020','P021') else 0
            prop=props.crop((kind*32,0,kind*32+32,48));im.paste(prop,(x-16,y-36),prop)
    for door in m['portals']:
        x,y=door['x'],door['y'];rect(d,(x-13,y-4,x+13,y+7),'#9d906b');d.polygon([(x-4,y+1),(x+4,y+1),(x,y+5)],fill=PAL['paper'])
    save(im,f'maps/{m["id"]}.png')
# Main menu: a quiet, perspectival school corridor, composed at 480 x 270.
im=Image.new('RGB',(480,270),PAL['ink']);d=ImageDraw.Draw(im)
d.polygon([(0,0),(480,0),(339,98),(283,98)],fill='#172731')
d.polygon([(0,0),(283,98),(283,166),(0,270)],fill='#233943')
d.polygon([(480,0),(339,98),(339,166),(480,270)],fill='#31494e')
d.polygon([(0,270),(283,166),(339,166),(480,270)],fill='#2d4147')
rect(d,(283,98,339,166),'#405550')
# Perspective floorboards.
for x in range(-200,760,65):d.line((311,158,x,270),fill='#1c2b33')
for y in (177,193,216,247):d.line((0,y,480,y),fill='#23353d')
# Windows on right wall, sharp lattice, rain and muted reflections.
for pts in [[(376,53),(457,11),(457,172),(376,148)],[(346,85),(368,73),(368,146),(346,139)]]:
    d.polygon(pts,fill='#101e2a',outline='#7b8f87');x0=min(x for x,y in pts);x1=max(x for x,y in pts)
    inner=[(x+3 if x==x0 else x-3,y+5 if y<100 else y-4) for x,y in pts];d.polygon(inner,fill='#3b5766')
    mid=(x0+x1)//2;d.line((mid,pts[0][1]-10,mid,pts[2][1]-10),fill='#182b36',width=3)
    d.line((x0,104,x1,100),fill='#1a2a33',width=3)
    for _ in range(28):
        x=rng.randrange(x0+4,x1-2);y=rng.randrange(78,133);d.line((x,y,x-2,y+5),fill='#64828c')
# Bulletin board, notices, old clock.
d.polygon([(50,62),(157,91),(157,157),(50,190)],fill='#1b2a31',outline='#7a7660')
for x,y,w,h in [(66,84,20,40),(95,96,19,29),(122,106,21,34)]:
    rect(d,(x,y,x+w,y+h),'#aba58a')
    for sy in range(y+5,y+h-3,5):d.line((x+3,sy,x+w-3,sy+1),fill='#7c8174')
d.ellipse((184,70,215,102),fill='#a5a88e',outline='#14232d',width=3)
d.line((199,86,207,91),fill='#263c43',width=2);d.line((199,86,187,87),fill='#263c43')
# Door and the small third-panel window.
rect(d,(295,110,326,165),'ink');rect(d,(298,113,323,164),'#657367');rect(d,(302,118,318,135),'#1d303a');rect(d,(318,145,320,147),'amber')
rect(d,(298,105,323,108),'#b0a886')
# Fluorescent lights and reflections.
for box in [(188,9,316,13),(263,63,325,66),(289,88,321,90)]:rect(d,box,'#bbc8ab')
for box in [(192,246,323,249),(265,202,327,203),(290,181,322,182)]:rect(d,box,'#687a6b')
# Border details / drifting dust remain pixel-perfect.
for _ in range(45):
    x=rng.randrange(175,470);y=rng.randrange(20,265);d.point((x,y),fill='#5a6d68')
save(im,'backgrounds/corridor.png')
# Original Japanese title is rendered once as a 1-bit pixel mask, not a photographic filter.
jp=Path('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc')
if jp.exists():
    logo=Image.new('RGBA',(240,44));mask=Image.new('1',(240,44));md=ImageDraw.Draw(mask)
    md.text((2,0),'忘れられた声',font=ImageFont.truetype(str(jp),31),fill=1)
    logo.paste(PAL['paper'],(0,0,240,44),mask);save(logo,'ui/logo.png')
    shutil.copy('/usr/share/doc/fonts-noto-cjk/copyright',A/'fonts/NOTO-CJK-LICENSE.txt')
# Icon and atlas metadata.
icon=Image.new('RGBA',(32,32),PAL['ink']);q=ImageDraw.Draw(icon);rect(q,(7,3,25,30),'sage');rect(q,(10,6,22,17),'deep');rect(q,(21,23,23,25),'amber');rect(q,(2,29,29,31),'red');save(icon,'ui/icon.png');icon.save(A/'ui/icon.ico',sizes=[(32,32)])
(A/'sprites/atlas.json').write_text(json.dumps({'characters':{'frame_width':32,'frame_height':48,'columns':6,'rows':4,'directions':['down','left','right','up'],'fps':8},'portraits':{'frame_width':96,'frame_height':96,'columns':3,'expressions':['neutral','uneasy','sad']},'props':{'frame_width':32,'frame_height':48,'columns':8}},indent=2))
# Soft PCM assets; conservative peaks, seeded noise, fade-in/out, no imported music.
RATE=22050
def wav(name,seconds,fn):
    frames=bytearray()
    for i in range(int(seconds*RATE)):
        t=i/RATE;fade=min(1,t/.04,(seconds-t)/.1);s=max(-.7,min(.7,fn(t)))*fade
        frames+=struct.pack('<h',int(s*32767))
    with wave.open(str(A/name),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(frames)
wav('audio/step.wav',.12,lambda t:rng.uniform(-1,1)*.14*math.exp(-35*t))
wav('audio/knock.wav',.42,lambda t:math.sin(2*math.pi*135*t)*math.exp(-18*t)*.35)
wav('audio/chime.wav',1.5,lambda t:(math.sin(2*math.pi*660*t)+.3*math.sin(2*math.pi*990*t))*.15*math.exp(-3*t))
wav('audio/rain.wav',8,lambda t:rng.uniform(-1,1)*.045+math.sin(2*math.pi*90*t)*.004)
wav('audio/hum.wav',8,lambda t:math.sin(2*math.pi*60*t)*.025+math.sin(2*math.pi*120*t)*.007)
notes=[220,261.63,293.66,329.63,293.66,196]
for ch in range(7):
    def tune(t,ch=ch):
        k=int(t/2)%6;local=t%2;freq=notes[k]*(.5 if ch==4 else 1)
        if k==5 and ch<6:return 0
        return .12*math.sin(2*math.pi*freq*local)*math.exp(-2.4*local)+.025*math.sin(2*math.pi*freq*.5*t)
    wav(f'music/{"sixth_name" if ch==6 else "chapter_"+str(ch)}.wav',12,tune)
manifest=[]
import hashlib
for f in sorted(A.rglob('*')):
    if f.is_file() and f.name!='manifest.json':manifest.append(dict(path=f.relative_to(ROOT).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Generated',len(manifest),'assets with deterministic seed 444')
