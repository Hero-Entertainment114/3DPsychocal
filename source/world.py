import math, random
from panda3d.core import (GeomVertexData,GeomVertexFormat,GeomVertexWriter,GeomTriangles,Geom,GeomNode,TextNode,AmbientLight,DirectionalLight,Vec4,Fog,TransparencyAttrib)
from .core import ROOT,STORY,tr

def mesh(name,vertices,faces):
 data=GeomVertexData(name,GeomVertexFormat.getV3n3t2(),Geom.UHStatic)
 v=GeomVertexWriter(data,'vertex');n=GeomVertexWriter(data,'normal');uv=GeomVertexWriter(data,'texcoord');tri=GeomTriangles(Geom.UHStatic)
 from panda3d.core import Vec3
 index=0
 for face in faces:
  a,b,c=[Vec3(*vertices[i]) for i in face[:3]];normal=(b-a).cross(c-a).normalized()
  for j,point in enumerate(face):v.addData3(*vertices[point]);n.addData3(normal);uv.addData2([(0,0),(1,0),(1,1),(0,1)][j%4])
  for j in range(1,len(face)-1):tri.addVertices(index,index+j,index+j+1)
  index+=len(face)
 geom=Geom(data);geom.addPrimitive(tri);node=GeomNode(name);node.addGeom(geom);return node
CUBE=mesh('box',[(-.5,-.5,-.5),(.5,-.5,-.5),(.5,.5,-.5),(-.5,.5,-.5),(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
def roundmesh():
 vertices=[];faces=[]
 for z,r in [(0,1),(1,1)]:
  for i in range(12):vertices.append((r*math.cos(i*math.tau/12),r*math.sin(i*math.tau/12),z))
 for i in range(12):j=(i+1)%12;faces.append((i,j,j+12,i+12))
 faces.extend([tuple(range(11,-1,-1)),tuple(range(12,24))]);return mesh('cylinder',vertices,faces)
ROUND=roundmesh()
class World:
 def __init__(self,app):
  self.app=app;self.root=app.render.attachNewNode('world');self.blocks=[];self.targets=[];self.people=[];self.fans=[];self.rain=None
  self.textures={n:app.loader.loadTexture(str(ROOT/f'assets/textures/{n}.png')) for n in ('wood','tile','plaster','concrete','paper','roof')}
 def destroy(self):self.root.removeNode()
 def box(self,pos,size,mat='wood',color=(1,1,1,1),solid=False):
  node=self.root.attachNewNode(CUBE.makeCopy());node.setPos(*pos);node.setScale(*size);node.setTexture(self.textures[mat]);node.setColor(*color)
  if solid:self.blocks.append((pos[0]-size[0]/2,pos[0]+size[0]/2,pos[1]-size[1]/2,pos[1]+size[1]/2))
  return node
 def cylinder(self,pos,scale,color):
  n=self.root.attachNewNode(ROUND.makeCopy());n.setPos(*pos);n.setScale(*scale);n.setColor(*color);return n
 def sign(self,text,pos,size=.22):
  t=TextNode('sign');t.setText(text);t.setFont(self.app.font);t.setAlign(TextNode.ACenter);t.setTextColor(.89,.84,.65,1)
  node=self.root.attachNewNode(t);node.setPos(*pos);node.setScale(size);return node
 def table(self,x,y):
  self.box((x,y,.83),(2,1.1,.13),solid=True)
  for dx in (-.8,.8):
   for dy in (-.4,.4):self.box((x+dx,y+dy,.4),(.09,.09,.8))
 def chair(self,x,y):
  self.box((x,y,.45),(.65,.65,.12),solid=True);self.box((x,y+.3,.85),(.65,.08,.7))
  for dx in (-.25,.25):
   for dy in (-.25,.25):self.box((x+dx,y+dy,.23),(.07,.07,.46))
 def npc(self,x,y,name,index):
  skin=(.64,.45,.30,1);cloth=[(.32,.42,.34,1),(.67,.61,.47,1),(.27,.35,.42,1),(.55,.56,.52,1),(.52,.29,.25,1)][index%5]
  parent=self.root.attachNewNode('person');parent.setPos(x,y,0)
  for px,py,pz,scale,col in [(0,0,.7,(.28,.17,.6),cloth),(0,0,1.3,(.17,.16,.3),skin),(-.16,0,0,(.09,.1,.7),(.18,.2,.21,1)),(.16,0,0,(.09,.1,.7),(.18,.2,.21,1)),(-.35,0,.7,(.07,.07,.55),skin),(.35,0,.7,(.07,.07,.55),skin)]:
   n=self.cylinder((0,0,0),scale,col);n.reparentTo(parent);n.setPos(px,py,pz)
  # Hair and eyes give each low-poly figure a readable face.
  n=self.cylinder((0,0,0),(.18,.17,.08),(.12,.12,.1,1));n.reparentTo(parent);n.setPos(0,0,1.57)
  for dx in (-.065,.065):
   n=self.box((0,0,0),(.025,.015,.025),'wood',(.08,.07,.06,1));n.reparentTo(parent);n.setPos(dx,-.16,1.48)
  self.blocks.append((x-.4,x+.4,y-.3,y+.3));self.people.append(parent)
  self.targets.append(dict(kind='npc',id=index,pos=(x,y,1.3),label=name))
 def plant(self,x,y):
  self.cylinder((x,y,0),(.3,.3,.45),(.5,.26,.15,1))
  for i in range(5):
   a=i*math.tau/5;n=self.box((x+math.cos(a)*.2,y+math.sin(a)*.2,.75),(.12,.55,.06),'plaster',(.35,.6,.3,1));n.setHpr(i*72,35,0)
 def build(self,index,lang):
  c=STORY['chapters'][index];self.index=index
  self.box((0,0,-.15),(25,26,.3),'tile' if index in (0,1) else 'concrete')
  # Boundary walls; a single neighbourhood-scale area is resident at a time.
  for pos,size in [((-12,0,2),(.35,26,4)),((12,0,2),(.35,26,4)),((0,12.5,2),(24,.35,4)),((0,-12.5,.5),(24,.35,1))]:self.box(pos,size,'plaster',solid=True)
  # Rear veranda and corrugated roofing, wood posts, windows and shutters.
  roof=self.box((0,9,3.9),(23,6,.18),'roof');roof.setP(-8)
  for x in (-10,-5,5,10):self.box((x,7,1.8),(.17,.17,3.6),'wood',solid=True)
  for x in (-8,-3,3,8):
   self.box((x,12.25,2.1),(2.4,.12,1.6),'wood');self.box((x,12.15,2.1),(2.1,.1,1.3),'roof',(.45,.6,.62,1))
   for dx in (-.7,0,.7):self.box((x+dx,12.02,2.1),(.06,.1,1.4),'wood')
  self.sign(tr(c['place'],lang).upper(),(0,12.0,3.2),.34)
  # Laundry line / cable and laundry, shade trees, domestic objects.
  self.box((-8,1,3),(.035,15,.035),'roof')
  for y in (-4,-2,0):self.box((-8,y,2.5),(.04,1,.95),'plaster',(.7,.75,.8,1))
  for x,y in [(-10,-9),(10,-9),(-10,5),(10,5)]:self.plant(x,y)
  for x,y in [(-10,-4),(10,2)]:
   self.cylinder((x,y,0),(.16,.16,3.7),(.35,.25,.17,1))
   for dx,dy,z in [(-.6,0,3.1),(.5,.3,3.7),(0,-.4,4.2)]:self.cylinder((x+dx,y+dy,z),(.9,.9,.8),(.3,.42,.22,1))
  # Ceiling fan animated in every covered room.
  self.box((0,9,3.35),(.08,.08,1),'roof');fan=self.root.attachNewNode('fan');fan.setPos(0,9,2.9)
  for a in range(3):
   n=self.box((0,0,0),(.12,1.8,.035),'roof');n.reparentTo(fan);n.setH(a*120)
  self.fans.append(fan)
  # Three physical evidence stations, each with a visible paper and desk lamp.
  stations=[(-5,-1),(5,1),(-5,7)]
  for n,(x,y) in zip(c['notes'],stations):
   self.table(x,y);self.chair(x,y+1)
   paper=self.box((x,y,.93),(.55,.4,.025),'paper')
   if n['id']=='draft':self.draft_paper=paper
   self.cylinder((x+.65,y,.91),(.04,.04,.4),(.25,.29,.25,1));self.cylinder((x+.65,y,1.3),(.17,.17,.1),(.85,.65,.3,1))
   self.targets.append(dict(kind='note',id=n['id'],pos=(x,y,1.05),label=tr(n['title'],lang)))
  self.table(4,7);self.box((4,7,1.02),(1.5,.6,.1),'paper')
  self.targets.append(dict(kind='board',id='board',pos=(4,7,1.1),label=self.app.u('desk')))
  self.npc(1,5,c['npc']['name'],index)
  self.targets.append(dict(kind='exit',id='exit',pos=(9,10,1.4),label=self.app.u('exit')))
  self.box((9,11,1.3),(1.8,.2,2.6),'wood',solid=True);self.sign('→',(9,10.85,2),.7)
  # Individual chapter architecture and props.
  if index==0:
   for x in (-3,0,3):self.chair(x,-5)
   self.table(-5,-6);self.cylinder((-5,-6,.91),(.16,.16,.2),(.7,.72,.62,1))
   # Bicycle with thin 12-sided wheel outlines and metal frame.
   for y in (3,4.5):
    for i in range(12):
     a=i*math.tau/12;n=self.box((9,y+math.cos(a)*.45,.6+math.sin(a)*.45),(.045,.25,.045),'roof');n.setP(-i*30)
   self.box((9,3.8,.9),(.06,1,.06),'roof');self.box((9,4.45,1.1),(.06,.06,1),'roof')
  if index==1:
   self.box((0,12,2),(5,.15,1.7),'roof',(.25,.4,.3,1));self.sign('17 / 08 / 1998',(0,11.85,2),.3)
   for x in (-2,2,6):
    for y in (-5,-2):self.table(x,y);self.chair(x,y-1)
  if index in (2,4):
   self.box((-8,8,.025),(5,8,.05),'roof',(.4,.65,.7,1))
   for y in (5,6,7,8,9,10):self.box((-8,y,.2),(3,.8,.12),'wood')
   boat=self.box((-9,3,.3),(1.1,3,.5),'wood');boat.setH(20)
  if index in (3,4):
   for x in (-10,10):
    for y in (-6,-2,3):
     self.box((x,y,1.1),(1.2,1.5,2.2),'wood',solid=True)
     for z in (.4,.9,1.4,1.9):self.box((x,y-.78,z),(.9,.08,.32),'paper')
  if index==4:self.npc(3,4,'Nhi',5);self.people[-1].setScale(.72)
  if index==3:
   self.box((-5,7,.95),(1.2,.8,.12),'wood')
   self.drawer=self.box((-5,6.45 if self.app.state.decisions.get('cabinet_open') else 7,.98),(1.1,.72,.08),'wood')
   self.drawer.setName('archive-drawer')
   self.draft_paper.setPos(-5,self.drawer.getY(),1.035);self.draft_paper.wrtReparentTo(self.drawer)
   if not self.app.state.decisions.get('cabinet_open'):self.draft_paper.hide()
  self.sign('•',(0,8,2.6),.15)
  # Bake static geometry into a few material-compatible batches.
  for child in list(self.root.getChildren()):
   if child.getName()=='box':child.flattenLight()
  amb=AmbientLight('ambient');amb.setColor((.46,.45,.38,1));self.ambient=self.root.attachNewNode(amb);self.root.setLight(self.ambient)
  sun=DirectionalLight('afternoon');sun.setColor((.85,.69,.48,1) if index<2 else (.54,.63,.7,1));self.sun=self.root.attachNewNode(sun);self.sun.setHpr(-35,-55,0);self.root.setLight(self.sun)
  fog=Fog('distance');fog.setColor(.31,.37,.35);fog.setLinearRange(16,48);self.root.setFog(fog)
  self.app.setBackgroundColor(.31,.37,.35,1)
 def walkable(self,x,y):
  r=.28
  return -11.5<x<11.5 and -12<y<12 and not any(a-r<x<b+r and c-r<y<d+r for a,b,c,d in self.blocks)
 def tick(self,dt,time):
  for fan in self.fans:fan.setH(time*120)
  for i,p in enumerate(self.people):
   dx=self.app.camera.getX()-p.getX();dy=self.app.camera.getY()-p.getY();p.setH(math.degrees(math.atan2(dx,-dy)))
   p.setZ(math.sin(time*1.7+i)*.014)
