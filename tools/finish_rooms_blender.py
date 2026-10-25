"""Local Blender Form composition from the human-approved Function layouts.
No paid services. No GLB/runtime export until a separate Form approval.
"""
import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'production/room-review';OUT=ROOT/'production/form-review';OUT.mkdir(parents=True,exist_ok=True)
ASSETS=ROOT/'assets/textures'
def material(name,color,texture=None,metallic=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1);bsdf.inputs['Roughness'].default_value=.72;bsdf.inputs['Metallic'].default_value=metallic
 if texture:
  tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ASSETS/f'{texture}.png'));tex.image.pack();tex.projection='BOX';tex.projection_blend=.12
  m.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
 return m
def assign(o,m):o.data.materials.clear();o.data.materials.append(m)
def box(name,pos,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);assign(o,mat);return o
def cyl(name,pos,radius,depth,mat,vertices=32):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=pos);o=bpy.context.object;o.name=name;assign(o,mat)
 bevel=o.modifiers.new('Rolled manufactured edges','BEVEL');bevel.width=.008;bevel.segments=2
 return o
def aim(cam,pos,target):cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
def render(scene,path):scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
records=[]
for index,rid in enumerate(['courtyard','school','wharf','archive','warehouse']):
 bpy.ops.wm.open_mainfile(filepath=str(PACK/f'{rid}-FUNCTION-DRAFT.blend'))
 scene=bpy.context.scene;floor=bpy.data.objects['floor'];w,d=floor.dimensions.x,floor.dimensions.y
 wood=material('Worn timber',(.28,.16,.08),'wood');plaster=material('Aged lime plaster',(.65,.64,.48),'plaster');tile=material('Terracotta',(.5,.25,.12),'tile');roof=material('Corrugated metal',(.2,.27,.24),'roof',.25);paper=material('Old paper',(.8,.74,.59),'paper');metal=material('Dark iron',(.09,.12,.1),metallic=.5);teal=material('Tin enamel',(.13,.3,.27),metallic=.45);cream=material('Tin cream stripe',(.79,.74,.55),metallic=.35)
 leaf=material('Foliage',(.17,.28,.12));pot=material('Clay',(.4,.2,.11));glass=material('Window glass',(.38,.55,.55));water=material('River',(.12,.24,.26));water.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.2
 for o in list(scene.objects):
  if o.type!='MESH':continue
  name=o.name
  if name=='ceiling':o.location.z-=.02
  mat=plaster if name.startswith('wall') else tile if name=='floor' and index in (0,1) else roof if name=='ceiling' else paper if 'paper' in name else water if name=='river' else wood
  assign(o,mat)
  if name=='tin-design-volume':bpy.data.objects.remove(o,do_unlink=True)
  elif 'table' in name or 'chair' in name or 'crate' in name:
   bevel=o.modifiers.new('Worn edges','BEVEL');bevel.width=.012;bevel.segments=1
 # Distinct hero tin: body, rim, stripe, removable lid and visible seam.
 x,y=2,d/2-2
 body=cyl('TinBody',(x,y,.925),.12,.115,teal)
 lid=cyl('TinLid',(x,y,.987),.124,.014,teal)
 cyl('TinCreamBand',(x,y,.955),.1208,.014,cream)
 cyl('TinRolledRim',(x,y,.98),.123,.009,metal)
 # Letter and key are separate manipulable meshes, placed on the focus table.
 box('ArchiveLetter',(x-.43,y,.885),(.22,.29,.006),paper)
 key=cyl('KeyRing',(x+.36,y,.895),.023,.007,metal,16)
 box('KeyShaft',(x+.41,y,.895),(.09,.012,.006),metal);box('KeyTooth',(x+.45,y+.012,.895),(.012,.03,.006),metal)
 # Window frames and sill books have actual support; no opaque glazing hides an aperture.
 for side,xx in [('west',-w/2),('east',w/2)]:
  for yy in (-.18,2.18):box('WindowJamb-'+side,(xx,yy,2),(.32,.08,1.48),wood)
  for zz in (1.3,2.7):box('WindowRail-'+side,(xx,1,zz),(.32,2.48,.08),wood)
  box('WindowMullion-'+side,(xx,1,2),(.25,.06,1.4),wood)
 # Hinged door leaf is stored open; opening remains traversable.
 door=box('ExitDoorLeaf',(w/2-1.2,d/2+.8,1.28),(.09,1.6,2.55),wood)
 cyl('DoorHandle',(w/2-1.14,d/2+.3,1.05),.035,.09,metal,12).rotation_euler[1]=math.pi/2
 # Original potted plants, bowls and cups add grounded domestic scale.
 for px,py in [(-w/2+1,-d/2+1),(w/2-1,-d/2+1)]:
  cyl('PlantPot',(px,py,.2),.23,.4,pot,16)
  for k in range(6):
   a=k*math.tau/6
   cyl('PlantStem',(px+math.cos(a)*.15,py+math.sin(a)*.15,.5),.015,.32,leaf,8)
   bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(px+math.cos(a)*.22,py+math.sin(a)*.22,.65));o=bpy.context.object;o.name='PlantLeaf';o.scale=(.12,.36,.055);o.rotation_euler=(.4,0,a);assign(o,leaf)
 for tx,ty in [(-w/2+2,-1),(w/2-2,1)]:
  cyl('TeaCup',(tx+.42,ty,.92),.045,.1,cream,16)
  box('EvidencePage',(tx,ty,.878),(.28,.36,.006),paper)
 # Readable storage contents, not empty repeated furniture.
 if index==3:
  for sx in (-w/2+1,w/2-1):
   for sy in (-3,0,3):
    for sz in (.78,1.33,1.88):
     for k in range(5):box('ArchiveFolder',(sx,sy-.55+k*.25,sz),(.65,.19,.18),paper)
 if index==1:
  for xx in (-3,0,3):
   for yy in (-3,0,3):box('ExerciseBook',(xx,yy,.88),(.2,.28,.02),paper)
 # Exterior receiver makes every aperture show depth and a destination.
 box('ExteriorGround',(0,0,-.22),(w+14,d+14,.2),plaster)
 # Suspended fan with explicit stem attached to ceiling underside.
 fan_y=d/2-2 if index in (0,2) else 0
 cyl('FanStem',(0,fan_y,3.385),.035,.41,metal,12);cyl('FanMotor',(0,fan_y,3.14),.13,.14,metal,16)
 for k in range(3):
  a=k*math.tau/3;blade=box('FanBlade',(math.cos(a)*.38,fan_y+math.sin(a)*.38,3.08),(.65,.13,.025),wood);blade.rotation_euler[2]=a
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False
 scene.render.resolution_x=800;scene.render.resolution_y=450;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX'
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.64,.7,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
 bpy.ops.object.light_add(type='SUN',location=(0,0,8));sun=bpy.context.object;sun.rotation_euler=(.55,-.5,-.7);sun.data.energy=2;sun.data.angle=.15;sun.data.color=(1,.83,.62) if index<2 else (.75,.85,1)
 bpy.ops.object.light_add(type='AREA',location=(0,0,3.5));light=bpy.context.object;light.data.energy=250;light.data.shape='DISK';light.data.size=8
 cam=scene.camera;cam.data.type='PERSP';cam.data.lens=21;cam.data.clip_start=.05
 dest=OUT/rid;dest.mkdir(exist_ok=True)
 aim(cam,(0,-d/2+1,1.7),(0,d/2,1.5));render(scene,dest/'production.png')
 # Wide corner checks plus three deliberate ceiling views.
 cam.data.lens=10.4
 views=[('corner-sw',(-w/2+.5,-d/2+.5,1.7),(0,0,1.6)),('corner-se',(w/2-.5,-d/2+.5,1.7),(0,0,1.6)),('corner-nw',(-w/2+.5,d/2-.5,1.7),(0,0,1.6)),('corner-ne',(w/2-.5,d/2-.5,1.7),(0,0,1.6)),('center-up',(0,fan_y,.3),(0,fan_y,4)),('ceiling-a',(-w/2+1,-d/2+1,1.5),(0,fan_y,3.6)),('ceiling-b',(w/2-1,d/2-1,1.5),(0,fan_y,3.6))]
 for name,pos,target in views:aim(cam,pos,target);render(scene,dest/f'{name}.png')
 cam.data.lens=21;aim(cam,(0,-d/2+1,1.7),(0,d/2,1.5))
 scene['review_status']='Form review pending';scene['generation_route']='Local Blender; no paid API'
 bpy.ops.wm.save_as_mainfile(filepath=str(dest/f'{rid}-FORM.blend'))
 triangles=sum(len(p.vertices)-2 for o in scene.objects if o.type=='MESH' for p in o.data.polygons)
 records.append({'room':rid,'source':f'{rid}/{rid}-FORM.blend','source_sha256':hashlib.sha256((dest/f'{rid}-FORM.blend').read_bytes()).hexdigest(),'baseTriangles':triangles,'renders':8,'formApproval':'pending','runtimeExport':False})
 (OUT/'manifest.json').write_text(json.dumps(records,indent=2))
 print('FORM ROOM COMPLETE',rid,flush=True)
