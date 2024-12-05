#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from functools import reduce

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def memmul(csum: int, grps: re.match) -> int:
    return csum + int(grps.group(1)) * int(grps.group(2))

def main(sample: bool, part_two: bool, loglevel: str):
    """
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    mems = "".join(line for line in read_line(fp))
    # execute
    ans = 0
    p = re.compile(r"mul\((\d+),(\d+)\)")
    if not part_two:
        ans = reduce(memmul, p.finditer(mem), 0)
    else:
        pa = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")
        enable = True
        for a, b, do, dn in pa.findall(mems):
            # findall returns all hits sequentially
            if a and b:
                ans += int(a) * int(b) * enable
            elif do or dn:
                # if only don't() found, bool(do) = False
                # since do will be None
                enable = bool(do)

        # split by "don't()"
        # find first instance of "do()"
        p_do = re.compile(r"do\(\)")
        segments = mems.split("don't()")
        logger.debug(f'segments\n{segments}')
        # handle beginning as edge case since all are enabled
        ans = reduce(memmul, p.finditer(segments[0]), 0)
        for sgmt in segments[1:]:
            if (do := p_do.search(sgmt)):
                # .search() returns a match obj if hit; None if not found
                enabled = sgmt[do.end():]
                logger.debug(f'enabled: {enabled}')
                logger.debug(f'do found at {do.start()}')
                ans = reduce(memmul, p.finditer(enabled), ans)
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
    logger.info(f"runtime: {(tstop-tstart):.3f} ms")
    print('ans ', ans)
