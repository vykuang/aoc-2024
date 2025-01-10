#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def sim_secret(seed: int, cycles: int, mult=64, prune=16777216,div=32,mult2=2048) -> int:
    logger.debug(f'seed: {seed}')
    secret = seed
    for _ in range(cycles):
        mix = secret * mult
        secret ^= mix
        secret %= prune
        mix = secret // div
        secret ^= mix
        secret %= prune
        mix = secret * mult2
        secret ^= mix
        secret %= prune
    logger.debug(f'secret: {secret}')
    return secret

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    cycles = 2000
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    secrets = [sim_secret(int(seed), cycles) for seed in read_line(fp)]
    # execute

    # output
    ans = sum(secrets)
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
