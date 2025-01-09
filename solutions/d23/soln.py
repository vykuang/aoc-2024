#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import defaultdict

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
    lan = defaultdict(list)
    for line in read_line(fp):
        a, b = line.strip().split('-')
        # bidirectional edges
        lan[a].append(b)
        lan[b].append(a)
    logger.debug(f'lan: \n{lan}')
    # execute
    # look for trios - 
    trios = set()
    for c1 in lan:
        for c2 in lan[c1]:
            for c3 in lan[c2]:
                if not any(com[0] ==  't' for com in [c1, c2, c3]):
                    continue
                # look if c1 in any
                if c1 in lan[c3]:
                    # because regular sets are mutable
                    trio = frozenset((c1, c2, c3))
                    trios.add((trio))
                    logger.debug(f'trio: {trio}')

    # output
                    
    ans = len(trios)
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
