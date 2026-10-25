"""Playable production features layered onto the existing campaign."""
from panda3d.core import LineSegs,TextureStage
from direct.gui.DirectGui import DirectButton,DirectLabel,DirectSlider,DirectEntry
from direct.gui import DirectGuiGlobals as DGG
from .core import STORY,NOTES
from .investigation import connect,chapter_snapshot
from .world import CUBE

class Features:
 def sequence_panel(self,p,order=None):
  order=[] if order is None else order
  self.panel_open(self.t(p['title']));self.label(self.t(p['prompt']),.54,.042)
  self.label(' → '.join(str(i+1) for i in order) or '—',.32,.052)
  for i,o in enumerate(p['options']):
   if i not in order:self.button(str(i+1)+'. '+self.t(o),lambda n=i:self.sequence_panel(p,order+[n]),.13-i*.14)
  self.button(self.u('reset'),lambda:self.sequence_panel(p),-.36,x=-.67,width=.55)
  self.button(self.u('submit'),lambda:self.answer(p,''.join(map(str,order))),-.36,x=.67,width=.55)
  self.button(self.u('hint'),lambda:self.hint(p),-.5);self.hint_label=self.label('',-.63,.033)
  self.button(self.u('back'),self.board,-.83)
 def inspect_item(self,id):
  if id not in self.state.clues:return
  if id not in self.state.inspected:self.state.inspected.append(id)
  self.save();self.panel_open(self.u('inspect')+' · '+self.t(NOTES[id]['title']))
  self.inspect_model=self.panel.attachNewNode(CUBE.makeCopy());self.inspect_model.setPos(-.64,-.2,.04);self.inspect_model.setScale(.7,.025,.85)
  self.inspect_model.setTexture(self.world.textures['paper']);self.inspect_model.setHpr(15,0,8);self.inspect_model.setLightOff()
  self.label(self.t(NOTES[id]['body']),.42,.033,x=.57,wrap=28)
  self.button('↶',lambda:self.rotate_item(-25),-.55,x=-.9,width=.24)
  self.button('↷',lambda:self.rotate_item(25),-.55,x=-.35,width=.24)
  self.button(self.u('flip'),lambda:self.inspect_model.setP(self.inspect_model.getP()+180),-.55,x=.4,width=.36)
  self.button(self.u('back'),lambda:self.note(id),-.8)
 def rotate_item(self,amount):self.inspect_model.setH(self.inspect_model.getH()+amount)
 def inventory_panel(self,page=0):
  if not self.running:return
  self.panel_open(self.u('inventory'))
  for id in self.state.clues[page*6:page*6+6]:self.button(self.t(NOTES[id]['title']),lambda n=id:self.inspect_item(n))
  if not self.state.clues:self.label(self.u('allnotes'),.3)
  if page:self.button('←',lambda:self.inventory_panel(page-1),-.43,x=-.5,width=.3)
  if len(self.state.clues)>6*(page+1):self.button('→',lambda:self.inventory_panel(page+1),-.43,x=.5,width=.3)
  self.button(self.u('close'),self.close,-.79)
 def links_panel(self,page=0):
  if not self.running:return
  self.panel_open(self.u('links'));self.link_page=page;self.link_first=getattr(self,'link_first',None);self.pin_nodes={};self.dragging=None
  self.label(self.u('linkhelp'),.62,.031,wrap=72)
  positions=self.state.decisions.setdefault('pin_positions',{})
  for i,id in enumerate(self.state.clues[page*8:page*8+8]):
   x,z=positions.get(id,[-.92+(i%4)*.61,.3-(i//4)*.43])
   pin=DirectButton(parent=self.panel,text=self.t(NOTES[id]['title']),text_font=self.font,text_scale=.029,text_wordwrap=16,text_fg=(.95,.89,.73,1),frameColor=(.18,.25,.2,1),frameSize=(-.27,.27,-.13,.1),pos=(x,-.1,z),command=lambda n=id:self.select_pin(n))
   handle=DirectLabel(parent=pin,text='• • •',text_font=self.font,text_scale=.027,frameColor=(.35,.35,.23,1),frameSize=(-.27,.27,-.02,.025),pos=(0,-.01,.13))
   handle.bind(DGG.B1PRESS,lambda event,n=id:self.begin_drag(n));handle.bind(DGG.B1RELEASE,lambda event:self.end_drag())
   self.pin_nodes[id]=pin
  self.link_status=self.label(self.t(NOTES[self.link_first]['title']) if self.link_first else '',-.46,.031,wrap=72);self.draw_links()
  if page:self.button('←',lambda:self.links_panel(page-1),-.61,x=-.75,width=.3)
  if len(self.state.clues)>8*(page+1):self.button('→',lambda:self.links_panel(page+1),-.61,x=.75,width=.3)
  self.button(self.u('alllinks'),self.link_list,-.61,width=.4)
  self.button(self.u('close'),self.close,-.81)
 def begin_drag(self,id):self.dragging=id
 def end_drag(self):
  self.dragging=None;self.save()
 def feature_tick(self,dt):
  if getattr(self,'dragging',None) and self.panel and self.mouseWatcherNode.hasMouse():
   m=self.mouseWatcherNode.getMouse();x=max(-1.04,min(1.04,m.x*self.getAspectRatio()));z=max(-.28,min(.38,m.y))
   self.pin_nodes[self.dragging].setPos(x,-.1,z);self.state.decisions['pin_positions'][self.dragging]=[x,z];self.draw_links()
 def select_pin(self,id):
  if self.link_first is None:self.link_first=id;self.link_status['text']=self.t(NOTES[id]['title']);return
  result=connect(self.state,self.link_first,id);self.link_first=None
  self.link_status['text']=self.t(result) if result else self.u('unproven');self.draw_links();self.save()
 def draw_links(self):
  if getattr(self,'lines',None) and not self.lines.isEmpty():self.lines.removeNode()
  seg=LineSegs();seg.setThickness(2);seg.setColor(.85,.62,.32,1)
  for a,b in self.state.links:
   if a in self.pin_nodes and b in self.pin_nodes:
    pa=self.pin_nodes[a].getPos();pb=self.pin_nodes[b].getPos();seg.moveTo(pa.x,0,pa.z);seg.drawTo(pb.x,0,pb.z)
  self.lines=self.panel.attachNewNode(seg.create())
 def link_list(self):
  self.panel_open(self.u('alllinks'))
  text='\n\n'.join(self.t(NOTES[a]['title'])+' ↔ '+self.t(NOTES[b]['title']) for a,b in self.state.links)
  self.label(text or self.u('unproven'),.53,.035,wrap=60);self.button(self.u('back'),self.links_panel,-.8)
 def chapters_panel(self):
  self.panel_open(self.u('chapters'))
  unlocked=self.state.chapter if self.running else 0
  if not self.running:
   try:unlocked=self.saves.load().chapter
   except ValueError:pass
  for i in range(unlocked+1):self.button(self.t(STORY['chapters'][i]['title']),lambda n=i:self.start_replay(n))
  self.label(self.u('replaynotice'),-.3,.032,wrap=65);self.button(self.u('back'),self.menu,-.8)
 def start_replay(self,index):
  if getattr(self,'campaign',None) is None:self.campaign=self.state if self.running else self.saves.load()
  self.state=chapter_snapshot(self.campaign,index);self.running=True;self.load_world();self.intro()
 def end_replay(self):
  self.state=self.campaign;self.campaign=None;self.load_world();self.menu()
 def sound_settings(self):
  self.panel_open(self.u('sound'))
  for key,y in [('music_volume',.48),('ambience_volume',.23),('sfx_volume',-.02)]:
   self.label(self.u(key),y,.037,x=-.75)
   slider=DirectSlider(parent=self.panel,range=(0,1),value=self.settings[key],pageSize=.05,scale=.54,pos=(.42,0,y))
   slider['command']=lambda k=key,s=slider:self.setting(k,s['value'])
  self.button(self.u('subtitles')+': '+self.u('on' if self.settings['subtitles'] else 'off'),self.toggle_subtitles,-.3)
  self.button(self.u('back'),self.settings_done,-.78)
 def toggle_subtitles(self):self.settings['subtitles']=not self.settings['subtitles'];self.sound_settings()
 def bindings_panel(self):
  self.panel_open(self.u('bindings'))
  for i,action in enumerate(('forward','backward','left','right','interact')):
   self.button(self.u('action_interact' if action=='interact' else action)+': '+self.settings['bindings'][action].upper(),lambda a=action:self.change_binding(a),.5-i*.15)
  self.button(self.u('back'),self.settings_done,-.8)
 def change_binding(self,action):
  self.panel_open(self.u('bindings'));self.label(self.u('bindinghelp'),.46,.04)
  entry=DirectEntry(parent=self.panel,text_font=self.font,scale=.07,width=4,pos=(-.15,0,.1),focus=1)
  self.bind_error=self.label('',-.42,.034)
  self.button(self.u('submit'),lambda:self.apply_binding(action,entry.get()),-.2)
  self.button(self.u('back'),self.bindings_panel,-.8)
 def apply_binding(self,action,key):
  key=key.strip().lower()
  # A/D/S/W are permitted only if they are not bound to another action.
  reserved=set('jbm ic'.replace(' ',''))
  if len(key)!=1 or key not in 'abcdefghijklmnopqrstuvwxyz' or key in reserved or key in [v for k,v in self.settings['bindings'].items() if k!=action]:
   self.bind_error['text']=self.u('bindinginvalid');return
  self.settings['bindings'][action]=key;self.bind_controls();self.bindings_panel()
 def bind_controls(self):
  for key in getattr(self,'bound_keys',[]):self.ignore(key);self.ignore(key+'-up')
  self.bound_keys=list(self.settings['bindings'].values())
  for action,canonical in [('forward','w'),('backward','s'),('left','a'),('right','d')]:
   key=self.settings['bindings'][action];self.accept(key,self.key,[canonical,True]);self.accept(key+'-up',self.key,[canonical,False])
  self.accept(self.settings['bindings']['interact'],self.interact)
 def play_theme(self,name):
  if getattr(self,'theme',None)==name:return
  from .core import ROOT
  if getattr(self,'music',None):self.music.stop()
  self.theme=name;self.music=self.loader.loadMusic(str(ROOT/f'assets/audio/{name}.wav'));self.music.setLoop(True)
  self.music.setVolume(self.settings['volume']*self.settings['music_volume']*.45);self.music.play()
 def cabinet_panel(self):
  self.panel_open(self.u('cabinet'));self.label(self.u('cabinetstory'),.45,.043)
  if 'tin' in self.state.solved:self.button(self.u('usekey'),self.unlock_cabinet,-.2)
  else:self.label(self.u('nokey'),-.2)
  self.button(self.u('close'),self.close,-.78)
 def unlock_cabinet(self):
  if 'tin' not in self.state.solved:return
  self.state.decisions['cabinet_open']=True
  if getattr(self.world,'draft_paper',None):self.world.draft_paper.show()
  if getattr(self.world,'drawer',None):self.world.drawer.posInterval(.6,(-5,6.45,.98)).start()
  self.save();self.close()
 def conversation_topics(self,index):
  import json
  from .core import ROOT
  self.topics=json.loads((ROOT/'data/dialogues.json').read_text(encoding='utf8'))
  self.panel_open(STORY['chapters'][index]['npc']['name'])
  for topic in self.topics[index]:
   mark='✓ ' if topic['id'] in self.state.decisions.get('topics',[]) else ''
   self.button(mark+self.t(topic['title']),lambda t=topic:self.conversation_answer(index,t))
  self.button(self.u('back'),lambda:self.dialogue(index),-.8)
 def conversation_answer(self,index,topic):
  seen=self.state.decisions.setdefault('topics',[])
  if topic['id'] not in seen:seen.append(topic['id'])
  self.save();self.panel_open(self.t(topic['title']))
  self.label(self.t(topic['question']),.54,.036,wrap=59,color=(.85,.71,.5,1))
  self.label(self.t(topic['answer']),.26,.042,wrap=52)
  self.button(self.u('back'),lambda:self.conversation_topics(index),-.78)
 def side_stories(self):
  import json
  from .core import ROOT
  self.side_data=json.loads((ROOT/'data/side_stories.json').read_text(encoding='utf8'))
  self.panel_open(self.u('sidestories'))
  for story in self.side_data:
   if self.running and self.state.chapter>=story['unlock']:self.button(self.t(story['title']),lambda s=story:self.side_step(s))
  if not self.running or self.state.chapter<1:self.label(self.u('side_locked'),.3)
  self.button(self.u('back'),self.menu,-.8)
 def side_step(self,story):
  progress=self.state.decisions.setdefault('side_progress',{}).get(story['id'],0)
  if progress>=len(story['steps']):
   self.panel_open(self.t(story['title']));self.label(self.t(story['steps'][-1]['reveal']),.42,.041);self.button(self.u('back'),self.side_stories,-.8);return
  item=story['steps'][progress];self.panel_open(self.t(item['title']));self.label(self.t(item['body']),.54,.035,wrap=65);self.label(self.t(item['question']),.12,.035)
  for i,option in enumerate(item['options']):self.button(self.t(option),lambda a=i:self.side_answer(story,progress,a),-.09-i*.15)
  self.side_feedback=self.label('',-.59,.033);self.button(self.u('back'),self.side_stories,-.81)
 def side_answer(self,story,index,answer):
  item=story['steps'][index]
  if answer!=item['answer']:self.side_feedback['text']=self.u('wrong');return
  self.state.decisions.setdefault('side_progress',{})[story['id']]=index+1;self.save();self.panel_open(self.t(item['title']));self.label(self.t(item['reveal']),.42,.042)
  self.button(self.u('continue'),lambda:self.side_step(story),-.5)
