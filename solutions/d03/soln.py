#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from itertools import chain
from functools import reduce

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
sample = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def memmul(csum: int, grps: re.match) -> int:
    return csum + int(grps.group(1)) * int(grps.group(2))

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
    # execute
    p = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
    if not part_two:
        ans = 0
        for mem in read_line(fp):
            ans += reduce(memmul, p.finditer(mem), 0)
    else:
        p1 = re.compile(r"^.*don't\(\)")
        p2 = re.compile(r"do\(\).*don't\(\)")
        p2 = re.compile(r"do\(\).*$")
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
