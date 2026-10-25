from pathlib import Path
import os
import sys
ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
USER = Path(os.environ.get('FORGOTTEN_VOICES_USER_DIR', str(Path(os.environ.get('LOCALAPPDATA', Path.home() / '.local' / 'share')) / '3DPsychocal')))
