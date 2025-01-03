#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from math import prod
from statistics import pstdev
from collections import Counter
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def tree_check(pos: list, width: int, height: int, stdev_x: int = 5, stdev_y: int = 5) -> bool:
    """
    instead of checking for reflection centered on the meridian,
    count n_robots for each row/col at each cycle
    assume mu = n_robots / nrow or ncol
    compare new count with past accum. stdev.
    if > 3 stdev, render for visual inspection
    assumes that the population mean should be centred on the
    meridian/equator (half of width/height)
    """
    xs, ys = zip(*pos)
    nxs = Counter(xs)
    nys = Counter(ys)
    # for each row/col, compare the count vs existing mean and take the z-val
    mu_x = len(pos) / width
    mu_y = len(pos) / height
    z_xs = [(nx - mu_x)/stdev_x for nx in nxs.values()]
    z_ys = [(ny - mu_y)/stdev_y for ny in nys.values()]
    logger.debug(f'max zx {max(z_xs)}\tmax zy{max(z_ys)}')
    return any(zx > 3 for zx in z_xs) or any(zy > 3 for zy in z_ys)

    
def render(pos: list, width: int, height: int) -> None:
    """
    renders the live pos of all robots
    # - robot; . for space
    """
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x, y in pos:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))

def main(sample: bool, part_two: bool, loglevel: str, seconds: int = 100):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
        height = 103
        width = 101
    else:
        fp = "sample.txt"
        height = 7
        width = 11
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')
    if part_two:
        seconds = 100000
    # read input
    p = re.compile(r'([-]*\d+),([-]*\d+)')
    pos, vels = zip(*[[list(map(int, num)) 
            for num in p.findall(line.strip())] 
            for line in read_line(fp)])
    # execute
    xavgs = []
    pos = list(pos)
    logger.info(f'{len(pos)} robots')
    for sec in range(seconds):
        xavg = 0
        for rb in range(len(pos)):
            pos[rb][0] = (pos[rb][0] + vels[rb][0]) % width
            pos[rb][1] = (pos[rb][1] + vels[rb][1]) % height
            # width = 101; if pos.real = 101, that puts its out of bound 
            # bc of 0-index. but 101 % width = 0 which wraps it back so it works
        if part_two and tree_check(pos, width, height):
            logger.info(f'end of {sec} seconds')
            render(pos, width, height)
            input('press to render next second')
    # count in quadrants
    quads = [0] * 4
    eq = height // 2
    mer = width // 2
    for x, y in pos:
        if x < mer:
            if y < eq:
                # top left
                quads[0] += 1
            elif y > eq:
                # bot left
                quads[3] += 1
        elif x > mer:
            if y < eq:
                # top right
                quads[1] += 1
            elif y > eq:
                # bot right
                quads[2] += 1
    logger.info(f'quads {quads}')
    # output
    ans = prod(quads)
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
