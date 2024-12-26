#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque, defaultdict

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main(sample: bool, part_two: bool, loglevel: str, wall='#', space='.'):
    """ 
    pathfinding, with cheats
    - disable collision for >=2 turns
    - cannot have 2 x 1 turn cheats, must be together
    - go through 1 layer of wall, essentially
    - keep dict(time_saved: num_cheats)
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
        ps_lim = 100
    else:
        fp = "sample.txt"
        ps_lim = 50
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    track = {complex(x, y): ch for y, line in enumerate(read_line(fp))
            for x, ch in enumerate(line.strip())}

    start = [p for p in track if track[p] == 'S'][0]
    fin = [p for p in track if track[p] == 'E'][0]
    logger.info(f'start @ {start}\tend @ {fin}')
    res = defaultdict(int) # defaults to 0
    # execute
    dxys = [-1, 1, 1j, -1j]
    pos = start
    picos = 0
    path = dict()
    while pos != fin:
        # no bfs needed; single track from start to finish
        logger.debug(f'at pos {pos}')
        path[pos] = picos
        for nx in [pos + dxy for dxy in dxys]:
            logger.debug(f'check nx {nx}')
            if nx in path:
                logger.debug(f'nx {nx} already in path')
                continue
            elif track[nx] == wall:
                logger.debug(f'nx {nx} is wall')
                continue
            else:
                pos = nx
                picos += 1
                logger.debug(f'new pos {nx}')
                break
    path[pos] = picos 
    logger.info(f'path:\n{len(path)-1} picosecs')

    skips = 20 if part_two else 2
    chks = []
    for x in range(-skips, skips+1):
        for y in range(-skips, skips+1):
            if 2 <= abs(x) + abs(y) <= skips:
                chks.append(complex(x,y))
    #logger.info(f'skip range: {chks}')
    # retrace no-skip path for possible wallskips
    for pos, picos in path.items():
        # look for other paths within 2 steps
        for nx in [pos + skip for skip in chks]:
            if nx in path and path[nx] > path[pos] + abs(skips.real) + abs(skips.imag):
                # +abs... to count the ps taken during the cheat
                # record shortcut
                res[path[nx] - path[pos] - abs(skips.real) - abs(skips.imag)] += 1

    ordered = sorted(res.items(), key=lambda tup: tup[0], reverse=True)
    logger.info(ordered)
    ans = (n for t, n in ordered if t >= ps_lim)
    logger.info(ans)
    # output
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
