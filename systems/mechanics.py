"""Small interactive puzzle models. Game and route tests use the same input path."""
class Mechanism:
    def __init__(self,puzzle):
        self.kind=puzzle['mechanic'];self.cursor=0;self.values=[0,0,0];self.selected=[];self.rhythm=[];self.phase=0
    def key(self,name):
        if name=='left':self.cursor=(self.cursor-1)%3
        if name=='right':self.cursor=(self.cursor+1)%3
        if self.kind=='basket' and name in ('1','2','3'):
            i=int(name)-1
            if i in self.selected:self.selected.remove(i)
            else:self.selected.append(i)
        elif self.kind in ('wires','sequence') and name in ('1','2','3','4'):
            if len(self.selected)<3:self.selected.append(int(name))
        elif self.kind=='battery' and name=='space':self.phase=1-self.phase
        elif self.kind=='dials' and name in ('up','down'):self.values[self.cursor]=(self.values[self.cursor]+(1 if name=='up' else -1))%10
        elif self.kind=='count' and name in ('up','down'):self.phase=max(0,min(9,self.phase+(1 if name=='up' else -1)))
        elif self.kind=='rhythm':
            if name=='space' and len(self.rhythm)<8:self.rhythm.append('x')
            if name=='right' and len(self.rhythm)<8:self.rhythm.append('|')
        elif self.kind=='doors' and name in ('1','2','3'):self.phase=int(name)
        elif self.kind=='latch':
            if name=='left' and self.phase==0:self.phase=1
            elif name=='down' and self.phase==1:self.phase=2
        if name=='backspace':self.selected=[];self.rhythm=[];self.phase=0;self.values=[0,0,0]
    def answer(self):
        if self.kind=='basket':return str(sum([120,80,200][i] for i in self.selected))
        if self.kind=='battery':return '-' if self.phase else '+'
        if self.kind in ('sequence','wires'):return ''.join(map(str,self.selected))
        if self.kind=='rhythm':return '21' if ''.join(self.rhythm)=='xx|x' else 'invalid_rhythm'
        if self.kind=='dials':return ''.join(map(str,self.values))
        if self.kind=='count':return str(self.phase)
        if self.kind=='doors':return str(self.phase)
        if self.kind=='latch':return '2' if self.phase==2 else '1'
        return None
    @property
    def instructions(self):
        return {'basket':'1 Cơm • 2 Trà • 3 Pin — chọn/bỏ món', 'battery':'Space: xoay pin • Enter: lắp thử', 'sequence':'Nhập thứ tự các số ngày • Backspace: làm lại', 'wires':'1 / 2 / 3: nối cổng theo thứ tự • Backspace: tháo', 'rhythm':'Space: gõ • →: khoảng nghỉ • Backspace: thử lại', 'dials':'← →: chọn vòng • ↑ ↓: xoay số', 'count':'↑ ↓: đếm người chưa có tên', 'doors':'1 / 2 / 3: chọn cửa theo nguồn âm', 'latch':'← rút chốt, rồi ↓ lùi khỏi ngưỡng'}.get(self.kind,'Nhập câu trả lời bằng bàn phím')
    def display(self):
        if self.kind=='basket':return ' + '.join(['Cơm','Trà','Pin'][i] for i in sorted(self.selected)) or 'Giỏ trống'
        if self.kind=='battery':return '[ Lò xo ]  '+ ('− | PIN | +' if self.phase else '+ | PIN | −')
        if self.kind in ('sequence','wires'):return ' → '.join(map(str,self.selected)) or 'Chưa sắp xếp'
        if self.kind=='rhythm':return ' '.join('cộc' if k=='x' else '— nghỉ —' for k in self.rhythm) or 'Đang nghe'
        if self.kind=='dials':return '   '.join(f'[{v}]' if i==self.cursor else str(v) for i,v in enumerate(self.values))
        if self.kind=='count':return f'Có {self.phase} người chưa có tên'
        if self.kind=='doors':return f'Cửa đã chọn: {self.phase or "chưa chọn"}'
        if self.kind=='latch':return ('Chốt đang cài','Đã rút chốt • hãy lùi lại','Ngưỡng cửa đã trống')[self.phase]
        return ''
