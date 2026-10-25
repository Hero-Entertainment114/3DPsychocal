"""Offline Japanese/Chinese draft translation using official Argos models.
Authoring only: pip install ctranslate2 sentencepiece numpy.
Models are not required by the game and are not included in player packages.
"""
import argparse,json,sys,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from source.locale import UI
import ctranslate2,sentencepiece as spm
parser=argparse.ArgumentParser();parser.add_argument('--models',type=Path,required=True);args=parser.parse_args()
texts=set(v[1] for v in UI.values())
def visit(value):
 if isinstance(value,dict):
  if 'en' in value:texts.add(value['en'])
  else:
   for v in value.values():visit(v)
 elif isinstance(value,list):
  for v in value:visit(v)
for name in ('story.json','dialogues.json','side_stories.json'):visit(json.loads((ROOT/'data'/name).read_text()))
catalog={}
for lang,folder in [('ja','en_ja'),('zh','translate-en_zh-1_9')]:
 model=args.models/folder
 tokenizer=spm.SentencePieceProcessor(model_file=str(model/'sentencepiece.model'))
 translator=ctranslate2.Translator(str(model/'model'),device='cpu',compute_type='int8',inter_threads=2,intra_threads=4)
 catalog[lang]={}
 for index,text in enumerate(sorted(texts)):
  # Preserve paragraph order; split long paragraphs at sentence boundaries.
  paras=[]
  for para in text.split('\n'):
   sentences=re.split(r'(?<=[.!?])\s+',para)
   tokens=[tokenizer.encode(s,out_type=str) for s in sentences if s.strip()]
   result=translator.translate_batch(tokens,beam_size=3,max_decoding_length=300,repetition_penalty=1.1) if tokens else []
   paras.append(''.join(tokenizer.decode(r.hypotheses[0]) for r in result))
  catalog[lang][text]='\n'.join(paras)
  if index%40==0:print(lang,index,len(texts),flush=True)
 catalog[lang].update({'New game':'ニューゲーム' if lang=='ja' else '新游戏','Settings':'設定' if lang=='ja' else '设置','Language: English':'言語：日本語' if lang=='ja' else '语言：简体中文','THE NAMELESS WHARF':'名もなき船着き場' if lang=='ja' else '无名渡口'})
 (ROOT/'data/translations.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
print('Translated',len(texts),'unique source strings per language')
(ROOT/'docs/LOCALIZATION_STATUS.json').write_text(json.dumps({'languages':['vi','en','ja','zh'],'ja_zh_status':'offline machine-translation draft; native-speaker review pending','engine':'CTranslate2 4.8.3 / official Argos models en-ja 1.1 and en-zh 1.9','strings_per_new_language':len(texts),'runtime_requires_models':False},indent=2))
