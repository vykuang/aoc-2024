#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from math import inf
from functools import cache
from sys import setrecursionlimit

setrecursionlimit(10000)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f
@cache
def min_tokens_i(axy, bxy, target, tokens=0, na=0, nb=0) -> int:
    """
    either spend 3 tokens to press A or 1 to press B
    """
    if target == 0+0j:
        return tokens
    elif target.imag < 0 or target.real < 0 or na > 100 or nb > 100:
        return inf
    else:
        a = min_tokens(axy, bxy, target - axy, tokens+3, na+1, nb)
        b = min_tokens(axy, bxy, target - bxy, tokens+1, na, nb+1)
        return min(a, b)

def min_tokens(axy, bxy, target) -> int:
    """
    greedy approach
    start with all B, then incrementally replace with As
    first hit must be the minimum
    """
    nb = target.real // bxy.real
    na = 0
    while nb >= 0:
        if nb * bxy.real + na * axy.real == target.real and nb * bxy.imag + na * axy.imag == target.imag:
            return nb + 3 * na
        nb -= 1
        na = (target.real - nb * bxy.real) // axy.real
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

    # read input
    claws = []
    claw = {}
    p_nums = re.compile(r'X[+=](\d+),.*Y[+=](\d+)')
    for line in read_line(fp):
        m = p_nums.search(line)
        if not m:
            claws.append(claw)
            claw = {}
            continue
        x, y = [int(n) for n in m.group(1,2)]
        xy = complex(x, y)
        if 'A:' in line:
            claw['A'] = xy
        elif 'B:' in line:
            claw['B'] = xy
        else:
            if part_two:
                xy += 10000000000000 + 10000000000000j
            claw['target'] = xy
    # one last claw to be appended
    claws.append(claw)

    logger.info(f'{len(claws)} claws in total')
    # dynamic prog to minimize token use
    ans = 0
    for claw in claws:
        tokens = min_tokens(claw['A'], claw['B'], claw['target'])
        #ans += tokens if tokens < inf else 0
        ans += tokens
        logger.info(f"target: {claw['target']} tokens {tokens}; total {ans}")

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
