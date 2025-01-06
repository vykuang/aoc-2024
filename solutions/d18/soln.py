#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

dxys = [-1, 1, -1j, 1j]

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def render_mem(side: int, bad: set, path: list = []) -> None:
    for y in range(side):
        row = []
        for x in range(side):
            pos = '#' if complex(x, y) in bad else '.'
            pos = 'O' if path and complex(x,y) in path else pos
            row.append(pos)
        print(''.join(row))
        
def find_path(bad: set(), side: int, start: complex = 0j) -> bool:
    """
    Returns whether or not a valid path is possible given
    params:
    bad: set, pos of obstacles
    side: side length of area
    start: complex, starting position

    returns: bool
    """
    end = side-1+(side-1) * 1j
    visited = set()
    todo = deque([(start, set())])
    while todo:
        curr, path = todo.popleft()
        if curr == end:
            #render_mem(side, bad, path)
            return path
        # bytes start falling after taking the first step
        if curr in visited or curr in bad or not 0 <= curr.real < side or not 0 <= curr.imag < side:
            logger.debug('visited or corrupt or outside')
            continue
        visited.add(curr)
        for nx in [curr + dxy for dxy in dxys]:
            todo.append((nx, path.union([curr])))
    return None
def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
        side = 71
        n_fallen = 1024
    else:
        fp = "sample.txt"
        side = 7
        n_fallen = 12
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    incs = []
    for line in read_line(fp):
        x, y = line.split(',')
        incs.append(complex(int(x), int(y)))
    # execute
    logger.debug(f'{len(incs)} bytes\n{incs}')
    bad = set(incs[:n_fallen]) # start here for p2 as well
    path = find_path(bad=bad, side=side)
    p1 = len(path)
    nbytes = n_fallen
    for byte in incs[n_fallen:]:
        bad.add(byte)
        nbytes += 1
        if byte not in path:
            continue
        if not (path := find_path(bad=bad, side=side)):
            p2 = nbytes, byte
            break
    # output
    return p1, p2

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
