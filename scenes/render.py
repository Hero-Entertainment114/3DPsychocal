import math
import pygame
from core.paths import ROOT

C={'ink':(17,27,36),'deep':(24,39,51),'blue':(41,63,75),'fog':(91,117,120),'sage':(114,135,119),'paper':(217,208,180),'amber':(214,173,104),'red':(141,68,71),'muted':(145,161,151)}
class Renderer:
    def __init__(self,screen,content):
        self.screen=screen
        self.fonts={size:pygame.font.Font(str(ROOT/'assets/fonts/NotoSans-Regular.ttf'),size) for size in (9,10,11,12,15,20)}
        self.cache={}
        self.assets={}
        for p in (ROOT/'assets').rglob('*.png'):
            self.assets[p.relative_to(ROOT/'assets').as_posix()]=pygame.image.load(str(p)).convert_alpha()
        self.vignette=pygame.Surface((480,270),pygame.SRCALPHA)
        for i in range(18):pygame.draw.rect(self.vignette,(6,12,19,max(0,12-i//2)),(i,i,480-2*i,270-2*i),1)
        self.content=content
    def text(self,text,x,y,color='paper',size=11):
        key=(str(text),size,color)
        if key not in self.cache:
            if len(self.cache)>3000:self.cache.clear()
            self.cache[key]=self.fonts[size].render(str(text),False,C.get(color,color))
        self.screen.blit(self.cache[key],(int(x),int(y)))
    def wrap(self,text,width,size=11):
        lines=[]
        for paragraph in str(text).split('\n'):
            current=''
            for word in paragraph.split():
                trial=(current+' '+word).strip()
                if self.fonts[size].size(trial)[0]>width and current:lines.append(current);current=word
                else:current=trial
            lines.append(current)
        return lines
    def paragraph(self,text,x,y,width,size=11,color='paper',lineheight=15,maxlines=None):
        lines=self.wrap(text,width,size)
        for i,line in enumerate(lines[:maxlines] if maxlines is not None else lines):self.text(line,x,y+i*lineheight,color,size)
        return y+len(lines)*lineheight
    def panel(self,title,subtitle=''):
        s=self.screen
        pygame.draw.rect(s,C['ink'],(16,19,448,233))
        pygame.draw.rect(s,C['fog'],(16,19,448,233),1)
        pygame.draw.rect(s,C['amber'],(24,28,2,17))
        self.text(title,34,27,'paper',15)
        if subtitle:self.text(subtitle,34,49,'muted',9)
        pygame.draw.line(s,C['blue'],(28,64),(452,64))
    def sprite(self,cid,x,y,frame=0,direction=0,alpha=255):
        sheet=self.assets[f'sprites/{cid}.png'];area=pygame.Rect(frame*32,direction*48,32,48)
        if alpha==255:self.screen.blit(sheet,(int(x)-16,int(y)-44),area)
        else:
            part=sheet.subsurface(area).copy();part.set_alpha(alpha);self.screen.blit(part,(int(x)-16,int(y)-44))
    def menu(self,items,selected,progress,t,settings):
        self.screen.blit(self.assets['backgrounds/corridor.png'],(0,0))
        # An opaque, worn paper-like inset maintains readable navigation.
        pygame.draw.rect(self.screen,C['ink'],(17,19,226,236))
        pygame.draw.line(self.screen,C['fog'],(22,23),(22,250))
        self.text('TSUKIMORI  /  OCTOBER 1998',35,31,'amber',9)
        self.screen.blit(self.assets['ui/logo.png'],(30,47))
        self.text('THE FORGOTTEN VOICES',35,93,'paper',12)
        self.text('NHỮNG TIẾNG NÓI BỊ LÃNG QUÊN',35,112,'muted',9)
        for i,label in enumerate(items):
            y=137+i*15
            if i==selected:
                pygame.draw.rect(self.screen,C['blue'],(31,y-1,195,15));self.text('›',35,y,'amber',11)
            self.text(label,49,y,'amber' if i==selected else 'paper',10)
        self.text('BẢN SẢN XUẤT 0.1 • MỞ ĐẦU + HANAKO',268,250,'paper',9)
        if progress>=9:self.sprite('mio',312,158,alpha=100)
        if progress>=22:
            overlay=pygame.Surface((237,270),pygame.SRCALPHA);overlay.fill((185,153,90,28));self.screen.blit(overlay,(243,0))
        elif not settings['reduced_motion']:
            for i in range(24):
                x=380+(i*17)%73;y=67+int(t*22+i*13)%80
                pygame.draw.line(self.screen,C['fog'],(x,y),(x-1,y+4))
    def world(self,world,progress,t,settings,scare=0):
        state=world.state;cam=world.camera
        self.screen.fill(C['ink']);self.screen.blit(self.assets[f'maps/{state.room}.png'],(-int(cam.x),-int(cam.y)))
        if state.memory:
            overlay=pygame.Surface((480,270),pygame.SRCALPHA);overlay.fill((92,53,56,38));self.screen.blit(overlay,(0,0))
            self.text('NHÀ KHO',max(8,380-cam.x),max(40,62-cam.y),'amber',10)
        elif state.room=='school':self.text('PHÒNG Y TẾ',max(8,380-cam.x),max(40,62-cam.y),'muted',10)
        people=[(p['y'],p['id'],p['x'],p['y'],0,0) for p in world.actors()]
        frame=int(world.walk_time*8)%6 if world.moving else 0
        people.append((state.y,'ren',state.x,state.y,frame,world.direction))
        for _,cid,x,y,f,dr in sorted(people):self.sprite(cid,x-cam.x,y-cam.y,f,dr)
        if scare>0 and not settings['reduced_scares']:self.sprite('mio',340-cam.x,170-cam.y,alpha=int(min(1,scare)*140))
        for o in world.objects():
            x,y=o['x']-cam.x,o['y']-cam.y
            if o['kind']=='puzzle':
                if o['id'] in state.solved:color=C['sage'];mark='·'
                elif progress.available(o['id']):color=C['amber'];mark='!'
                else:continue
                self.text(mark,x-2,y-51,color,12)
            elif o['kind']=='portal':self.text(o['label'],x-15,y+10,'muted',9)
        if state.room in ('station','town') and not settings['reduced_motion']:
            for i in range(36):
                x=(i*71+int(t*5))%480;y=(i*43+int(t*90))%270
                pygame.draw.line(self.screen,(88,113,123),(x,y),(x-2,y+7))
        self.screen.blit(self.vignette,(0,0))
        pygame.draw.rect(self.screen,C['ink'],(0,0,480,27))
        self.text(world.room['name'],10,5,'paper',10)
        phases={'afternoon':'CHIỀU','evening':'TỐI','night':'ĐÊM','dawn':'RẠNG SÁNG'}
        self.text(phases[state.phase]+'  •  '+str(len(state.solved))+'/22',352,6,'amber',9)
        near=world.nearest()
        if near:
            label=f"[{settings['keys']['interact'].upper()}] {near['label']}"
            w=min(460,self.fonts[10].size(label)[0]+20)
            pygame.draw.rect(self.screen,C['ink'],(240-w//2,226,w,20));self.text(label,250-w//2,229,'paper',10)
        pygame.draw.rect(self.screen,C['ink'],(0,254,480,16))
        self.text('WASD Di chuyển • Shift Chạy • J Sổ tay • Tab Túi • Esc Tạm dừng',8,255,'muted',9)
        if settings['crt']:
            for y in range(29,253,3):pygame.draw.line(self.screen,(20,32,40),(0,y),(479,y))
    def dialogue(self,d,pages,index,choice):
        self.panel(d['lines'][pages[index][0]]['speaker'],'LẮNG NGHE  /  '+str(index+1)+' / '+str(len(pages)))
        cid=d['character'];portrait=self.assets[f'sprites/{cid}_portraits.png']
        self.screen.blit(portrait,(30,78),pygame.Rect(0,0,96,96))
        for i,line in enumerate(pages[index][1]):self.text(line,140,82+i*16,'paper',11)
        if choice:
            self.text('1  Ngồi lại, nghe cho hết.',140,191,'amber',10)
            self.text('2  Kể lại ngay điều vừa nghe.',140,209,'muted',10)
        else:self.text('Enter / E / nhấp để tiếp tục',140,221,'muted',9)
        self.text('Esc để khép cuộc trò chuyện',30,233,'muted',9)
