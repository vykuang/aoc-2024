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

def first_diff(nums) -> int:
    diffs = []
    for i in range(1, len(nums)):
        diffs.append(nums[i] - nums[i-1])
    return diffs
def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
        pluto = [8793800, 1629, 65, 5, 960, 0, 138983, 85629]
    else:
        fp = "sample.txt"
        pluto = [17]
    # logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    # execute
    if part_two:
        blinks = 75
    else:
        blinks = 25
    lengs = [len(pluto)]
    for n in range(blinks):
        i = 0
        # logger.debug(f'starting cycle {i}')
        while i < len(pluto):
            # splitting changes length of the array, not suitable with for-loop
            stone = pluto[i]
            # logger.debug(f'at pos {i} stone {stone}')
            if stone == 0:
                # logger.debug('zero to one')
                pluto[i] = 1
            elif len(st := str(stone)) > 1 and len(st) % 2 == 0:
                # split in half
                left = int(st[:len(st) // 2])
                right = int(st[len(st) // 2:])
                pluto[i] = left
                pluto.insert(i+1, right)
                i += 1
                # logger.debug(f'split in half; pos now at {i}')
            else:
                # logger.debug(f'mult {stone} @ pos {i} by 2024')
                pluto[i] *= 2024
            i += 1
        logger.info(f'{n}th cycle: {len(pluto)}')
        lengs.append(len(pluto))
    # output
    diffs = first_diff(lengs)
    for i in range(10):
        logger.info(f'{i+1}th diff: {diffs}')
        diffs = first_diff(diffs)
    ans = len(pluto)
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
