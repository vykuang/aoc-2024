#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque
from itertools import accumulate

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input into map
    garden = {}
    for j, line in enumerate(read_line(fp)):
        for i, plant in enumerate(line.strip()):
            garden[complex(i, j)] = plant

    # flood search
    # tuple(pos, heading)
    que = deque([(complex(0,0), 1+0j)])
    visited = set()
    ans = 0
    dxys = [-1,1,-1j,1j]
    def side_search(pos, heading, area, edges, sides):
        """
        dfs to always check left of prev heading first
        """
        # base cases
        if pos not in garden:
            edges += 1
            return
        dxys = accumulate([-1j] * 4, lambda x, y: x * y, initial=-1j)
        for nx in [pos + dxy for dxy in dxys[1:]]:
            # start with left first
            side_search(nx, nx - pos)




    while que:
        curr, heading = que.popleft()
        logger.debug(f'searching from {curr} for {garden[curr]}')
        if curr in visited:
            continue
        # new region, search 4 cardinal
        logger.debug('start new region')
        search = deque([curr, heading])
        edges = 0
        area = 0
        while search:
            pos, heading = search.popleft()
            logger.debug(f'checking {garden[pos]} at pos {pos}')
            if pos in visited:
                logger.debug(f'{pos} already visited')
                continue
            area += 1
            logger.debug(f'{area}th {garden[pos]} at {pos}')
            visited.add(pos)
            # dynamically generate new dxys to always turn left from current
            for nx in [pos + dxy for dxy in dxys]:
                if nx not in garden:
                    edges += 1
                    logger.debug(f'{edges}th edge at {nx}: bounds')
                    continue
                if garden[nx] != garden[curr]:
                    edges += 1
                    que.append(nx)
                    logger.debug(f'{edges}th edge at {nx}: new plant')
                    continue
                # otherwise, in garden and same type
                logger.debug(f'add {nx} to continue searching for {garden[nx]}')
                search.append(nx)
        ans += edges * area
        logger.info(f'region of {garden[curr]} has a={area} and pi={edges}')
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
