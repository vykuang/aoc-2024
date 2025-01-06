#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def convert_move(arrow: str) -> complex:
    match arrow:
        case "^":
            return -1j
        case "<":
            return -1+0j
        case ">":
            return 1+0j
        case "v":
            return 1j
        case _:
            return 0j
    
def render_wh(wh: dict, pos: complex, width: int, height: int) -> None:
    logger.info(f'render of current warehouse layout; pos @ {pos}')
    for y in range(height):
        # if 0 < y < height:
        #     row = ""
        #     for x in range(width):
        #         if pos == complex(x, y):
        #             spot = '@'
        #         else:
        #             spot = wh[complex(x, y)]
        #         row += spot
        # else:
        #     row = '#' * width
        row = ''.join('@' if pos == complex(x,y) else str(wh[complex(x,y)])[:1] for x in range(width)) if 0 < y < height else '#' * width
        print(row)

def p1(sample: bool, part_two: bool, loglevel: str, box='O', bot='@', wall='#', space='.'):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    wh = {}
    inp = read_line(fp)
    line = next(inp)
    y = 0
    pos = None
    while (line := line.strip()):
        # break once it reaches an empty line; move onto seq of movement
        wh |= {complex(x, y): ch for x, ch in enumerate(line)}
        if not pos and (chk := line.find(bot)) >= 0:
            pos = complex(chk, y)
        y += 1
        line = next(inp)
    width = int(max(pos.real for pos in wh) + 1)
    height = y
    
    #logger.debug(f'edges at 0 and width {wh[0j]} {wh[width+0j]}')
    logger.info(f'width {width} height {height}')
    moves = [convert_move(ch) for line in inp for ch in line.strip()]

    # execute
    # logger.debug(f'robot: {pos}\nboxes coord:\n{[p for p in wh if wh[p]]}\nmoves\n{moves}')
    # traverse
    for dxy in moves:
        # logger.debug(f'moving {dxy}')
        nx = pos + dxy
        if not (0 < nx.real < width) or not (0 < nx.imag < height):
            continue
        # check if box
        chk = nx
        to_move = []
        while wh[chk] == box:
            # exits if edge or empty
            logger.debug(f'box at {chk}: {wh[chk]}')
            to_move.append(chk)
            chk += dxy
        # check if wall at the end
        if wh[chk] == wall:
            continue
        # otherwise move all boxes
        pos = nx
        if to_move:
            wh[to_move[0]] = space
            wh[to_move[-1]+dxy] = box
            logger.debug(f'move box from {to_move[0]} to {to_move[-1]+dxy}')
    
    # output
    render_wh(wh, pos, width, height)
    ans = sum(100 * b.imag + b.real for b in wh if wh[b] == box)
    return ans

def pushbox(pos, dxy, width, height, boxmap, wh) -> list:
    """
    keeps searching for more locations to check
    Returns list of boxes to be moved in dxy direction,
    or empty list if none can be moved due to obstruction
    """
    que = deque([pos])
    to_move = []
    while que:
        # nx: complex, reps loc of grid
        curr = que.popleft()
        nx = curr + dxy
        #if not (1 < nx.real < width-1) or not (0 < nx.imag < height) or wh[nx] == '#':
        if wh[nx] == '#':
            return []
        # empty space? continue down the queue
        elif wh[nx] == '.':
            continue
        # otherwise, look for other spots occupied by box
        boxid = wh[nx]
        if boxid in to_move:
            continue
        to_move.append(boxid)
        # add both and let to_move filter out those already processed
        que.append(boxmap[boxid])
        que.append(boxmap[boxid]+1)
    return to_move

def p2(sample: bool, loglevel: str, box='O', bot='@', wall='#', space='.'):
    """
    everything is twice as wide except for the robot
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    # read input
    boxmap = {}     # lookup xy from id
    wh = {}         # lookup obj from xy
    inp = read_line(fp)
    line = next(inp)
    y = 0
    boxid = 0
    while (line := line.strip()):
        for x, ch in enumerate(line):
            if ch == bot:
                pos = complex(2*x, y)
                ch = space
            xy1 = complex(2*x, y)
            xy2 = complex(2*x+1, y)
            if ch == box:
                ch = boxid
                # id lookup only returns left loc
                boxmap[boxid] = xy1 
                boxid += 1
                logger.debug(f'box {boxid} found')

            wh[xy1] = ch
            wh[xy2] = ch
            logger.debug(f'wh[{xy1}] = {ch}')
        y += 1
        line = next(inp)
    width = int(max(pos.real for pos in wh) + 1)
    height = y
    #logger.debug(f'edges at 0 and width {wh[0j]} {wh[width+0j]}')
    logger.info(f'width {width} height {height}')
    render_wh(wh, pos, width, height)
    moves = [convert_move(ch) for line in inp for ch in line.strip()]
    # traverse
    for dxy in moves:
        logger.debug(f'move {dxy}')
        if wh[pos+dxy] == space:
            pos += dxy
        elif (to_move := pushbox(pos, dxy, width, height, boxmap, wh)):
            pos += dxy
            while to_move:
                boxid = to_move.pop()
                logger.debug(f'moving box {boxid} @ {boxmap[boxid]} to {boxmap[boxid]+dxy}')
                wh[boxmap[boxid]] = space    # unreg wh 
                wh[boxmap[boxid]+1] = space    # unreg wh 
                boxmap[boxid] += dxy         # move box
                wh[boxmap[boxid]] = boxid      # update wh
                wh[boxmap[boxid]+1] = boxid      # update wh
    render_wh(wh, pos, width, height)
    
    # output
    ans = sum(100*pos.imag + pos.real for pos in boxmap.values())
    logger.info(f'p2 ans {ans}')
    return ans

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    args = parser.parse_args()
    tstart = time()
    #ans = p1(args.sample, args.part_two, args.loglevel)
    ans2 = p2(args.sample, args.loglevel)
    tstop = time()
    logger.info(f"runtime: {(tstop-tstart)*1e3:.3f} ms")
    print('ans ', ans, ans2)
