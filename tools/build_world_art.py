"""Render the sixteen authored layouts as pixel assets; no interpolated photos."""
from pathlib import Path
import json, random, hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets'
COL={'ink':'#111b24','blue':'#293f4b','fog':'#657c7e','sage':'#728777','paper':'#d1c5a5','amber':'#d6ad68','red':'#8d4447'}
F=ImageFont.truetype(str(A/'fonts/NotoSans-Regular.ttf'),9)
def make_maps():
    maps=json.loads((ROOT/'data/maps.json').read_text(encoding='utf8'))
    floor_colors={'platform':(54,65,72),'hall':(66,76,76),'street':(42,55,62),'shop':(82,78,64),'lobby':(74,91,87),'ward':(79,91,85),'entry':(79,65,55),'kitchen':(84,76,60),'yard':(48,63,59),'vestibule':(62,68,66),'classroom':(65,65,53),'office':(63,67,62),'broadcast':(44,61,66),'corridor':(45,63,68),'store':(52,55,52),'toilets':(61,77,73),'stairs':(56,65,65),'library':(67,63,53),'medical':(77,89,82),'guard':(62,65,57)}
    for index,m in enumerate(maps):
        rng=random.Random(444+index);theme=m['theme'];base=floor_colors[theme];w,h=m['width']*16,m['height']*16
        im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im);d.fontmode='1'
        def rect(box,c):d.rectangle(box,fill=COL.get(c,c))
        def line(box,c,width=1):d.line(box,fill=COL.get(c,c),width=width)
        def label(x,y,text,c='paper'):d.text((x,y),text,font=F,fill=COL.get(c,c))
        for ty,row in enumerate(m['tiles']):
            for tx,tile in enumerate(row):
                x,y=tx*16,ty*16
                if tile==0:
                    shade=tuple(max(0,min(255,c+rng.randrange(-2,3))) for c in base);rect((x,y,x+15,y+15),shade)
                    line((x,y+15,x+15,y+15),tuple(c-9 for c in base))
                    if theme not in ('entry','kitchen','classroom'):line((x,y,x,y+15),tuple(c-7 for c in base))
                    for _ in range(3):d.point((x+rng.randrange(16),y+rng.randrange(15)),fill=tuple(c+4 for c in base))
                elif tile==1:
                    rect((x,y,x+15,y+15),'blue');line((x,y+14,x+15,y+14),'ink');line((x+8,y,x+8,y+14),'#344b52')
                else:
                    rect((x,y,x+15,y+15),'#665a48');rect((x+1,y+1,x+14,y+10),'#968267');line((x+1,y+2,x+14,y+2),'#b6a181')
                    if theme=='shop':
                        for px in (2,6,10):rect((x+px,y+3,x+px+2,y+8),rng.choice(['#a78a5d','#738b76','#926259']))
                    elif theme in ('vestibule','store'):
                        rect((x+2,y+2,x+13,y+12),'#4d5753');rect((x+4,y+4,x+10,y+6),'paper');d.point((x+11,y+9),fill=COL['amber'])
                    elif theme=='ward':
                        rect((x,y,x+15,y+15),'#adbaab');line((x,y,x+15,y),'paper')
                    elif theme=='toilets':rect((x+1,y+1,x+14,y+13),'#63796e');line((x+1,y+12,x+14,y+12),'ink')
        if theme in ('platform','street','yard'):
            for x in range(24,w-20,64):
                line((x,64,x,90),'fog');rect((x-6,64,x+6,70),'amber')
            for _ in range(80):
                x=rng.randrange(20,w-20);y=rng.randrange(72,h-36);line((x,y,x+3,y),'#567079')
        else:
            for x in range(40,w-50,110):
                rect((x,12,x+55,47),'ink');rect((x+3,15,x+52,43),'#3b5660');line((x+27,15,x+27,43),'fog',2);line((x+3,29,x+52,29),'fog',2);rect((x-2,47,x+57,51),'#99977b')
        if theme=='platform':
            for y in (h-22,h-12):line((20,y,w-20,y),'fog',2)
            for x in range(20,w-20,12):rect((x,h-24,x+3,h-10),'#7d705b')
            label(260,22,'TSUKIMORI / 16:10')
            rect((w-105,68,w-25,94),'ink');label(w-100,72,'TUYEN TAM DUNG','amber')
        elif theme=='hall':
            rect((176,14,306,49),'ink');label(181,19,'VE TAU / 1 HANG - 2 KHACH','amber')
            rect((w-50,96,w-25,142),'#55756c');rect((w-46,100,w-30,114),'ink');line((w-45,119,w-32,119),'paper');line((w-44,123,w-44,136),'ink',3)
        elif theme=='street':
            for x,title in ((80,'SAKURAI'),(240,'BỆNH VIỆN'),(450,'ĐƯỜNG VỀ NHÀ')):
                rect((x,10,x+110,45),'#685a4b');label(x+6,20,title,'paper')
                for ax in range(x,x+110,10):rect((ax,50,ax+8,62),'#8b6257' if ax%20 else '#b9ac8b')
        elif theme=='shop':
            rect((200,15,370,48),'#786b55');label(213,23,'SAKURAI • CƠM / TRÀ / PIN','paper')
            # Register, crates, sleeping cat: non-colliding wall decoration.
            rect((360,70,403,91),'ink');rect((364,73,393,80),'sage');label(365,80,'400','amber')
            d.ellipse((40,65,67,75),fill='#a69b7e');d.polygon([(43,69),(43,62),(49,67)],fill='#a69b7e')
        elif theme=='lobby':
            rect((155,12,342,46),'paper');label(165,19,'TIẾP NHẬN • XIN CHỜ ĐẾN LƯỢT','ink')
            rect((32,70,82,82),'#9b8d6e');label(38,70,'LẤY SỐ','ink')
        elif theme=='ward':
            label(42,21,'204 / PHÒNG BỆNH','paper')
            for x in (305,385):rect((x,114,x+38,135),'paper');rect((x+4,117,x+34,130),'#dce2cf')
            line((433,76,433,158),'fog',2);rect((424,79,439,98),'#acb9ac')
            label(36,75,'KHĂN KHÔ / NƯỚC ẤM','paper')
        elif theme=='entry':
            rect((285,32,336,60),'ink');rect((290,36,324,53),'#77928a');line((293,41,321,41),'sage');d.point((330,51),fill=COL['amber'])
            for x in range(72,114,14):d.ellipse((x,115,x+9,120),fill='#25373d')
            label(48,21,'NHÀ MIZUHARA','paper')
        elif theme=='kitchen':
            rect((385,103,430,125),'ink')
            for x in (396,419):d.ellipse((x-7,108,x+7,120),outline=COL['fog'],width=2)
            for x in (222,264):d.ellipse((x,151,x+13,160),fill=COL['paper']);line((x+17,150,x+18,161),'amber')
            label(60,22,'BẾP • HAI CHIẾC BÁT','paper')
        elif theme=='yard':
            rect((175,5,458,51),'#4a605d');label(250,21,'TRƯỜNG TSUKIMORI','paper')
            for x in (159,449):
                rect((x-5,80,x+4,135),'#635a49');d.polygon([(x-32,85),(x-15,64),(x+15,64),(x+32,85),(x+20,105),(x-22,108)],fill='#536d60');line((x,90,x+14,75),'#84917a')
            line((55,h-70,w-50,h-70),'#809080')
        elif theme=='vestibule':
            label(200,22,'TỦ GIÀY / LỊCH TRỰC','paper')
            for x in (112,368):rect((x,118,x+26,129),'paper');line((x+3,123,x+20,123),'fog')
        elif theme=='classroom':
            rect((150,10,410,48),'#3e5e4c');rect((146,48,415,52),'#a39570');label(170,20,'6–2    NHẠC / VẼ / TOÁN','paper')
            rect((440,83,467,107),'#8f7e60');d.ellipse((448,80,460,88),fill='#98aa8a');line((455,83,455,98),'sage')
        elif theme=='office':
            label(154,22,'PHÒNG GIÁO VIÊN','paper')
            for x in (112,334):
                rect((x,131,x+27,145),'paper');line((x+3,135,x+22,135),'red');line((x+3,140,x+23,140),'fog')
        elif theme=='broadcast':
            label(145,21,'PHÁT THANH / NGẮT NGUỒN KHI NỐI DÂY','paper')
            for x in (82,340):
                rect((x,99,x+45,125),'ink')
                for xx in (x+12,x+32):d.ellipse((xx-8,103,xx+8,119),outline=COL['fog'],width=2);d.point((xx,111),fill=COL['paper'])
        elif theme=='corridor':
            d.ellipse((282,7,316,42),fill=COL['paper'],outline=COL['ink'],width=3);line((299,25,309,31),'ink',2);line((299,25,287,27),'ink',2)
            label(344,21,'TẦNG '+str(m.get('floor',3)),'paper')
        elif theme=='store':
            label(169,20,'PHÒNG Y TẾ','paper');line((165,39,279,39),'#ac9270');d.point((160,39),fill=COL['amber'])
            rect((414,77,449,105),'#bcb99b');line((421,91,442,91),'red',3);line((431,81,431,101),'red',3)
        elif theme=='toilets':
            for n,x in enumerate((96,208,320),1):
                label(x+21,85,str(n),'paper');rect((x+47,124,x+50,129),'amber')
            rect((33,71,71,88),'paper');d.ellipse((39,74,65,84),fill='#69817b');line((52,66,52,77),'fog',2)
            label(183,23,'ĐỪNG GỌI THAY MỘT CÁI TÊN' if m['id']=='school_toilets' else 'XIN KHÓA VÒI NƯỚC','paper')
        if theme=='stairs':
            for sy in range(112,241,12):
                rect((170,sy,330,sy+9),'#838579');line((170,sy,330,sy),'#bcc0ab')
            line((164,104,164,248),'#aea88c',3);line((337,104,337,248),'#aea88c',3)
            label(350,142,'↑' if m['floor']==1 else '↑↑','paper')
        if theme=='library':
            for xx in range(116,170,7):rect((xx,99,xx+4,139),rng.choice(['#8d6860','#9c986a','#6d8c7c']))
            rect((330,133,355,147),'paper');line((343,133,343,147),'ink')
        if theme=='medical':
            rect((112,97,175,148),'#afbbad');rect((117,102,138,115),'paper')
            line((336,110,351,110),'red',3);line((343,103,343,117),'red',3)
        if theme=='guard':
            rect((117,99,170,121),'#5e796b');rect((126,103,158,115),'ink')
            d.ellipse((350,109,362,121),fill='#a79774');line((356,112,356,118),'ink')
        if 'sign' in m:
            # Rasterize CJK once; the runtime does not depend on a system font.
            jf=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',14)
            text=m['sign']['jp'];bounds=d.textbbox((0,0),text,font=jf);tw=bounds[2]-bounds[0]
            sx,sy=m['sign']['position'];rect((sx-tw//2-7,sy-24,sx+tw//2+7,sy-3),'paper')
            d.text((sx-tw//2,sy-25),text,font=jf,fill=COL['ink'])
        for door in m['portals']:
            x,y=door['x'],door['y'];rect((x-14,y-5,x+14,y+8),'#b2a17a');d.polygon([(x-5,y),(x+5,y),(x,y+5)],fill=COL['ink'])
        im.save(A/'maps'/f'{m["id"]}.png')

def manifest():
    entries=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(A.rglob('*')) if p.is_file() and p.name!='manifest.json']
    (A/'manifest.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':make_maps();manifest();print('Rendered authored map layouts')
