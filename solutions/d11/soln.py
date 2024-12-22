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
    cache = {}
    def blink(stone, blinks):
        """
        Recursively solve using cache in outside scope
        """
        # base: finished blinking
        if blinks == 0:
            # no more div; return 1 == len(stone)
            return 1
        # hit cache first for length
        if (key := (stone, blinks)) in cache:
             return cache[key]
        if stone == 0:
            # logger.debug('zero to one')
            res = blink(1, blinks-1)
        elif len(st := str(stone)) > 1 and len(st) % 2 == 0:
            # split in half
            left = blink(int(st[:len(st) // 2]), blinks-1)
            right = blink(int(st[len(st) // 2:]), blinks-1)
            res = left + right
            # logger.debug(f'split in half; pos now at {i}')
        else:
            # logger.debug(f'mult {stone} @ pos {i} by 2024')
            res = blink(stone * 2024, blinks-1)
        # cache the result
        cache[key] = res
        return res

    ans = sum(blink(stone, blinks) for stone in pluto)
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
