#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from operator import add, mul
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def is_valid(test: int, eqns: list[int]):
    """
    bfs with + and * as children nodes
    """
    logger.debug(f'test {test} eqns {eqns}')
    idx = 1
    que = deque([(eqns[0], idx)])
    while que:
        curr, idx = que.popleft()
        logger.debug(f'ccurr {curr} idx {idx}')
        if idx == len(eqns) and curr == test:
            logger.debug('yay')
            return test
        if curr >= test and idx < len(eqns) - 1:
            continue
        if idx >= len(eqns):
            continue
        for op in [add, mul]:
            que.append((op(curr, eqns[idx]), idx+1))
        
        # part two, add concatenation
        que.append((int(str(curr) + str(eqns[idx])), idx+1))
    logger.debug('boo')
    return 0

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    ans = 0
    # read input
    for line in read_line(fp):
        test, nums = line.split(':')
        eqns = [int(n) for n in nums.split()]
        ans += is_valid(int(test), eqns)

    # execute

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
