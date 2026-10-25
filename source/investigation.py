"""Evidence links are stored by ID and evaluated independently of UI text."""
from .core import NOTES
LINKS={
 frozenset(('calendar','photo')):{'vi':'Ngày trong ảnh xác nhận Lan có mặt sau tháng bảy.','en':'The photograph confirms Lan was present after July.'},
 frozenset(('register','attendance')):{'vi':'Phiếu trực nhật mâu thuẫn với ngày tự ý nghỉ.','en':'The cleaning rota contradicts the claimed departure date.'},
 frozenset(('carbon','register')):{'vi':'Bản sao giữ lại lý do di dời đã bị sửa ở bản gốc.','en':'The copy preserves the relocation reason erased from the original.'},
 frozenset(('ferry','receipt')):{'vi':'Hai đầu hành trình cùng xác nhận chuyến cứu người.','en':'Both ends of the journey independently confirm the rescue.'},
 frozenset(('petition','photo')):{'vi':'Tấm ảnh làm suy yếu lời khai nhà đã trống.','en':'The photograph undermines the vacancy claim.'},
 frozenset(('draft','petition')):{'vi':'Thư giải thích ai hướng dẫn bức vẽ và ai hưởng lợi.','en':'The letter identifies who directed the drawing and benefited.'},
 frozenset(('lan','editor')):{'vi':'Cả hai đều yêu cầu xác minh và sự đồng ý trước khi trích lời.','en':'Both require verification and consent before quotation.'},
}
def connect(state,a,b):
 if a==b or a not in state.clues or b not in state.clues:return None
 key=frozenset((a,b))
 if key not in LINKS:return None
 link=sorted((a,b))
 if link not in state.links:state.links.append(link)
 return LINKS[key]
def chapter_snapshot(state,index):
 """Replay unlocked chapters without overwriting the canonical campaign."""
 from dataclasses import asdict
 from .core import State,STORY
 if type(index)!=int or not 0<=index<=state.chapter:raise ValueError('locked chapter')
 clone=State(**asdict(state));clone.chapter=index;clone.position=[0,-8,1.7];clone.heading=0;clone.ending=None
 permitted={p['id'] for c in STORY['chapters'][:index] for p in c['puzzles']}
 clone.solved=[p for p in clone.solved if p in permitted]
 clone.decisions['replay']=True
 return clone.validate()
