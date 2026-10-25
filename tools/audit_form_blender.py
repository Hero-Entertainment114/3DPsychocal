"""Evaluate real mesh topology, openings and principal fixture support."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]/'production/form-review';reports=[]
for record in json.loads((ROOT/'manifest.json').read_text()):
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/record['source']))
 graph=bpy.context.evaluated_depsgraph_get();triangles=0;nonmanifold=[]
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  e=o.evaluated_get(graph);mesh=e.to_mesh();bm=bmesh.new();bm.from_mesh(mesh)
  triangles+=sum(len(p.vertices)-2 for p in mesh.polygons)
  if any(not edge.is_manifold for edge in bm.edges):nonmanifold.append(o.name)
  bm.free();e.to_mesh_clear()
 w=bpy.data.objects['floor'].dimensions.x;d=bpy.data.objects['floor'].dimensions.y
 def clear(name,origin,direction):
  o=bpy.data.objects[name];inv=o.matrix_world.inverted();loc=inv@Vector(origin);direction=inv.to_3x3()@Vector(direction)
  return not o.ray_cast(loc,direction,distance=2)[0]
 doors={'arrival':clear('wall-south',(0,-d/2-1,1.3),(0,1,0)),'exit':clear('wall-north',(w/2-2,d/2+1,1.3),(0,-1,0)),'windowWest':clear('wall-west',(-w/2-1,1,2),(1,0,0)),'windowEast':clear('wall-east',(w/2+1,1,2),(-1,0,0))}
 ceiling=bpy.data.objects['ceiling'];gap=ceiling.location.z-ceiling.dimensions.z/2-3.6
 tin=bpy.data.objects['TinBody'];tin_contact=tin.location.z-tin.dimensions.z/2-.87
 reports.append({'room':record['room'],'evaluatedTriangles':triangles,'underTriangleBudget':triangles<100000,'nonManifoldMeshes':nonmanifold,'apertureRayTests':doors,'ceilingWallGapMeters':round(gap,5),'tinTableContactMeters':round(tin_contact,5),'remainingChecks':['BVH clearance for every prop','seating orientation and production-camera tangencies','full artistic review','human Form approval','runtime export/performance']})
(ROOT/'geometry-audit.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports))
