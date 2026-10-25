from __future__ import annotations
import argparse,json,math,os,tempfile
from pathlib import Path
from panda3d.core import loadPrcFileData,WindowProperties,TextNode,Vec3,ClockObject
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame,DirectLabel,DirectButton,DirectEntry,DirectSlider
from .core import ROOT,STORY,NOTES,State,Saves,tr
from .locale import ui
from .world import World
from .features import Features

class Game(Features,ShowBase):
 def __init__(self,headless=False,save_dir=None):
  self.headless=headless
  loadPrcFileData('', 'win-size 1280 720\nwindow-title Ben Khong Ten\nsync-video true\nshow-frame-rate-meter false\ntextures-power-2 none\naudio-library-name p3openal_audio')
  if headless:loadPrcFileData('', 'window-type offscreen\nload-display p3headlessgl\naudio-library-name null')
  super().__init__();self.disableMouse();self.camLens.setNearFar(.08,70)
  self.saves=Saves(save_dir);self.config_path=self.saves.path/'settings.json'
  self.settings=dict(language='vi',fov=75.0,volume=.45,sensitivity=.16,bob=False,quality='Low',fullscreen=False,resolution='1280x720',textsize=1.0,fps=60,brightness=1.0,music_volume=.7,ambience_volume=.7,sfx_volume=.7,subtitles=True,bindings={'forward':'w','backward':'s','left':'a','right':'d','interact':'e'})
  try:
   data=json.loads(self.config_path.read_text())
   if not isinstance(data,dict):raise ValueError('settings object required')
   for k,v in data.items():
    if k in self.settings and type(v)==type(self.settings[k]):self.settings[k]=v
  except (OSError,ValueError,TypeError):pass
  if self.settings['language'] not in ('vi','en','ja','zh'):self.settings['language']='vi'
  for key,low,high in [('fov',55,100),('volume',0,1),('sensitivity',.04,.5),('textsize',.8,1.2),('brightness',.6,1.4)]:self.settings[key]=max(low,min(high,self.settings[key]))
  if self.settings['quality'] not in ('Low','Medium','High'):self.settings['quality']='Low'
  if self.settings['resolution'] not in ('1280x720','1600x900','1920x1080'):self.settings['resolution']='1280x720'
  if self.settings['fps'] not in (30,60,120):self.settings['fps']=60
  defaults={'forward':'w','backward':'s','left':'a','right':'d','interact':'e'}
  bindings=self.settings['bindings']
  if set(bindings)!=set(defaults) or any(not isinstance(v,str) or len(v)!=1 or v not in 'abcdefghijklmnopqrstuvwxyz' or v in 'jbm ic'.replace(' ','') for v in bindings.values()) or len(set(bindings.values()))!=5:self.settings['bindings']=defaults
  for key in ('music_volume','ambience_volume','sfx_volume'):self.settings[key]=max(0,min(1,self.settings[key]))
  self.font=self.loader.loadFont(str(ROOT/'assets/fonts/NotoSansCJK-Regular.ttc'))
  if self.font.getNumPages()==0:self.font.setPixelsPerUnit(48)
  self.state=State();self.world=None;self.panel=None;self.running=False;self.keys={};self.target=None;self.elapsed=0;self.step_time=0;self.hints={};self.toast_timer=0
  self.music=self.loader.loadMusic(str(ROOT/'assets/audio/memory.wav'));self.music.setLoop(True);self.music.play()
  self.rain=self.loader.loadSfx(str(ROOT/'assets/audio/rain.wav'));self.rain.setLoop(True)
  self.sounds={n:self.loader.loadSfx(str(ROOT/f'assets/audio/{n}.wav')) for n in ('step','paper','discovery')}
  self.hud=DirectLabel(text='',text_font=self.font,text_scale=.043,text_fg=(.94,.89,.73,1),frameColor=(0,0,0,0),pos=(0,0,.91))
  self.prompt=DirectLabel(text='',text_font=self.font,text_scale=.041,text_fg=(1,.92,.72,1),frameColor=(.04,.06,.05,.8),pos=(0,0,-.82))
  self.toast=DirectLabel(text='',text_font=self.font,text_scale=.039,text_fg=(.9,.83,.6,1),frameColor=(0,0,0,0),pos=(0,0,-.68))
  self.cross=DirectLabel(text='·',text_font=self.font,text_scale=.06,text_fg=(1,1,.8,1),frameColor=(0,0,0,0))
  for key in ('shift','c','arrow_left','arrow_right','arrow_up','arrow_down'):
   self.accept(key,self.key,[key,True]);self.accept(key+'-up',self.key,[key,False])
  for key,fn in [('escape',self.escape),('e',self.interact),('j',self.journal),('b',self.board),('m',self.map_panel),('f5',lambda:self.save('1')),('f9',lambda:self.load('1'))]:self.accept(key,fn)
  self.bind_controls();self.accept('i',self.inventory_panel)
  self.accept('window-event',self.window_event)
  self.load_world();self.apply_settings();self.menu();self.taskMgr.add(self.update,'game-loop')
 def u(self,key):return ui(key,self.settings['language'])
 def t(self,value):return tr(value,self.settings['language'])
 def key(self,key,value):self.keys[key]=value
 def window_event(self,window):
  if not self.headless and window and not window.getProperties().getForeground() and self.running and self.panel is None:self.menu()
 def capture(self,on):
  if self.headless:return
  props=WindowProperties();props.setCursorHidden(on);self.win.requestProperties(props)
  if on:self.win.movePointer(0,self.win.getXSize()//2,self.win.getYSize()//2)
 def load_world(self):
  if self.world:self.world.destroy()
  self.world=World(self);self.world.build(self.state.chapter,self.settings['language']);self.camera.setPos(*self.state.position);self.camera.setHpr(self.state.heading,0,0)
  if not self.world.walkable(self.camera.getX(),self.camera.getY()):self.camera.setPos(0,-8,1.7)
  self.rain.stop()
  if self.state.chapter in (2,4):self.rain.play()
  self.play_theme('chapter'+str(self.state.chapter));self.refresh_hud()
 def refresh_hud(self):
  c=STORY['chapters'][self.state.chapter];self.hud['text']=self.t(c['title'])+'   /   '+self.t(c['place'])
 def apply_settings(self):
  self.camLens.setFov(self.settings['fov']);self.music.setVolume(self.settings['volume']*self.settings['music_volume']*.45);self.rain.setVolume(self.settings['volume']*self.settings['ambience_volume']*.55)
  for s in self.sounds.values():s.setVolume(self.settings['volume']*self.settings['sfx_volume'])
  ClockObject.getGlobalClock().setMode(ClockObject.MLimited);ClockObject.getGlobalClock().setFrameRate(self.settings['fps'])
  self.world.root.setColorScale(*([self.settings['brightness']]*3),1)
  self.camLens.setFar({'Low':40,'Medium':55,'High':70}[self.settings['quality']])
  if not self.headless:
   props=WindowProperties();props.setFullscreen(self.settings['fullscreen']);props.setSize(*map(int,self.settings['resolution'].split('x')));self.win.requestProperties(props)
 def panel_open(self,title):
  self.dragging=None
  if self.panel:self.panel.destroy()
  self.capture(False);self.keys.clear();self.prompt['text']='';self.cross.hide()
  self.panel=DirectFrame(frameColor=(.035,.055,.05,.97),frameSize=(-1.38,1.38,-.95,.95))
  self.label(title,.79,.067,color=(.91,.79,.53,1));self.y=.57
 def label(self,text,y,scale=.043,color=(.89,.87,.78,1),x=0,wrap=55):
  return DirectLabel(parent=self.panel,text=text,text_font=self.font,text_scale=scale*self.settings['textsize'],text_fg=color,text_align=TextNode.ACenter,text_wordwrap=wrap,frameColor=(0,0,0,0),pos=(x,0,y))
 def button(self,text,command,y=None,x=0,width=1.12):
  if y is None:y=self.y;self.y-=.115
  return DirectButton(parent=self.panel,text=text,text_font=self.font,text_scale=.039*self.settings['textsize'],text_fg=(.94,.89,.74,1),frameColor=(.13,.2,.17,1),frameSize=(-width,width,-.045,.055),pos=(x,0,y),command=command,relief=1,pressEffect=True)
 def close(self):
  self.pause_clock=False;self.dragging=None
  if self.panel:self.panel.destroy();self.panel=None
  self.cross.show();self.capture(self.running)
  if self.running and not self.state.ending:self.play_theme('chapter'+str(self.state.chapter))
 def escape(self):
  if self.panel and self.running and not self.state.ending:self.close()
  else:self.menu()
 def menu(self):
  self.pause_clock=True
  self.play_theme('menu')
  self.panel_open(self.u('title'));self.label(self.u('subtitle'),.63,.035);self.y=.43
  if getattr(self,'campaign',None) is not None:self.button(self.u('endreplay'),self.end_replay)
  else:self.button(self.u('chapters'),self.chapters_panel)
  if self.running:self.button(self.u('review') if self.state.ending else self.u('continue'),self.resume)
  elif self.saves.exists():self.button(self.u('continue'),lambda:self.load('auto'))
  self.button(self.u('new'),self.new_confirm)
  self.button(self.u('load'),lambda:self.slots(False))
  if self.running:self.button(self.u('save'),lambda:self.slots(True))
  self.button(self.u('settings'),self.settings_panel)
  self.button(self.u('sidestories'),self.side_stories)
  self.button(self.u('credits'),self.credits)
  self.button(self.u('quit'),self.quit_game)
 def resume(self):
  if self.state.ending:self.ending_panel()
  else:self.close()
 def new_confirm(self):
  self.panel_open(self.u('new'));self.label(self.u('newwarning'),.4);self.button(self.u('start'),self.new_game,-.2);self.button(self.u('back'),self.menu,-.4)
 def new_game(self):
  self.campaign=None;self.state=State();self.running=True;self.hints={};self.load_world();self.save();self.intro()
 def intro(self):
  self.pause_clock=False
  c=STORY['chapters'][self.state.chapter];self.panel_open(self.t(c['title']));self.label(self.t(c['intro']),.45,.043,wrap=52);self.label(self.u('controls'),-.3,.031,wrap=74);self.button(self.u('continue'),self.close,-.74)
 def credits(self):
  self.panel_open(self.u('credits'));self.label('Bến Không Tên / The Nameless Wharf\n'+('Kịch bản hư cấu · Tài nguyên thủ tục nguyên bản\nPanda3D · DejaVu Sans · Apache 2.0\nBản phát triển ngắn, chưa phải bản phát hành 4–6 giờ.' if self.settings['language']=='vi' else 'Original fiction · Original procedural assets\nPanda3D · DejaVu Sans · Apache 2.0\nShort development build; not a 4–6 hour release.'),.5,.04)
  self.label(self.u('controls'),-.05,.035,wrap=65);self.button(self.u('back'),self.menu,-.75)
 def settings_panel(self):
  self.panel_open(self.u('settings'))
  self.button(self.u('language'),self.toggle_language,.58,x=-.65,width=.6)
  self.button(self.u('quality')+': '+({'Low':'Thấp','Medium':'Vừa','High':'Cao'}[self.settings['quality']] if self.settings['language']=='vi' else self.settings['quality']),lambda:self.cycle('quality',['Low','Medium','High']),.58,x=.65,width=.6)
  for key,y,ran in [('fov',.36,(55,100)),('volume',.17,(0,1)),('sensitivity',-.02,(.04,.5)),('brightness',-.21,(.6,1.4))]:
   self.label(self.u(key),y,.035,x=-.75)
   slider=DirectSlider(parent=self.panel,range=ran,value=self.settings[key],pageSize=(ran[1]-ran[0])/20,scale=.55,pos=(.4,0,y))
   slider['command']=lambda k=key,s=slider:self.setting(k,s['value'])
  self.button(self.u('bob')+': '+self.u('on' if self.settings['bob'] else 'off'),lambda:self.cycle('bob',[False,True]),-.4,x=-.65,width=.6)
  self.button(self.u('fullscreen')+': '+self.u('on' if self.settings['fullscreen'] else 'off'),lambda:self.cycle('fullscreen',[False,True]),-.4,x=.65,width=.6)
  self.button(self.settings['resolution'],lambda:self.cycle('resolution',['1280x720','1600x900','1920x1080']),-.54,x=-.65,width=.6)
  self.button(self.u('textsize')+f": {self.settings['textsize']:.1f}",lambda:self.cycle('textsize',[.9,1.0,1.1]),-.54,x=.65,width=.6)
  self.button(self.u('fps')+': '+str(self.settings['fps']),lambda:self.cycle('fps',[30,60,120]),-.68)
  self.button(self.u('sound'),self.sound_settings,-.79,x=-.65,width=.6)
  self.button(self.u('bindings'),self.bindings_panel,-.79,x=.65,width=.6)
  self.button(self.u('back'),self.settings_done,-.91)
 def setting(self,k,v):self.settings[k]=v;self.apply_settings()
 def cycle(self,k,values):self.settings[k]=values[(values.index(self.settings[k])+1)%len(values)];self.apply_settings();self.settings_panel()
 def toggle_language(self):
  langs=['vi','en','ja','zh'];self.settings['language']=langs[(langs.index(self.settings['language'])+1)%len(langs)];self.state.position=list(self.camera.getPos());self.state.heading=self.camera.getH();self.load_world();self.settings_panel()
 def settings_done(self):
  try:self.config_path.write_text(json.dumps(self.settings),encoding='utf8')
  except OSError:self.message(self.u('error'))
  self.menu()
 def message(self,text):self.toast['text']=text;self.toast_timer=6
 def save(self,slot='auto'):
  if self.state.decisions.get('replay'):
   if slot!='auto':self.message(self.u('replaysave'))
   return
  if not self.running:return
  self.state.position=list(self.camera.getPos());self.state.heading=self.camera.getH()
  try:self.saves.save(self.state,slot);self.message(self.u('saved'))
  except (OSError,ValueError):self.message(self.u('error'))
 def load(self,slot):
  self.campaign=None
  try:self.state=self.saves.load(slot)
  except ValueError:self.message(self.u('error'));return
  self.running=True;self.load_world();self.close()
  if self.state.ending:self.ending_panel()
 def slots(self,save):
  self.panel_open(self.u('save' if save else 'load'))
  for i in (['1','2','3'] if save else ['auto','1','2','3']):
   valid=self.saves.exists(i)
   title=('Tự lưu' if self.settings['language']=='vi' else 'Autosave') if i=='auto' else ('Ô ' if self.settings['language']=='vi' else 'Slot ')+i
   if save or valid:self.button(title,lambda s=i:self.save_slot(s) if save else self.load(s))
  self.button(self.u('back'),self.menu,-.75)
 def save_slot(self,slot):self.save(slot);self.menu()
 def note(self,id):
  if id=='draft' and not self.state.decisions.get('cabinet_open'):self.cabinet_panel();return
  self.state.collect(id);self.sounds['paper'].play();self.save();n=NOTES[id];self.panel_open(self.t(n['title']));self.label(self.t(n['body']),.47,.047,wrap=49);self.button(self.u('inspect'),lambda:self.inspect_item(id),-.56);self.button(self.u('close'),self.close,-.73)
 def journal(self,page=0):
  if not self.running:return
  self.panel_open(self.u('journal'));clues=self.state.clues[page*6:page*6+6]
  if not clues:self.label(self.u('allnotes'),.3)
  for id in clues:self.button(self.t(NOTES[id]['title']),lambda n=id:self.note(n))
  if page>0:self.button('←',lambda:self.journal(page-1),-.45,x=-.65,width=.3)
  if len(self.state.clues)>(page+1)*6:self.button('→',lambda:self.journal(page+1),-.45,x=.65,width=.3)
  self.button(self.u('revisit'),self.revisit,-.6);self.button(self.u('close'),self.close,-.77)
 def revisit(self):
  self.panel_open(self.u('revisit'))
  for i in range(self.state.chapter+1):self.button(STORY['chapters'][i]['npc']['name'],lambda n=i:self.dialogue(n))
  self.button(self.u('back'),self.journal,-.75)
 def board(self):
  if not self.running:return
  self.panel_open(self.u('board'))
  for p in STORY['chapters'][self.state.chapter]['puzzles']:
   mark='✓ ' if p['id'] in self.state.solved else '◇ '
   self.button(mark+self.t(p['title']),lambda item=p:self.puzzle(item))
  self.label(self.u('inventory')+': '+str(len(self.state.clues)),0,.035)
  self.button(self.u('links'),self.links_panel,-.35);self.button(self.u('close'),self.close,-.75)
 def puzzle(self,p):
  self.panel_open(self.t(p['title']));pid=p['id']
  if pid in self.state.solved:self.label(self.t(p['reveal']),.42,.044);self.button(self.u('back'),self.board,-.75);return
  if not self.state.ready(pid):
   self.label(self.u('missing'),.4);self.label(self.u('required')+':\n'+'\n'.join(self.t(NOTES[n]['title']) for n in p['requires']),.15,.04);self.button(self.u('back'),self.board,-.75);return
  self.label(self.t(p['prompt']),.5,.044,wrap=51)
  if p['kind']=='sequence':self.sequence_panel(p);return
  if p['kind']=='code':
   entry=DirectEntry(parent=self.panel,text_font=self.font,scale=.065,pos=(-.42,0,.1),width=13,numLines=1,focus=1,command=lambda answer:self.answer(p,answer))
   self.button(self.u('submit'),lambda:self.answer(p,entry.get()),-.1)
  else:
   for i,option in enumerate(p['options']):self.button(self.t(option),lambda a=i:self.answer(p,a),.19-i*.15)
  self.button(self.u('hint'),lambda:self.hint(p),-.4);self.hint_label=self.label('',-.53,.034,wrap=65);self.button(self.u('back'),self.board,-.83)
 def hint(self,p):
  level=self.hints.get(p['id'],0);self.hint_label['text']=self.t(p['hints'][min(level,1)]);self.hints[p['id']]=level+1
 def answer(self,p,answer):
  if self.state.solve(p['id'],answer):self.sounds['discovery'].play();self.save();self.puzzle(p)
  else:self.hint_label['text']=self.u('wrong')
 def dialogue(self,index):
  if index==5:
   self.panel_open('Nhi');self.label(self.t(NOTES['nhi']['body']),.4);self.button(self.u('close'),self.close,-.75);return
  npc=STORY['chapters'][index]['npc'];self.panel_open(npc['name']);self.label(self.t(npc['role']),.62,.033);self.label(self.t(npc['line']),.42,.043,wrap=53)
  self.button(self.u('topics'),lambda:self.conversation_topics(index),-.22)
  self.button(self.u('consent'),lambda:self.consent(index),-.38)
  self.button(self.u('rush'),lambda:self.private_notes(index),-.53);self.button(self.u('close'),self.close,-.75)
 def consent(self,index):
  if index not in self.state.consent:self.state.consent.append(index)
  self.state.decisions[str(index)]='approval';self.save();self.message(self.u('consented'));self.close()
 def private_notes(self,index):self.state.decisions[str(index)]='private';self.save();self.close()
 def map_panel(self):
  if not self.running:return
  self.panel_open(self.u('map'));self.label(self.t(STORY['chapters'][self.state.chapter]['place']),.62,.035)
  for target in self.world.targets:
   x,y,_=target['pos'];px=x*.07;py=y*.043-.05
   self.label('◇',py,.03,x=px);self.label(target['label'],py-.045,.021,x=px,wrap=20)
  self.label('●',self.camera.getY()*.043-.05,.04,x=self.camera.getX()*.07,color=(1,.65,.3,1));self.button(self.u('close'),self.close,-.82)
 def interact(self):
  if not self.running or self.panel or not self.target:return
  t=self.target
  if t['kind']=='note':self.note(t['id'])
  elif t['kind']=='npc':self.dialogue(t['id'])
  elif t['kind']=='board':self.board()
  elif t['kind']=='exit':self.next_chapter()
 def next_chapter(self):
  if not self.state.complete():self.message(self.u('blocked'));return
  if self.state.chapter==4:self.final_choice();return
  self.state.advance();self.load_world();self.save();self.intro()
 def final_choice(self):
  self.panel_open(self.u('ending'));self.label(self.t(NOTES['lan']['body']),.49,.042)
  for i,key in enumerate(('silence','alone','together')):self.button(self.u(key),lambda k=key:self.finish(k),-.07-i*.16)
  self.button(self.u('close'),self.close,-.78)
 def finish(self,key):
  if self.state.finish(key):self.save();self.ending_panel()
  else:self.message(self.u('needconsent'))
 def ending_panel(self):
  self.play_theme('ending_'+self.state.ending)
  self.panel_open(self.u('title'));self.label(self.t(STORY['endings'][self.state.ending]),.46,.046,wrap=49);self.button(self.u('back'),self.menu,-.75)
 def update(self,task):
  dt=min(ClockObject.getGlobalClock().getDt(),.05);self.elapsed+=dt;self.world.tick(dt,self.elapsed);self.feature_tick(dt)
  if self.running and not self.state.ending and not getattr(self,'pause_clock',False):self.state.play_seconds+=dt
  self.toast_timer-=dt
  if self.toast_timer<0:self.toast['text']=self.u('raincaption' if self.state.chapter in (2,4) else 'musiccaption') if self.running and self.settings['subtitles'] and self.panel is None else ''
  if not self.running or self.panel:return task.cont
  h=self.camera.getH();p=self.camera.getP()
  if not self.headless:
   ptr=self.win.getPointer(0);cx=self.win.getXSize()//2;cy=self.win.getYSize()//2
   if ptr.getInWindow():
    h-=(ptr.getX()-cx)*self.settings['sensitivity'];p-=(ptr.getY()-cy)*self.settings['sensitivity'];self.win.movePointer(0,cx,cy)
  h+=(self.keys.get('arrow_left',False)-self.keys.get('arrow_right',False))*90*dt
  p+=(self.keys.get('arrow_up',False)-self.keys.get('arrow_down',False))*70*dt;self.camera.setHpr(h,max(-75,min(75,p)),0)
  forward=self.keys.get('w',False)-self.keys.get('s',False);side=self.keys.get('d',False)-self.keys.get('a',False)
  speed=1.5 if self.keys.get('c') else 4.5 if self.keys.get('shift') else 2.7
  angle=math.radians(h);dx=(-math.sin(angle)*forward+math.cos(angle)*side);dy=(math.cos(angle)*forward+math.sin(angle)*side);length=max(1,math.hypot(dx,dy));dx*=speed*dt/length;dy*=speed*dt/length
  x,y=self.camera.getX(),self.camera.getY()
  if self.world.walkable(x+dx,y):x+=dx
  if self.world.walkable(x,y+dy):y+=dy
  bob=math.sin(self.elapsed*9)*.025 if self.settings['bob'] and (forward or side) else 0
  self.camera.setPos(x,y,(1.05 if self.keys.get('c') else 1.7)+bob)
  if forward or side:
   self.step_time-=dt
   if self.step_time<0:self.sounds['step'].play();self.step_time=.35 if speed>3 else .5
  self.target=None;best=.86;direction=self.camera.getQuat(self.render).getForward()
  for target in self.world.targets:
   delta=Vec3(*target['pos'])-self.camera.getPos();distance=delta.length()
   if .1<distance<3.3:
    score=direction.dot(delta/distance)
    if score>best:self.target=target;best=score
  self.prompt['text']=('['+self.settings['bindings']['interact'].upper()+'] '+('Tương tác' if self.settings['language']=='vi' else 'Interact'))+' · '+self.target['label'] if self.target else 'WASD · E · J · B · M · Esc'
  return task.cont
 def quit_game(self):
  self.save();self.settings_done();self.userExit()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');parser.add_argument('--screenshot');args=parser.parse_args()
 if args.smoke:
  with tempfile.TemporaryDirectory() as tmp:
   game=Game(headless=True,save_dir=tmp);game.new_game();game.close()
   for _ in range(5):game.taskMgr.step()
   if args.screenshot:game.win.saveScreenshot(args.screenshot)
   print('SMOKE OK: 1280x720 frame rendered, world and bilingual font loaded')
   game.destroy()
 else:Game().run()
if __name__=='__main__':main()
