#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque
from itertools import accumulate
from functools import cache

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

NUMPAD = {
        0:'7',1:'8',2:'9',
        1j:'4',1+1j:'5',2+1j:'6',
        2j:'1',1+2j:'2',2+2j:'3',
        3j:None, 1+3j:'0',2+3j:'A'
        }
NUMPOS = {v:k for k, v in NUMPAD.items()}
DPAD = {
        0:None,1:'^',2:'A',
        1j:'<',1+1j:'v',2+1j:'>'
        }
DPOS = {v:k for k, v in DPAD.items()}
BUTTON_MAP = {1:'>',-1:'<',1j:'v',-1j:'^',0:'A'}
DXY_MAP = {v:k for k, v in BUTTON_MAP.items()}

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

@cache
def dist_to_buttons(dest: complex, src: complex, layer: int) -> list:
    """
    given a complex representing the manhattan dist
    return _safe_ direction in terms of arrows
    e.g. 1+2j -> '>vv'
    @cache performed better than manual cache
    """
    dist = dest - src
    xstep = 0 if not dist.real else int(dist.real / abs(dist.real))
    ystep = 0 if not dist.imag else int(dist.imag / abs(dist.imag))
    xs = [] if not xstep else [BUTTON_MAP[xstep]] * int(abs(dist.real))
    ys = [] if not ystep else [BUTTON_MAP[ystep*1j]] * int(abs(dist.imag))
    # check for gaps
    key_map = NUMPAD if layer == 0 else DPAD
    if xstep:
        # xpath = list(accumulate(xs, lambda a, b: a + DXY_MAP[b], initial=src))
        # if not all(key_map[xy] for xy in xpath):
        for dx in range(xstep, int(dist.real)+xstep, xstep):
            if key_map[src+dx]:
                continue
            # gap if x-dir first
            return press_pad(tuple(ys+xs+['A']), layer=layer+1)
    if ystep:
        # ypath = list(accumulate(ys, lambda a, b: a + DXY_MAP[b], initial=src))
        # if not all(key_map[xy] for xy in ypath):
        for dy in range(ystep, int(dist.imag)+ystep, ystep):
            if key_map[src+dy*1j]:
                continue
            return press_pad(tuple(xs+ys+['A']), layer=layer+1)  
    a = press_pad(tuple(xs+ys+['A']), layer=layer+1)  
    b = press_pad(tuple(ys+xs+['A']), layer=layer+1)
    # if both safe, return shortest
    buttons = a if len(a) <= len(b) else b
    return buttons

@cache
def press_pad(cmds: tuple, key: str = 'A', layer=0) -> list:
    """
    return movement and presses required for dpad
    """
    logger.debug(f'layer {layer} cmds {cmds}')
    # 3 for part i, 26 for part ii (25 from text, but program takes 26)
    if layer == 18:
        return cmds
    pos_map = NUMPOS if layer == 0 else DPOS
    pos = pos_map[key]
    buttons = []
    for press in cmds:
        presses = dist_to_buttons(dest=pos_map[press], src=pos, layer=layer)
        buttons += presses
        #logger.debug(f'{key_map[pos]} -> {press}: {presses}\nbuttons {buttons}')
        pos = pos_map[press]
    #logger.debug(f'layer {layer} cmds {cmds} -> {buttons}')
    return buttons

    
def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input; tuple over list for cache
    codes = [tuple(line.strip()) for line in read_line(fp)]
    # execute
    cmplx = 0
    for code in codes:
        logger.info(f'{"#"*30} code {code}')
        num = int(''.join(code[:3]))
        buttons = press_pad(code)
        cmplx += len(buttons) * num
        logger.info(f'complexity: {len(buttons), num}')
        #input()
    # output
    return cmplx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    args = parser.parse_args()
    tstart = time()
    ans = main(args.sample, args.part_two, args.loglevel)
    tstop = time()
    logger.info(f"runtime: {(tstop-tstart)*1e3:.3f} ms")
    print('ans ', ans)
