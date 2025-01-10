#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque

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
BUTTON_MAP = {1:'>',-1:'<',1j:'v',-1j:'^'}

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def dist_to_buttons(dist: complex, pos, is_num: bool = False) -> str:
    """
    given a complex representing the manhattan dist
    return direction in terms of arrows
    e.g. 1+2j -> '>vv'
    caveat: must avoid the 'gap', need current pos context
    Moves in same dir must be contiguous chunks to avoid
    switching back and forth
    either go left/right first, or up/down first
    If both dirs are valid, and neither go over the gap,
    then both must be considered in order to choose the shortest
    sequence...
    """
    logger.debug(f'dist, pos: {dist, pos}')
    # try left-right first
    xstep = 0 if not dist.real else int(dist.real / abs(dist.real))
    ystep = 0 if not dist.imag else dist.imag / abs(dist.imag) * 1j
    pad = NUMPAD if is_num else DPAD
    xs = [] if not xstep else [BUTTON_MAP[xstep]] * int(abs(dist.real))
    ys = [] if not ystep else [BUTTON_MAP[ystep]] * int(abs(dist.imag))
    logger.debug(f'xstep, ystep {xstep, ystep}')
    if xstep:
        chkgap = [pad[pos + dxy] for dxy in range(xstep, int(dist.real)+xstep, xstep)]
        logger.debug(f'chkgap {chkgap}')
        if None in chkgap:
            # move up-down first
            buttons = ys + xs
        else: # must compare x + y vs y + x
            # but check if gap is in y-dir
            chkgap = [pad[pos + dxy] for dxy in range(xstep, int(dist.real)+xstep, xstep)]
            buttons = xs + ys
    else:
        buttons = ys
    logger.debug(f'buttons {buttons}')
    return ''.join(buttons)

def press_numpad(code: str) -> list:
    """
    return movement and presses required for the code
    """
    pos = NUMPOS['A']
    buttons = ''
    #logger.debug(f'processing code {code}')
    for key in code:
        dist = NUMPOS[key] - pos
        logger.debug(f'{NUMPAD[pos],key}: {dist}')
        buttons += dist_to_buttons(dist, pos, True)
        buttons += 'A'
        pos = NUMPOS[key]
    return buttons
    
def press_dpad(cmds: str) -> list:
    """
    return movement and presses required for dpad
    """
    pos = DPOS['A']
    buttons = ''
    for press in cmds:
        dist = DPOS[press] - pos
        #logger.debug(f'{DPAD[pos],press}: {dist}')
        buttons += dist_to_buttons(dist, pos)
        buttons += 'A'
        pos = DPOS[press]
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

    # read input
    codes = [line.strip() for line in read_line(fp)]

    # execute
    cmplx = 0
    for code in codes:
        logger.info(f'{"#"*30} code {code}')
        num = int(code[:3])
        buttons = press_numpad(code)
        logger.info(f'numpad buttons {buttons}')
        logger.info(f'{"-"*30} first layer complete')
        buttons = press_dpad(buttons)
        # buttons = press_dpad(buttons)
        cmplx += len(buttons) * num
        logger.info(f'num: {num}')
        logger.info(f'dpad movements {len(buttons), buttons}')
    # output
    ans = cmplx
    return ans

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
