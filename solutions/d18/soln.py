#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


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
        
def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
        side = 71
    else:
        fp = "sample.txt"
        side = 7
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    incs = []
    for line in read_line(fp):
        x, y = line.split(',')
        incs.append(complex(int(x), int(y)))
    #falling = [complex(int(xy[0]), int(xy[1])) for line in read_line(fp) for xy in line.strip().split(',')]
    
    #falling = [complex(int(x), int(y)) for x, y in line.split(',') for line in read_line(fp)]
    # execute
    logger.debug(f'{len(incs)} bytes\n{incs}')
    start = (0, 0j, [0j])
    end = side-1+(side-1) * 1j
    logger.info(f'end {end}')
    todo = deque([start])
    visited = set()
    n_fallen = 1024
    bad = set(incs[:n_fallen])
    dxys = [-1, 1, -1j, 1j]
    while todo:
        steps, curr, path = todo.popleft()
        logger.debug(f'at {curr} after {steps} steps')
        if curr == end:
            render_mem(side, bad, path)
            ans = steps
            break
        # bytes start falling after taking the first step
        if curr in visited:
            logger.debug('visited')
            continue
        if curr in bad:
            logger.debug('corrupt')
            continue
        visited.add(curr)
        if not 0 <= curr.real < side or not 0 <= curr.imag < side:
            logger.debug('out of bounds')
            continue
        if steps > n_fallen:
            bad.add(incs[n_fallen])
            logger.debug(f'block corrupted at step {steps}: {incs[n_fallen]}')
            #render_mem(side, bad)
            n_fallen = steps
        for nx in [curr + dxy for dxy in dxys]:
            todo.append((steps+1, nx, path + [curr]))

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
