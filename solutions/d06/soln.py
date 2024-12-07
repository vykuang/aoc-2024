#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from collections import defaultdict, namedtuple
#from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

Point = namedtuple('Point', ['row', 'col'])

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main(sample: bool, part_two: bool, loglevel: str, guard: str = '^'):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    # execute
    # find starting pos
    p_obs = re.compile(r'#')
    p_g = re.compile(r'\^')
    colmap = defaultdict(list)
    rowmap = defaultdict(list)
    pos = None
    for i, line in enumerate(read_line(fp)):
        m_obs = p_obs.finditer(line)
        for m in m_obs:
            colmap[m.start()].append(i)
            rowmap[i].append(m.start())
        if not pos and (m_g := p_g.search(line)):
            pos = Point(i, m_g.start())
    height, width = i, len(line)
    #logger.debug(f'colmap\n{colmap}\nrowmap\n{rowmap}\nstart {pos_g}')
    visited = set()
    # real: row movement; imag: col movement; 0, -1 = -1j -> moving up
    dxy = complex(0, -1)
    # exit con: if guard is at the edge, they will always exit
    while 0 < pos.row < height and 0 < pos.col < width:
        # move the guard
        if dxy.real == -1:
            logger.debug('moving left')
            # populate lane with possible obs, and check if any
            lane = [o for o in rowmap[pos.row] if o < pos.col]
            # when pos updates to 0, it will exit from while
            obs = -1 if not lane else max(lane)
            logger.debug(f'obs @ {pos.row, obs}')
            path = [Point(pos.row, col) for col in range(obs+1, pos.col)]
            pos = Point(pos.row, obs + 1)
            # look for max
        elif dxy.real == 1:
            logger.debug('moving right')
            lane = [o for o in rowmap[pos.row] if o > pos.col]
            obs = width+1 if not lane else min(lane)
            logger.debug(f'obs @ {pos.row, obs}')
            path = [Point(pos.row, col) for col in range(pos.col, obs)]
            pos = Point(pos.row, obs - 1)
        elif dxy.imag == -1:
            logger.debug('moving up')
            lane = [o for o in colmap[pos.col] if o < pos.row]
            obs = -1 if not lane else max(lane)
            logger.debug(f'obs @ {obs, pos.col}')
            path = [Point(row, pos.col) for row in range(obs+1, pos.row)]
            pos = Point(obs + 1, pos.col)
        elif dxy.imag == 1:
            logger.debug('moving down')
            lane = [o for o in colmap[pos.col] if o > pos.row]
            obs = height+1 if not lane else min(lane)
            logger.debug(f'obs @ {obs, pos.col}')
            path = [Point(row, pos.col) for row in range(pos.row, obs)]
            pos = Point(obs-1, pos.col)
        
        logger.debug(f'update path: {path}')
        # turn CW 90deg
        dxy /= -1j
        logger.debug(f'new pos {pos} facing {dxy}')
        visited.update(path)
    # output
    ans = len(visited)
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
    logger.info(f"runtime: {(tstop-tstart):.3f} ms")
    print('ans ', ans)
