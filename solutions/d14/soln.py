#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from math import prod
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def tree_check(pos: set, width: int, tol=0.5) -> bool:
    """
    tests for horizontal reflection
    """
    mer = width // 2
    refl = 0
    checked = set()
    for x, y in pos:
        if (x, y) in checked:
            continue
        if x == mer:
            refl += 1
        elif x < mer and (mer + (mer - x), y) in pos:
            refl += 1
            checked.add((x,y))
        elif x > mer and (mer - (x - mer), y) in pos:
            refl += 1
            checked.add((x,y))
    return f'{refl/len(pos):.3f}', refl / len(pos) > tol
    
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

    # read input
    p = re.compile(r'([-]*\d+),([-]*\d+)')
    # for line in read_line(fp):
    #     vals = p.findall(line.strip())
    #     pos, vel = [complex(*list(map(int, num))) for num in vals]
    #     logger.debug(f'pos {pos} vel {vel}')

    # pos, vels = zip(*[[complex(*list(map(int, num))) for num in p.findall(line.strip())] 
    #         for line in read_line(fp)])
    pos, vels = zip(*[[list(map(int, num)) for num in p.findall(line.strip())] 
            for line in read_line(fp)])
    # execute
    xavgs = []
    pos = list(pos)
    logger.info(f'{len(pos)} robots')
    for sec in range(seconds):
        xavg = 0
        for rb in range(len(pos)):
            pos[rb][0] += vels[rb][0]
            pos[rb][1] += vels[rb][1]
            # width = 101; if pos.real = 101, that puts its out of bound 
            # bc of 0-index. but 101 % width = 0 which wraps it back so it works
            pos[rb][0] %= width
            pos[rb][1] %= height
            xavg += pos[rb][0]
        #ptree = tree_check(rbmap, width)
        xavg /= len(pos)
        xavgs.append((xavg, sec))
        if abs(xavg - width//2) < 0.5:
            logger.info(f'xavg {xavg} @ {sec}')
    
    xavgs.sort(key=lambda p: abs(width//2-p[0]))
    logger.info(f'closest to mer: {xavgs[:10]}')
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
