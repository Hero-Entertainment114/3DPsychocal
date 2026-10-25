"""Deterministic original textures and synthesized audio, built offline."""
import math, random, wave, struct
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'assets'
rng=random.Random(1998)
for name,base in {'plaster':(166,164,123),'wood':(94,65,42),'tile':(146,78,52),'concrete':(115,119,110),'paper':(218,207,164),'roof':(78,94,88)}.items():
 im=Image.new('RGB',(256,256));pix=im.load()
 for y in range(256):
  for x in range(256):
   noise=rng.randint(-13,13)+(int(7*math.sin(x*.4+y*.02)) if name=='wood' else 0)
   pix[x,y]=tuple(max(0,min(255,c+noise)) for c in base)
 d=ImageDraw.Draw(im)
 if name=='tile':
  for n in range(0,257,64):d.line((n,0,n,256),fill=(75,67,52),width=3);d.line((0,n,256,n),fill=(75,67,52),width=3)
 if name=='roof':
  for n in range(0,256,16):d.line((n,0,n,256),fill=(46,57,54),width=4)
 if name=='paper':
  for y in range(35,230,14):d.line((25,y,rng.randint(130,230),y),fill=(104,92,74),width=2)
 im.save(ROOT/f'textures/{name}.png')
def write(name,duration,func):
 rate=22050
 with wave.open(str(ROOT/f'audio/{name}.wav'),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
  f.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,func(i/rate)))*18000)) for i in range(int(rate*duration))))
notes=[220,261.63,329.63,293.66,220,196,246.94,164.81]
def music(t):
 k=int(t/2)%len(notes);u=t%2;f=notes[k]
 return .18*math.exp(-u*1.5)*(math.sin(2*math.pi*f*t)+.3*math.sin(4*math.pi*f*t))
write('memory',16,music)
write('rain',8,lambda t:rng.uniform(-.13,.13)*(.6+.2*math.sin(t*3)))
write('paper',.3,lambda t:rng.uniform(-.3,.3)*math.exp(-t*14))
write('step',.16,lambda t:rng.uniform(-.2,.2)*math.exp(-t*25))
write('discovery',1.2,lambda t:.2*math.sin(2*math.pi*(440 if t<.4 else 554.37 if t<.8 else 659.25)*t)*math.sin(math.pi*t/1.2))
print('6 original textures and 5 WAV files generated')
