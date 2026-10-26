from dataclasses import dataclass, field, asdict

@dataclass
class State:
    schema: int = 2
    room: str = 'station'
    x: float = 64.0
    y: float = 272.0
    solved: list = field(default_factory=list)
    inventory: list = field(default_factory=lambda: ['Ảnh lớp bị cào', 'Chìa khóa đồng', 'Cassette chưa nghe'])
    evidence: list = field(default_factory=list)
    journal: list = field(default_factory=list)
    heard: list = field(default_factory=list)
    flags: dict = field(default_factory=dict)
    relations: dict = field(default_factory=dict)
    attempts: dict = field(default_factory=dict)
    hints: dict = field(default_factory=dict)
    choices: dict = field(default_factory=dict)
    fear: float = 0.0
    guilt: int = 0
    clarity: int = 0
    phase: str = 'afternoon'
    chapter: int = 0
    memory: bool = False
    play_seconds: float = 0.0
    def snapshot(self):
        return asdict(self)

DEFAULT_SETTINGS = {
    'master': 0.7, 'music': 0.35, 'effects': 0.6, 'voice': 0.6,
    'reduced_flashes': True, 'reduced_scares': False, 'reduced_motion': True,
    'reduced_blood': True, 'crt': False, 'fullscreen': False, 'language': 'vi',
    'keys': {'interact': 'e', 'journal': 'j', 'inventory': 'tab', 'memory': 'm'},
}
