"""Original short motifs; no external samples or commercial music."""
from pathlib import Path
import wave,math,struct
ROOT=Path(__file__).resolve().parents[1]/'assets/audio'
THEMES={
 'menu':([57,60,64,67,64,60,59,55],2.5),
 'chapter0':([60,64,67,69,67,64,62,60],2.0),
 'chapter1':([57,60,64,63,60,59,55,57],2.2),
 'chapter2':([50,57,60,62,57,53,52,50],2.4),
 'chapter3':([52,59,60,58,55,53,51,52],2.3),
 'chapter4':([57,60,64,67,65,62,59,57],2.6),
 'ending_silence':([57,60,59,55,52,50,48,45],3.0),
 'ending_alone':([57,58,64,63,60,59,55,58],2.7),
 'ending_together':([57,60,64,67,69,67,64,60],2.8),
}
for name,(notes,beat) in THEMES.items():
 rate=22050;seconds=len(notes)*beat;frames=bytearray()
 for i in range(int(seconds*rate)):
  t=i/rate;k=int(t/beat);u=t%beat;f=440*2**((notes[k]-69)/12)
  envelope=(1-math.exp(-u*35))*math.exp(-u*1.4)
  value=envelope*(.22*math.sin(2*math.pi*f*u)+.065*math.sin(4*math.pi*f*u)+.025*math.sin(6*math.pi*f*u))
  # A quiet lower fifth gives each plucked note a stable harmonic floor.
  value+=.025*math.sin(2*math.pi*f*.5*u)*math.sin(math.pi*u/beat)**2
  frames.extend(struct.pack('<h',int(value*22000)))
 with wave.open(str(ROOT/f'{name}.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(frames)
print(f'{len(THEMES)} original score cues generated')
