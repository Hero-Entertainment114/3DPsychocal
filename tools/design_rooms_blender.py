"""Function-review geometry only. No final scene/export approval is implied.
Run: blender --background --python tools/design_rooms_blender.py
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]/'production/room-review';ROOT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.background_type='WORLD';scene.world.color=(1,1,1)
scene.render.resolution_x=960;scene.render.resolution_y=960;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard';scene.render.film_transparent=False
plans=[]
def box(name,pos,dim,col=.55):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.dimensions=dim;o.color=(col,col,col,1);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
def table(x,y):
 box('table-top',(x,y,.82),(1.8,.9,.1),.35)
 for dx in (-.72,.72):
  for dy in (-.3,.3):box('table-leg',(x+dx,y+dy,.385),(.08,.08,.77),.25)
def chair(x,y):
 box('chair-seat',(x,y,.45),(.55,.55,.08),.4);box('chair-back',(x,y+.24,.8),(.55,.06,.65),.4)
 for dx in (-.21,.21):
  for dy in (-.21,.21):box('chair-leg',(x+dx,y+dy,.21),(.06,.06,.42),.3)
def aperture(wall,pos,dim,name):
 cutter=box(name+'-cutter',pos,dim);bpy.context.view_layer.objects.active=wall
 mod=wall.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
def aim(camera,pos,target):camera.location=pos;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
def render(name):scene.render.filepath=str(ROOT/name);bpy.ops.render.render(write_still=True)
for idx,(rid,w,d) in enumerate([('courtyard',18,16),('school',16,12),('wharf',20,14),('archive',14,12),('warehouse',18,16)]):
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 floor=box('floor',(0,0,-.1),(w,d,.2),.9)
 walls={}
 for name,pos,dim in [('north',(0,d/2,1.8),(w,.3,3.6)),('south',(0,-d/2,1.8),(w,.3,3.6)),('west',(-w/2,0,1.8),(.3,d,3.6)),('east',(w/2,0,1.8),(.3,d,3.6))]:walls[name]=box('wall-'+name,pos,dim,.6)
 aperture(walls['south'],(0,-d/2,1.3),(3,.7,2.6),'arrival')
 aperture(walls['north'],(w/2-2,d/2,1.3),(1.6,.7,2.6),'exit')
 for side in ('west','east'):
  x=(-1 if side=='west' else 1)*w/2
  aperture(walls[side],(x,1,2),(.7,2.4,1.4),'window-'+side)
  box('window-sill-'+side,(x,1,1.29),(.5,2.6,.12),.4)
 # Arrival apron and exit landing make the destinations spatially legible.
 box('arrival-apron',(0,-d/2-1.5,-.1),(3.8,3,.2),.85)
 box('exit-landing',(w/2-2,d/2+1,-.1),(2,2,.2),.85)
 roof=box('ceiling',(0,d/2-2,3.7),(w,4,.18),.8) if idx in (0,2) else box('ceiling',(0,0,3.7),(w,d,.18),.8)
 for x,y in [(-w/2+2,-1),(w/2-2,1),(-w/2+2,d/2-2),(2,d/2-2)]:table(x,y)
 if idx==0:
  for x in (-2,0,2):chair(x,-3)
 elif idx==1:
  for x in (-3,0,3):
   for y in (-3,0,3):table(x,y);chair(x,y-.9)
  box('blackboard',(0,d/2-.2,2),(4,.12,1.5),.15)
 elif idx==2:
  water=box('river',(-w/2-2,1,-.25),(4,d+6,.1),.75)
  for y in range(-3,5):box('dock-plank',(-w/2-1,y,.03),(2,.85,.12),.4)
 elif idx==3:
  for x in (-w/2+1,w/2-1):
   for y in (-3,0,3):
    box('shelf-back',(x,y,1.15),(.15,1.7,2.3),.5)
    for z in (.1,.65,1.2,1.75,2.3):box('shelf-board',(x,y,z),(1,1.7,.08),.4)
 elif idx==4:
  for x,y in [(-5,-4),(-4,-4),(5,-3),(5,-2),(-5,3)]:box('storage-crate',(x,y,.55),(.9,.9,1.1),.4)
  for x in (-1,1):chair(x,3)
 # Shared hero placeholder is an explicit dimensional design volume, not a generated final asset.
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.12,depth=.12,location=(2,d/2-2,.93));hero=bpy.context.object;hero.name='tin-design-volume';hero.color=(.2,.2,.2,1)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='ReviewCamera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(w,d+6)+2
 roof.hide_render=True;aim(cam,(0,0,30),(0,0,0));render(f'plans/{rid}-floor.png')
 roof.hide_render=False
 for o in scene.objects:
  if o.type=='MESH' and o!=roof:o.hide_render=True
 aim(cam,(0,0,-12),(0,0,4));render(f'plans/{rid}-ceiling.png')
 for o in scene.objects:o.hide_render=False
 cam.data.type='PERSP';cam.data.lens=24;aim(cam,(0,-d/2+1,1.7),(0,d/2,1.5));render(f'renders/{rid}-arrival.png')
 # Elevation sees the actual Boolean geometry, with dressing hidden.
 for o in scene.objects:
  if o.type=='MESH':o.hide_render=o!=walls['south']
 cam.data.type='ORTHO';cam.data.ortho_scale=w+1;aim(cam,(0,-25,1.8),(0,0,1.8));render(f'plans/{rid}-south-elevation.png')
 for o in scene.objects:o.hide_render=False
 cam.data.type='PERSP';aim(cam,(0,-d/2+1,1.7),(0,d/2,1.5))
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'{rid}-FUNCTION-DRAFT.blend'))
 objects=[]
 for o in scene.objects:
  if o.type=='MESH':objects.append({'id':o.name,'position':list(o.location),'dimensions':list(o.dimensions),'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)})
 plans.append({'id':rid,'bounds':[w,d,3.8],'objects':objects,'arrivalWidth':3,'exitWidth':1.6,'status':'Function proposal; not final Form composition'})
(ROOT/'geometry-metadata.json').write_text(json.dumps(plans,indent=2))
print('Five Function-review design sources and 20 renders created; no runtime export.')
