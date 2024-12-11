#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import defaultdict
from itertools import combinations

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

    # read antenna map
    antmap = defaultdict(list)
    for i, line in enumerate(read_line(fp)):
        for j, ch in enumerate(line.strip()):
            if ch == '.':
                continue
            antmap[ch].append((i, j))
    height, width = i, j
    # execute
    def in_bounds(point: tuple) -> bool:
        return 0 <= point[0] <= height and 0 <= point[1] <= width

    locs = set()
    for fr in antmap:
        logger.debug(f'pairs for freq {fr}')
        for aa, ab in combinations(antmap[fr], r=2):
            logger.debug(f'pair {aa, ab}')
            d = ab[0] - aa[0], ab[1] - aa[1]
            a1 = aa[0] - d[0], aa[1] - d[1]
            a2 = ab[0] + d[0], ab[1] + d[1]
            if part_two:
                locs.add(aa)
                locs.add(ab)
                # also need to add locs of antenna itself
                while in_bounds(a1):
                    locs.add(a1)
                    a1 = a1[0] - d[0], a1[1] - d[1]
                while in_bounds(a2):
                    locs.add(a2)
                    a2 = a2[0] + d[0], a2[1] + d[1]
            else:
                if in_bounds(a1):
                    logger.debug('a1 in')
                    locs.add(a1)
                if in_bounds(a2):
                    logger.debug('a2 in')
                    locs.add(a2)
    logger.debug(f'antinodes {locs}')
    ans = len(locs)
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
