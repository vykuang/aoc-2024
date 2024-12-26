#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
# from functools import cache

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

# @cache
cache = {}
def is_possible(pattern: str, linens: tuple[str]) -> bool:
    """
    Top-down recursion?
    keep past towels for debug
    """
    if not pattern:
        return True
    if pattern in cache:
        return cache[pattern]
    ans = False
    for towel in linens:
        # logger.debug(f'{towel} match?')
        if towel == pattern[:len(towel)]:
            # logger.debug('match')
            ans |= is_possible(pattern[len(towel):], linens)
    cache[pattern] = ans
    return ans

n_cache = {}
def count_possible(pattern: str, linens: tuple[str]) -> int:
    """
    count how many are possible
    """
    if not pattern:
        return 1
    if pattern in n_cache:
        return n_cache[pattern]
    ans = 0
    for towel in linens:
        # logger.debug(f'{towel} match?')
        if towel == pattern[:len(towel)]:
            # logger.debug('match')
            ans += count_possible(pattern[len(towel):], linens)
    n_cache[pattern] = ans
    return ans

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    # logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    inp = read_line(fp)
    linens = tuple(p.strip() for p in next(inp).strip().split(','))
    logger.info(f'{len(linens)} linens available')
    # skip blank
    next(inp)
    valid = poss = 0
    for pattern in inp:
        # logger.debug(f'checking {pattern.strip()}')
        valid += 1 if is_possible(pattern.strip(), linens) else 0
        poss += count_possible(pattern.strip(), linens)
        # input()
    # execute

    # output
    return valid, poss

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
