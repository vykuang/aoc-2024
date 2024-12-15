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


def main(sample: bool, part_two: bool, loglevel: str):
    """ 
    sample:
    5, 6, 5, 3, 1, 3, 5, 3, 5 = 36
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    grid = {complex(col, row): int(z)
            for row, line in enumerate(read_line(fp))
            for col, z in enumerate(line.strip())}
    
    heads = [xy for xy in grid if grid[xy] == 0]
    logger.debug(f'heads {heads}')
    dirs = (-1j, 1j, -1, 1)
    def hike(xy, path=set()):
        # base case
        path.add(xy)
        if grid[xy] == 9:
            logger.debug(f'reached 9 at {xy}')
            return 1
        # recursive; keep traversing and look for 9s
        score = 0
        for nx in [xy + dxy for dxy in dirs]:
            if nx in grid and nx not in path and grid[nx] == grid[xy] + 1:
                score += hike(nx, path)
        return score
    
    def count_paths(xy):
        """
        count number of valid paths
        """
        if grid[xy] == 9:
            logger.debug(f'reached 9 at {xy}')
            return 1
        # recursive; keep traversing and look for 9s
        num_paths = 0
        for nx in [xy + dxy for dxy in dirs]:
            if nx in grid and grid[nx] == grid[xy] + 1:
                # do not check if nx is already in path
                num_paths += count_paths(nx)
        return num_paths
    
    # scores = [hike(head) for head in heads]
    ans = []
    for head in heads:
        logger.debug(f"{'#'*10} - starting from {head} - {'#'*10}")
        if part_two:
            ans.append(count_paths(head))
        else:
            ans.append(hike(head, set()))
    logger.debug(f'answer: {ans}')

    # output
    return sum(ans)

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
