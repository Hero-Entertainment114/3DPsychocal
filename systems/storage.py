import json
import math
import os
import logging
from copy import deepcopy
from core.state import State, DEFAULT_SETTINGS

class SaveError(ValueError): pass

def validate(data, content):
    if not isinstance(data, dict) or data.get('schema') != 2:
        raise SaveError('Phiên bản save không được hỗ trợ.')
    fields = State().__dict__
    if set(data) != set(fields): raise SaveError('Save thiếu trường hoặc có trường lạ.')
    for key, default in fields.items():
        value = data[key]
        if isinstance(default, bool): ok = type(value) is bool
        elif type(default) is int: ok = type(value) is int
        elif type(default) is float:
            ok = type(value) in (int, float) and math.isfinite(value)
        else: ok = isinstance(value, type(default))
        if not ok: raise SaveError(f'Trường không hợp lệ: {key}')
    if data['room'] not in content.maps: raise SaveError('Bản đồ không hợp lệ.')
    m = content.maps[data['room']]
    if not (16 <= data['x'] < m['width']*16-16 and 40 <= data['y'] < m['height']*16-16):
        raise SaveError('Vị trí ngoài bản đồ.')
    if m['tiles'][int(data['y'])//16][int(data['x'])//16] in (1, 3):
        raise SaveError('Vị trí nằm trong tường hoặc bàn.')
    for key in ('solved', 'inventory', 'evidence', 'journal', 'heard'):
        if len(data[key]) > 5000 or any(not isinstance(x, str) for x in data[key]):
            raise SaveError(f'Danh sách lỗi: {key}')
    playable = {p['id'] for p in content.playable}
    if len(set(data['solved'])) != len(data['solved']) or not set(data['solved']) <= playable:
        raise SaveError('Câu đố không hợp lệ.')
    for pid in data['solved']:
        if not set(content.puzzles[pid]['requires']) <= set(data['solved']):
            raise SaveError('Thiếu điều kiện câu đố.')
    if not set(data['heard']) <= set(content.dialogues): raise SaveError('Hội thoại không hợp lệ.')
    if not set(data['evidence']) <= {p['reward'] for p in content.playable}: raise SaveError('Chứng cứ không hợp lệ.')
    if any(v > 3 for v in data['hints'].values() if type(v) is int): raise SaveError('Gợi ý vượt giới hạn.')
    if data['phase'] not in ('afternoon', 'evening', 'night', 'dawn') or data['chapter'] not in (0, 1):
        raise SaveError('Giai đoạn không hợp lệ.')
    if not 0 <= data['fear'] <= 100 or not 0 <= data['clarity'] <= 10000 or not 0 <= data['guilt'] <= 10000 or data['play_seconds'] < 0:
        raise SaveError('Trạng thái ngoài giới hạn.')
    for key in ('attempts', 'hints'):
        if any(k not in playable or type(v) is not int or v < 0 for k,v in data[key].items()):
            raise SaveError('Bộ đếm câu đố không hợp lệ.')
    if any(k not in playable or not isinstance(v, str) for k,v in data['choices'].items()):
        raise SaveError('Lựa chọn không hợp lệ.')
    if any(not isinstance(k, str) or type(v) not in (bool, str, int) for k,v in data['flags'].items()):
        raise SaveError('Cờ truyện không hợp lệ.')
    for cid, rel in data['relations'].items():
        if cid not in content.characters or not isinstance(rel, dict) or set(rel) != {'trust','familiarity','resentment','dependence','knowledge','willingness'}:
            raise SaveError('Quan hệ không hợp lệ.')
        if any(type(v) is not int or not -100 <= v <= 100 for v in rel.values()): raise SaveError('Chỉ số quan hệ lỗi.')
    return State(**data)

def migrate(data, content):
    if not isinstance(data,dict) or data.get('schema')!=1:return data
    result=deepcopy(data)
    # Validate the old payload's shape before relocating a legacy position.
    if set(result)!=set(State().__dict__):raise SaveError('Save cũ thiếu trường.')
    if any(type(result[k]) not in (float,int) or not math.isfinite(result[k]) for k in ('x','y')):raise SaveError('Tọa độ save cũ lỗi.')
    if result['room'] not in content.maps:raise SaveError('Bản đồ cũ không hợp lệ.')
    if not isinstance(result['flags'],dict) or not isinstance(result['solved'],list):raise SaveError('Tiến trình save cũ lỗi.')
    result['schema']=2
    result['x'],result['y']=content.maps[result['room']]['entry']
    for pid in result['solved']:
        if pid not in content.puzzles:raise SaveError('Câu đố cũ không hợp lệ.')
        for oid in content.puzzles[pid].get('observations',[]):result['flags']['observed_'+oid]=True
    result['flags']['migrated_v1']=True
    return result

class Storage:
    def __init__(self, directory, content):
        self.directory, self.content = directory, content
        directory.mkdir(parents=True, exist_ok=True)
    def path(self, slot):
        if slot not in ('auto', '1', '2', '3'): raise SaveError('Ô lưu không hợp lệ.')
        return self.directory / f'save_{slot}.json'
    def save(self, state, slot='auto'):
        data = state.snapshot()
        validate(data, self.content)
        target = self.path(slot)
        temporary = target.with_suffix('.tmp')
        with temporary.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush(); os.fsync(f.fileno())
        temporary.replace(target)
    def load(self, slot='auto'):
        try:
            target = self.path(slot)
            if target.stat().st_size > 2_000_000: raise SaveError('Save quá lớn.')
            raw=target.read_text(encoding='utf-8')
            data=json.loads(raw)
            result=validate(migrate(data,self.content),self.content)
            if data.get('schema')==1:
                backup=target.with_suffix('.v1.bak')
                if not backup.exists():backup.write_text(raw,encoding='utf-8')
            return result
        except (OSError, ValueError, TypeError) as e:
            logging.exception('Save load failed')
            raise SaveError('Không thể đọc save; tệp gốc được giữ nguyên. ' + str(e)) from e
    def settings(self):
        result = deepcopy(DEFAULT_SETTINGS)
        try:
            data = json.loads((self.directory / 'settings.json').read_text(encoding='utf-8'))
            for k in result:
                v = data.get(k)
                if k in ('master','music','effects','voice') and type(v) in (int,float) and math.isfinite(v): result[k] = max(0,min(1,v))
                elif isinstance(result[k], bool) and type(v) is bool: result[k] = v
                elif k == 'keys' and isinstance(v, dict):
                    for action, key in v.items():
                        if action in result[k] and isinstance(key,str) and len(key) < 20: result[k][action] = key
        except (OSError, ValueError, TypeError, AttributeError): pass
        return result
    def save_settings(self, settings):
        target = self.directory / 'settings.json'
        temp = target.with_suffix('.tmp')
        temp.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(target)
