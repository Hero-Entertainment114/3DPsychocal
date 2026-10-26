from pathlib import Path
import logging
import pygame
from core.content import Content
from core.state import State
from core.paths import ROOT, USER
from systems.progression import Progression, select_ending, ending_fixture
from systems.storage import Storage, SaveError
from systems.world import World
from systems.audio import Audio
from systems.mechanics import Mechanism
from systems.dialogue import choose, eligible, complete
from scenes.render import Renderer, C

class Game:
    MENU=['Bắt đầu hành trình','Tiếp tục','Chọn chương','Thiết lập','Tư liệu / phân cảnh thử','Thực hiện','Thoát']
    def __init__(self,headless=False,user_dir=None):
        pygame.init()
        pygame.display.set_caption('忘れられた声 • The Forgotten Voices | 3DPsychocal')
        self.content=Content()
        self.store=Storage(user_dir or USER,self.content)
        self.settings=self.store.settings()
        self.display=pygame.display.set_mode((960,540),pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load(str(ROOT/'assets/ui/icon.png')))
        self.surface=pygame.Surface((480,270))
        self.render=Renderer(self.surface,self.content)
        self.audio=Audio(self.settings)
        self.running=True;self.mode='menu';self.selection=0;self.time=0.;self.scare=0.
        self.toast='';self.toast_time=0.;self.page=0;self.input='';self.pid=None;self.dialogue=None
        self.dialogue_pages=[];self.dialogue_index=0;self.choice=False
        self.return_mode='menu';self.selected_evidence=[];self.journal_tab=0;self.ending_id='A';self.ending_page=0
        self.hint_visible=False;self.knock_queue=[];self.mechanism=None;self.remap=None;self.step_timer=0.;self.last_scale=(2,0,0)
        self.set_state(State())
        self.menu_progress=0
        if self.store.path('auto').exists():
            try:self.menu_progress=len(self.store.load().solved)
            except SaveError:pass
        if self.settings['fullscreen'] and not headless:self.toggle_fullscreen(persist=False)
        self.audio.music(0)
    def set_state(self,state):
        self.state=state;self.progress=Progression(self.content,state);self.world=World(self.content,state)
    def notify(self,message):self.toast=message;self.toast_time=4
    def save(self,slot='auto'):
        try:
            self.store.save(self.state,slot);self.menu_progress=max(self.menu_progress,len(self.state.solved))
            if slot!='auto':self.notify(f'Đã lưu vào trang {slot}.')
        except (OSError,SaveError) as e:logging.exception('Save failed');self.notify('Không lưu được: '+str(e))
    def load(self,slot='auto'):
        try:
            self.set_state(self.store.load(slot));self.mode='play';self.audio.ambience(self.world.room['ambient']);self.audio.music(self.state.chapter);return True
        except SaveError as e:self.notify(str(e));return False
    def start(self):
        self.set_state(State());self.mode='play';self.audio.ambience('rain');self.audio.music(0)
        self.show_message('Ba ngày ở quê','Tháng 10, 1998. Mẹ nhập viện, hồ sơ căn nhà cần chữ ký. Ren xin nghỉ ba ngày ở công ty vận chuyển. Trong túi là lá thư không người gửi, một bức ảnh bị cào và cassette chưa nghe.\n\nQua sảnh vé ở lối ra cuối sân ga. Quan sát nhãn vé và biển cửa. E để xem đồ vật hoặc nói chuyện. Ghé bệnh viện qua phố chính.\n\nCó âm thanh và chủ đề mất mát. Có thể giảm hiệu ứng trong Thiết lập.','play')
    def show_message(self,title,text,back='play'):
        self.message_title=title;self.message_text=text;self.return_mode=back;self.mode='message';self.page=0
    def open_dialogue(self,cid):
        d=self.content.dialogues.get(cid) if cid.startswith('D_') else choose(self.content,self.state,self.state.room,cid)
        if not d or not eligible(d,self.state):return
        self.dialogue=d;self.dialogue_pages=[]
        for i,l in enumerate(d['lines']):
            wrapped=self.render.wrap(l['text'],305,11)
            for j in range(0,len(wrapped),6):self.dialogue_pages.append((i,wrapped[j:j+6]))
        self.dialogue_index=0;self.choice=False;self.mode='dialogue'
    def next_dialogue(self):
        if self.choice:return
        if self.dialogue_index<len(self.dialogue_pages)-1:self.dialogue_index+=1
        else:
            self.choice=True
    def interact(self):
        o=self.world.nearest()
        if not o:self.notify('Đến gần đồ vật hoặc một người rồi nhấn E.');return
        if o['kind']=='portal':
            if self.world.travel(int(o['id'])):
                self.save();self.audio.ambience(self.world.room['ambient'])
            else:
                gate=self.world.room['portals'][int(o['id'])].get('requires')
                self.notify('Chưa mở lối: '+self.content.puzzles[gate]['title'] if gate else 'Lối này chưa mở.')
        elif o['kind']=='npc':self.open_dialogue(o['dialogue'])
        elif o['kind']=='reflection':self.open_dialogue(o['id'])
        elif o['kind']=='observation':
            note=self.content.observations[o['id']]
            flag='observed_'+o['id']
            if not self.state.flags.get(flag):
                self.state.flags[flag]=True
                self.state.journal.append(note['title']+' — '+note['text'])
                self.save()
            self.show_message(note['title'],note['text'])
        else:self.open_puzzle(o['id'])
    def open_puzzle(self,pid):
        p=self.content.puzzles[pid]
        if pid in self.state.solved:
            self.show_message(p['title'],p['resolution']+'\n\n'+self.state.choices.get(pid,''));return
        if not self.progress.available(pid):
            missing=[self.content.puzzles[x]['title'] for x in p['requires'] if x not in self.state.solved]
            self.show_message(p['title'],'Ren chưa đủ thông tin. Quay lại sau khi tìm hiểu:\n\n'+'\n'.join(missing));return
        self.pid=pid;self.input='';self.mode='puzzle';self.page=0;self.hint_visible=False;self.mechanism=Mechanism(p)
        if pid=='P013':self.knock_queue=[self.time,self.time+.28,self.time+.95]
    def answer(self,assisted=False):
        pid=self.pid;p=self.content.puzzles[pid]
        if self.mechanism is not None and self.mechanism.answer() is not None:self.input=self.mechanism.answer()
        if self.progress.solve(pid,self.input,assisted):
            self.audio.play('chime');self.mode='play';self.save();self.notify('Ren ghi lại: '+p['title'])
            if pid=='P004' and 'D_ren' not in self.state.heard:self.open_dialogue('D_ren')
            if pid=='P008':
                self.audio.music(1);self.show_message('I • Tiếng gõ sau cánh cửa','Yui mở cổng phía Đông. Trường vẫn có mùi phấn ẩm. Ren tự nhủ sẽ chỉ tìm người đã gửi băng, rồi trở về bệnh viện.\n\nLối vào trường nằm cuối phố. Các đồ vật có dấu ! đã đủ điều kiện để tìm hiểu.')
            if pid=='P013':
                self.scare=3.5;self.state.fear=min(70,self.state.fear+20)
                self.notify('Có tiếng chân dừng sau lưng. [cộc cộc — nghỉ — cộc]')
            if pid=='P022':
                self.show_message('Cánh cửa đã được mở','Ren rút chốt, giữ cả hai lời khai và trao bản sao cho Yui. Bên kia không còn tiếng yêu cầu mở cửa. Nhưng trên khăn, tên ấy vẫn chưa thuộc về bất kỳ hồ sơ nào.\n\nHẾT GIAI ĐOẠN CHƠI 0.2\nMở đầu và Hanako đã khép lại. Hai chương đầu có 16 bản đồ. Sáu chương còn lại chưa được triển khai. Bạn có thể trở lại phố, đọc sổ hoặc xem phân cảnh kết thúc thử trong Tư liệu.','play')
        else:
            attempts=self.state.attempts.get(pid,0)
            self.notify('Cần đủ ghi chép và thao tác đúng. H xem gợi ý.'+(' F để bỏ qua câu đố này.' if attempts>=3 else ''))
    def toggle_fullscreen(self,persist=True):
        if persist:self.settings['fullscreen']=not self.settings['fullscreen']
        self.display=pygame.display.set_mode((0,0),pygame.FULLSCREEN) if self.settings['fullscreen'] else pygame.display.set_mode((960,540),pygame.RESIZABLE)
        if persist:self.store.save_settings(self.settings)
    def settings_rows(self):
        s=self.settings
        def yes(k):return 'Bật' if s[k] else 'Tắt'
        return [f"Âm lượng tổng: {int(s['master']*100)}%",f"Nhạc: {int(s['music']*100)}%",f"Hiệu ứng: {int(s['effects']*100)}%",f"Lời thoại*: {int(s['voice']*100)}%",'Giảm xuất hiện bất ngờ: '+yes('reduced_scares'),'Giảm nhấp nháy: '+yes('reduced_flashes'),'Giảm chuyển động: '+yes('reduced_motion'),'Giảm máu*: '+yes('reduced_blood'),'Đường quét CRT: '+yes('crt'),'Toàn màn hình: '+yes('fullscreen'),'Đổi phím tương tác: '+s['keys']['interact'].upper(),'Đổi phím sổ tay: '+s['keys']['journal'].upper(),'Đổi phím túi: '+s['keys']['inventory'].upper(),'Đổi phím ký ức: '+s['keys']['memory'].upper()]
    def adjust_setting(self,delta=1):
        i=self.selection
        if i<4:
            key=('master','music','effects','voice')[i];self.settings[key]=round(max(0,min(1,self.settings[key]+delta*.1)),2)
        elif i<9:
            key=('reduced_scares','reduced_flashes','reduced_motion','reduced_blood','crt')[i-4];self.settings[key]=not self.settings[key]
        elif i==9:self.toggle_fullscreen();return
        else:self.remap=('interact','journal','inventory','memory')[i-10];return
        self.audio.refresh();self.store.save_settings(self.settings)
    def choose_menu(self):
        i=self.selection;self.selection=0
        if i==0:
            if self.store.path('auto').exists():self.mode='new_confirm'
            else:self.start()
        elif i==1:self.load()
        elif i==2:self.mode='chapters'
        elif i==3:self.mode='settings';self.return_mode='menu'
        elif i==4:self.mode='extras'
        elif i==5:self.show_message('Thực hiện & nguồn tài nguyên','Wasurerareta Koe — Những Tiếng Nói Bị Lãng Quên\nBản sản xuất độc lập 0.2. Mã và nội dung gốc: Apache-2.0. Mỹ thuật pixel và âm thanh được tạo bằng công cụ trong repo. Font Noto: SIL OFL.\n\nAlpix: canvas đã mở, không xuất ảnh. AutoSprite: nhân vật đã tạo, chưa có ảnh trả về; không dùng làm sprite runtime.\n\nTsukimori, Kiroku và các sự kiện đều hư cấu. Không coi truyện Inunaki trong game là lịch sử.','menu')
        else:self.running=False
    def handle(self,event):
        if event.type==pygame.QUIT:self.running=False;return
        if event.type==pygame.VIDEORESIZE:
            if not self.settings['fullscreen']:self.display=pygame.display.set_mode((max(480,event.w),max(270,event.h)),pygame.RESIZABLE)
            return
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button in (4,5) and self.mode in ('journal','inventory','message'):self.page=max(0,self.page+(-1 if event.button==4 else 1));return
            if event.button!=1:return
            scale,ox,oy=self.last_scale;mx=(event.pos[0]-ox)/scale;my=(event.pos[1]-oy)/scale
            if self.mode=='menu' and 31<=mx<=228 and 136<=my<242:
                self.selection=min(6,int((my-136)//15));self.choose_menu()
            elif self.mode=='dialogue' and self.choice:
                if 138<=mx<=448 and 187<=my<242:self.finish_dialogue('listen' if my<214 else 'repeat')
            elif self.mode=='dialogue':self.next_dialogue()
            elif self.mode=='play':self.interact()
            return
        if event.type!=pygame.KEYDOWN:return
        key=event.key;name=pygame.key.name(key)
        if self.remap:
            if key==pygame.K_ESCAPE:self.remap=None;return
            reserved={'escape','return','space','w','a','s','d','up','down','left','right','f5','f9','h','f','1','2','3','4','5','6','7','8','9','0'}
            if name in reserved or (name in self.settings['keys'].values() and self.settings['keys'][self.remap]!=name):self.notify('Phím này dành cho điều khiển khác.');return
            self.settings['keys'][self.remap]=name;self.store.save_settings(self.settings);self.remap=None;return
        if self.mode=='play':
            if key==pygame.K_ESCAPE:self.mode='pause';self.selection=0
            elif name==self.settings['keys']['interact']:self.interact()
            elif name==self.settings['keys']['journal']:self.mode='journal';self.page=0;self.selection=0;self.journal_tab=0
            elif name==self.settings['keys']['inventory']:self.mode='inventory';self.page=0
            elif name==self.settings['keys']['memory']:
                if 'P006' not in self.state.solved:self.notify('Cần nghe cassette trước khi nối lại ký ức.')
                else:
                    self.state.memory=not self.state.memory
                    if self.state.room=='school_store' and self.state.memory:self.state.flags['school_memory_seen']=True
                    self.notify('Ký ức • biển phòng và sắc cảnh đã thay đổi.' if self.state.memory else 'Hiện tại')
            elif key==pygame.K_F5:self.mode='save';self.selection=0
            elif key==pygame.K_F9:self.mode='load';self.return_mode='play';self.selection=0
            return
        if self.mode=='menu':
            if key in (pygame.K_DOWN,pygame.K_s):self.selection=(self.selection+1)%len(self.MENU)
            elif key in (pygame.K_UP,pygame.K_w):self.selection=(self.selection-1)%len(self.MENU)
            elif key in (pygame.K_RETURN,pygame.K_SPACE):self.choose_menu()
        elif self.mode=='new_confirm':
            if key==pygame.K_RETURN:self.start()
            elif key==pygame.K_ESCAPE:self.mode='menu'
        elif self.mode=='pause':
            items=6
            if key==pygame.K_ESCAPE:self.mode='play'
            elif key in (pygame.K_UP,pygame.K_DOWN):self.selection=(self.selection+(1 if key==pygame.K_DOWN else -1))%items
            elif key==pygame.K_RETURN:
                i=self.selection;self.selection=0
                if i==0:self.mode='play'
                elif i==1:self.mode='save'
                elif i==2:self.mode='load';self.return_mode='pause'
                elif i==3:self.mode='settings';self.return_mode='pause'
                elif i==4:self.save();self.mode='menu'
                else:self.running=False
        elif self.mode=='dialogue':
            if key==pygame.K_ESCAPE:self.mode='play'
            elif self.choice and key in (pygame.K_1,pygame.K_2):self.finish_dialogue('listen' if key==pygame.K_1 else 'repeat')
            elif not self.choice and (key in (pygame.K_RETURN,pygame.K_SPACE) or name==self.settings['keys']['interact']):self.next_dialogue()
        elif self.mode=='puzzle':
            if key==pygame.K_ESCAPE:self.mode='play'
            elif key==pygame.K_RETURN:self.answer()
            elif key==pygame.K_h:
                self.state.hints[self.pid]=min(3,self.state.hints.get(self.pid,0)+1);self.hint_visible=True
            elif key==pygame.K_TAB:self.hint_visible=False
            elif key==pygame.K_f and self.state.attempts.get(self.pid,0)>=3:self.answer(assisted=True)
            elif self.mechanism is not None and self.mechanism.answer() is not None:
                self.mechanism.key(name)
                if self.mechanism.kind=='rhythm' and name=='space':self.audio.play('knock')
            elif key==pygame.K_BACKSPACE:self.input=self.input[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.input)<48:self.input+=event.unicode
        elif self.mode=='message':
            lines=self.render.wrap(self.message_text,402,11);pages=max(1,(len(lines)+8)//9)
            if key==pygame.K_ESCAPE:self.mode=self.return_mode
            elif key in (pygame.K_RETURN,pygame.K_SPACE):
                if self.page+1<pages:self.page+=1
                else:self.mode=self.return_mode
        elif self.mode in ('inventory','journal'):
            if key==pygame.K_ESCAPE or name==self.settings['keys']['journal'] or name==self.settings['keys']['inventory']:self.mode='play'
            elif self.mode=='journal' and key in (pygame.K_LEFT,pygame.K_RIGHT):self.journal_tab=(self.journal_tab+(1 if key==pygame.K_RIGHT else -1))%5;self.page=0;self.selection=0
            elif key in (pygame.K_DOWN,pygame.K_PAGEDOWN):self.page+=1
            elif key in (pygame.K_UP,pygame.K_PAGEUP):self.page=max(0,self.page-1)
            elif self.mode=='journal' and self.journal_tab==1 and key==pygame.K_SPACE:
                ev=self.state.evidence
                if ev:
                    chosen=ev[min(self.page,len(ev)-1)]
                    if chosen in self.selected_evidence:self.selected_evidence.remove(chosen)
                    elif len(self.selected_evidence)<2:self.selected_evidence.append(chosen)
            elif self.mode=='journal' and key==pygame.K_c and len(self.selected_evidence)==2:
                ok=self.progress.combine(*self.selected_evidence);self.selected_evidence=[];self.notify('Hai nguồn hỗ trợ cùng một kết luận.' if ok else 'Giữ giả thuyết chưa xác nhận. Có thể thử lại.');self.save()
        elif self.mode=='settings':
            if key==pygame.K_ESCAPE:self.mode=self.return_mode;self.selection=0
            elif key in (pygame.K_UP,pygame.K_DOWN):self.selection=(self.selection+(1 if key==pygame.K_DOWN else -1))%len(self.settings_rows())
            elif key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN):self.adjust_setting(-1 if key==pygame.K_LEFT else 1)
        elif self.mode in ('save','load'):
            if key==pygame.K_ESCAPE:self.mode='play' if self.mode=='save' else self.return_mode
            elif key in (pygame.K_1,pygame.K_2,pygame.K_3):
                slot=str(key-pygame.K_0)
                if self.mode=='save':self.save(slot);self.mode='play'
                else:self.load(slot)
            elif key==pygame.K_a and self.mode=='load':self.load()
        elif self.mode=='chapters':
            if key==pygame.K_ESCAPE:self.mode='menu'
            elif key==pygame.K_1:self.start()
            elif key==pygame.K_2:
                if self.load() and 'P008' in self.state.solved:
                    self.state.room='school';self.state.x=64;self.state.y=272;self.world.follow(1)
                else:self.mode='chapters';self.notify('Chương I mở sau khi hoàn thành phần mở đầu.')
        elif self.mode=='extras':
            if key==pygame.K_ESCAPE:self.mode='menu'
            elif key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5):
                self.ending_id='ABCDE'[key-pygame.K_1];self.ending_page=0;self.mode='ending';self.audio.music(6)
        elif self.mode=='ending':
            if key==pygame.K_ESCAPE:self.mode='extras';self.audio.music(self.state.chapter)
            elif key in (pygame.K_RETURN,pygame.K_RIGHT):self.ending_page=min(7,self.ending_page+1)
            elif key==pygame.K_LEFT:self.ending_page=max(0,self.ending_page-1)
    def finish_dialogue(self,choice):
        complete(self.content,self.state,self.dialogue['id'],choice)
        self.mode='play';self.save()
        self.notify('Ren ghi rõ điều đã nghe.' if choice=='listen' else 'Ấn tượng này có thể đổi cách người khác kể lại chuyện.')
    def update(self,dt):
        self.time+=dt;self.toast_time=max(0,self.toast_time-dt)
        if self.mode!='puzzle':self.knock_queue=[]
        while self.knock_queue and self.knock_queue[0]<=self.time:
            self.audio.play('knock');self.knock_queue.pop(0)
        if self.mode=='play':
            self.state.play_seconds+=dt;self.scare=max(0,self.scare-dt)
            self.world.update(dt,pygame.key.get_pressed());self.state.fear=max(0,self.state.fear-dt*1.2)
            if self.world.moving:
                self.step_timer+=dt
                if self.step_timer>.33:self.audio.play('step');self.step_timer=0
        # No world simulation while reading, paused, choosing, or inspecting records.
    def draw_list(self,title,items,selected=0,subtitle='↑ ↓ Chọn • Enter Xác nhận • Esc Trở lại'):
        r=self.render;r.panel(title,subtitle)
        for i,label in enumerate(items):
            y=78+i*23
            if i==selected:pygame.draw.rect(self.surface,C['blue'],(30,y-2,420,22))
            r.text(('› ' if i==selected else '  ')+label,37,y,'amber' if i==selected else 'paper',11)
    def draw(self):
        r=self.render
        if self.mode in ('menu','new_confirm','chapters','extras','ending') or (self.mode in ('settings','message') and self.return_mode=='menu'):
            r.menu(self.MENU,self.selection,self.menu_progress,self.time,self.settings)
        else:r.world(self.world,self.progress,self.time,self.settings,self.scare)
        if self.mode=='new_confirm':
            r.panel('Bắt đầu lại?','Enter Bắt đầu • Esc Trở lại');r.paragraph('Tự động lưu sẽ được thay khi bạn bắt đầu tiến trình mới. Ba trang lưu thủ công vẫn được giữ.',34,88,400)
        elif self.mode=='pause':self.draw_list('Trang đang mở',['Tiếp tục','Lưu vào trang nhật ký','Đọc trang đã lưu','Thiết lập','Về hành lang','Thoát'],self.selection)
        elif self.mode=='dialogue':r.dialogue(self.dialogue,self.dialogue_pages,self.dialogue_index,self.choice)
        elif self.mode=='puzzle':
            p=self.content.puzzles[self.pid];r.panel(p['title'],'Enter Kiểm tra • H Gợi ý • Tab Ẩn gợi ý • Esc Trở lại')
            r.paragraph(p['prompt'],32,73,414,10,lineheight=14,maxlines=3)
            model=self.mechanism
            if model and model.answer() is not None:
                r.mechanism(model)
            else:
                pygame.draw.rect(self.surface,C['blue'],(30,132,420,28))
                r.text('Trả lời: '+self.input,36,138,'paper',12)
            known=sum(bool(self.state.flags.get('observed_'+oid)) for oid in p.get('observations',[]))
            r.text(f'Ghi chép đã xem: {known}/2 • J trong thế giới để đọc lại.',32,192,'muted',9)
            n=self.state.hints.get(self.pid,0)
            if n and self.hint_visible:
                pygame.draw.rect(self.surface,C['ink'],(29,73,422,113))
                r.paragraph(f'Gợi ý {n}/3: '+p['hints'][n-1],32,81,414,11,'amber',16)
                rooms=[self.content.maps[self.content.observations[o]['room']]['name'] for o in p.get('observations',[]) if not self.state.flags.get('observed_'+o)]
                r.paragraph('Tìm ghi chép: '+', '.join(rooms),32,144,414,9,'muted',13,maxlines=3)
            if self.state.attempts.get(self.pid,0)>=3:r.text('F: bỏ qua có ghi nhận • không khóa truyện',32,221,'amber',10)
        elif self.mode=='message':
            r.panel(self.message_title,'Enter Trang tiếp / Khép lại • Esc Khép lại')
            lines=r.wrap(self.message_text,402,11);last=max(0,(len(lines)-1)//9);self.page=min(self.page,last)
            for i,line in enumerate(lines[self.page*9:self.page*9+9]):r.text(line,34,77+i*17,'paper',11)
        elif self.mode=='settings':
            r.panel('Thiết lập','↑ ↓ Chọn • ← → Điều chỉnh • Enter Đổi • Esc Lưu & quay lại')
            rows=self.settings_rows();start=(self.selection//7)*7
            for i,label in enumerate(rows[start:start+7]):
                y=73+i*21
                if start+i==self.selection:pygame.draw.rect(self.surface,C['blue'],(29,y-1,420,21))
                r.text(label,37,y,'amber' if start+i==self.selection else 'paper',10)
            r.text('* Chưa có lồng tiếng / cảnh máu trong bản 0.2. UI: tiếng Việt.',31,226,'muted',9)
            if self.remap:r.text('Nhấn phím mới • Esc Hủy',31,239,'amber',9)
        elif self.mode in ('save','load'):
            r.panel('Lưu nhật ký' if self.mode=='save' else 'Đọc nhật ký','1 / 2 / 3 Chọn trang • A Tự động (đọc) • Esc Quay lại')
            for i,slot in enumerate(('1','2','3')):
                desc='Trang trống'
                if self.store.path(slot).exists():
                    try:
                        s=self.store.load(slot);desc=f'{len(s.solved)}/22 • {self.content.maps[s.room]["name"]}'
                    except SaveError:desc='Tệp lỗi — không tự ghi đè khi đọc'
                r.text(slot+'    '+desc,38,85+i*37,'paper',11)
            r.paragraph('Lưu thủ công ghi đè trang được chọn. Tự động lưu khi giải đố, hoàn thành hội thoại hoặc sang bản đồ.',38,201,396,10,'muted',14)
        elif self.mode=='inventory':
            r.panel('Túi vải của Ren','↑ ↓ Lật trang • Esc / Tab Khép lại')
            items=self.state.inventory;self.page=min(self.page,max(0,(len(items)-1)//5))
            for i,item in enumerate(items[self.page*5:self.page*5+5]):r.text('◇  '+item,40,83+i*26,'paper',11)
            r.paragraph('Vật dụng được dùng theo ngữ cảnh, không bị tiêu hao. Đến gần thiết bị rồi nhấn phím tương tác.',38,216,400,10,'muted',14)
        elif self.mode=='journal':self.draw_journal()
        elif self.mode=='chapters':
            r.panel('Những trang đã mở','1 Mở đầu mới • 2 Tiếp tục ở trường từ autosave • Esc Trở lại')
            r.text('01  Ba ngày ở quê',36,86,'paper',12)
            r.text('02  Tiếng gõ sau cánh cửa',36,118,'amber' if self.menu_progress>=8 else 'muted',12)
            r.paragraph('Chương II–VI và hồi kết chưa có bản đồ chơi được. Các bản thiết kế nằm trong repo; không mở khóa chương rỗng.',36,165,400,11)
        elif self.mode=='extras':
            r.panel('Tư liệu sản xuất • CÓ TIẾT LỘ','1–5 Xem phân cảnh kết thúc thử • Esc Trở lại')
            for i,e in enumerate(self.content.endings.values()):r.text(f'{i+1}  {e["title"]}',36,77+i*23,'paper',11)
            r.paragraph('Đây là bản xem thử độc lập, không phải kết thúc đã kiếm được trong tuyến chơi. Quy tắc kết thúc được kiểm thử bằng trạng thái giả lập.',36,202,400,10,'amber',14)
        elif self.mode=='ending':self.draw_ending()
        if self.toast_time>0:
            lines=r.wrap(self.toast,422,10)[:2];h=len(lines)*14+8
            pygame.draw.rect(self.surface,C['deep'],(22,250-h,436,h));pygame.draw.rect(self.surface,C['fog'],(22,250-h,436,h),1)
            for i,line in enumerate(lines):r.text(line,29,254-h+i*14,'amber',10)
    def draw_journal(self):
        r=self.render;tabs=['Ghi chép','Chứng cứ','Lời đã nói','Quan hệ','Việc đang làm']
        r.panel(tabs[self.journal_tab],'← → Đổi mục • ↑ ↓ Trang • Space Chọn chứng cứ • C Ghép • Esc Khép')
        if self.journal_tab==0:
            records=self.state.journal or ['Chỉ định ở lại ba ngày. Thăm mẹ, mua trà và trở về căn nhà cũ.']
            self.page=min(self.page,len(records)-1);r.paragraph(records[self.page],36,85,402,12,lineheight=18)
        elif self.journal_tab==1:
            records=self.state.evidence
            if not records:r.paragraph('Chưa có tài liệu để đối chiếu. Quan sát đồ vật và ghi lại những điều có thể kiểm tra.',36,85,402)
            else:
                self.page=min(self.page,len(records)-1);ev=records[self.page];p=self.content.puzzles['P'+ev[1:]]
                r.text(ev+' • '+p['title'],36,82,'amber',12);r.paragraph(p['resolution'],36,111,402)
                r.text('Đang ghép: '+' + '.join(self.selected_evidence),36,206,'muted',10)
        elif self.journal_tab==2:
            entries=[(d['lines'][i]['speaker'],d['lines'][i]['text']) for did in self.state.heard for d in [self.content.dialogues[did]] for i in range(len(d['lines']))]
            if entries:
                self.page=min(self.page,len(entries)-1);speaker,text=entries[self.page];r.text(speaker,36,80,'amber',12);r.paragraph(text,36,108,402)
            else:r.text('Những cuộc trò chuyện đã nghe hết sẽ ở đây.',36,88,'muted',10)
        elif self.journal_tab==3:
            records=list(self.state.relations.items())
            if records:
                self.page=min(self.page,len(records)-1);cid,rel=records[self.page]
                r.text(self.content.characters[cid]['name'],36,82,'amber',12)
                r.paragraph('Sẵn sàng ngồi lại với Ren.' if rel['trust']>rel['resentment'] else 'Thận trọng với cách Ren kể chuyện của mình.',36,113,400)
                r.paragraph('Ren chỉ biết cảm nhận của mình; người khác vẫn có quyền không đồng ý hoặc không giúp.',36,178,400,10,'muted',14)
            else:r.text('Chưa có cuộc trò chuyện trọn vẹn.',36,88,'muted',10)
        else:
            unfinished=[p for p in self.content.playable if p['id'] not in self.state.solved and self.progress.available(p['id'])]
            records=unfinished
            if unfinished:
                self.page=min(self.page,len(unfinished)-1);p=unfinished[self.page]
                r.text(p['title'],36,81,'amber',12);r.text('Nơi: '+self.content.maps[p['room']]['name'],36,111,'muted',10)
                r.paragraph(p['hints'][0],36,142,400)
            else:r.paragraph('Phân đoạn đã khép lại. Trở lại gặp những người còn ở thị trấn.',36,88,400)
        r.text(f'Trang {self.page+1} • Fear {int(self.state.fear)} / Guilt {self.state.guilt} / Clarity {self.state.clarity}',36,231,'muted',9)
    def draw_ending(self):
        r=self.render;e=self.content.endings[self.ending_id]
        r.panel(e['title'],'BẢN XEM THỬ • Enter / → Tiếp • ← Lùi • Esc Tư liệu')
        if self.ending_page<3:
            scene=e['scenes'][self.ending_page]
            # Scene-specific miniature, with actors and a differing palette.
            room=scene['location'] if scene['location'] in self.content.maps else 'school'
            thumb=pygame.transform.scale(r.assets[f'maps/{room}.png'],(140,84))
            self.surface.blit(thumb,(31,78));r.sprite('ren',91,150)
            if self.ending_id in 'CDE':r.sprite('mio',129,145,alpha=130)
            r.text(scene['title'],184,79,'amber',12);r.paragraph(scene['text'],184,105,260,11,lineheight=16)
        else:
            start=(self.ending_page-3)*2
            for i,text in enumerate(e['epilogues'][start:start+2]):r.paragraph(text,36,88+i*63,402,11,lineheight=16)
        r.text(f'{self.ending_id} • {self.ending_page+1}/8 • Sixth Name',36,231,'muted',9)
    def present(self):
        w,h=self.display.get_size();scale=max(1,min(w//480,h//270));ox=(w-480*scale)//2;oy=(h-270*scale)//2
        self.last_scale=(scale,ox,oy);self.display.fill(C['ink'])
        self.display.blit(pygame.transform.scale(self.surface,(480*scale,270*scale)),(ox,oy));pygame.display.flip()
    def run(self,frames=0,screenshot=None):
        clock=pygame.time.Clock();count=0
        while self.running:
            dt=min(.05,clock.tick(60)/1000)
            for event in pygame.event.get():self.handle(event)
            self.update(dt);self.draw();self.present();count+=1
            if frames and count>=frames:break
        if screenshot:pygame.image.save(self.surface,str(screenshot))
        # Saving on exit preserves in-progress attempts, memory, and exact location.
        if self.state.solved or self.state.heard or self.state.flags:self.save()
        self.store.save_settings(self.settings)
        pygame.quit()
