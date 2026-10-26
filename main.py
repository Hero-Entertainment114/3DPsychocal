"""Run offline: python main.py. Headless smoke: python main.py --headless --frames 60."""
import argparse
import logging
import os
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description='Wasurerareta Koe • 3DPsychocal')
    p.add_argument('--headless',action='store_true')
    p.add_argument('--frames',type=int,default=0)
    p.add_argument('--screenshot',type=Path)
    p.add_argument('--user-dir',type=Path)
    args=p.parse_args()
    if args.headless:
        os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
    from core.paths import USER
    folder=args.user_dir or USER;folder.mkdir(parents=True,exist_ok=True)
    logging.basicConfig(filename=folder/'game.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    try:
        from core.game import Game
        Game(args.headless,folder).run(args.frames,args.screenshot)
    except Exception:
        logging.exception('Fatal error')
        print('Không thể mở game. Xem nhật ký:',folder/'game.log')
        raise

if __name__=='__main__':main()
