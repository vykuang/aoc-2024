#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from math import log10

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main(sample: bool, part_two: bool, loglevel: str, blinks: int = 25):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    pluto = [125, 17]
    # execute
    for _ in range(blinks):
        while i < len(pluto):
            stone = pluto[i]
            # splitting changes length of the array, not suitable with for-loop
            if stone == 0:
                pluto[i] = 1
            elif len(st := str(stone)) > 1 and len(st) % 2 == 1:
                # split in half
                left = int(st[:len(st) // 2])
                right = int(st[len(st) // 2:])
                pluto[i] = left
                


    # output
    ans = None
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
