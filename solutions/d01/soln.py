#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import Counter

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

    # read input
    pairs = [map(int, line.split()) for line in read_line(fp)]
    
    # execute
    tstart = time()
    left, right = zip(*pairs)
    if not part_two:
        left = sorted(left)
        right = sorted(right)
        ans = sum(abs(a-b) for a, b in zip(left, right))
    else:
        # build counter using left as key
        cl = Counter(left)
        cr = Counter(right)
        # sum the key * vals in count
        ans = sum(cl[n] * n * cr[n] for n in cl)
        print(ans)
    # output
    tstop = time()
    logger.info(f"runtime: {(tstop-tstart):.3f} ms")
    return ans


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    args = parser.parse_args()
    ans = main(args.sample, args.part_two, args.loglevel)
    print('ans ', ans)
