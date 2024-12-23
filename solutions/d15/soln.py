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

def convert_move(arrow: str) -> complex:
    match arrow:
        case "^":
            return -1j
        case "<":
            return -1+0j
        case ">":
            return 1+0j
        case "v":
            return 1j
        case _:
            return 0j
    
def render_wh(wh: dict, pos: complex, width: int, height: int) -> None:
    logger.info('render of current warehouse layout')
    for y in range(height):
        if 0 < y < height:
            row = ""
            for x in range(width):
                if pos == complex(x, y):
                    spot = '@'
                else:
                    spot = wh[complex(x, y)]
                row += spot
        else:
            row = '#' * width
        print(row)

def main(sample: bool, part_two: bool, loglevel: str, box='O', bot='@', wall='#', space='.'):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    wh = {}
    inp = read_line(fp)
    line = next(inp)
    y = 0
    pos = None
    while (line := line.strip()):
        # break once it reaches an empty line; move onto seq of movement
        for x, ch in enumerate(line):
            wh[complex(x, y)] = ch
        if not pos and (chk := line.find(bot)) >= 0:
            pos = complex(chk, y)
        y += 1
        line = next(inp)
    width, height = x+1, y
    #logger.debug(f'edges at 0 and width {wh[0j]} {wh[width+0j]}')
    logger.info(f'width {width} height {height}')
    moves = [convert_move(ch) for line in inp for ch in line.strip()]
    # execute
    # logger.debug(f'robot: {pos}\nboxes coord:\n{[p for p in wh if wh[p]]}\nmoves\n{moves}')
    # traverse
    for dxy in moves:
        # logger.debug(f'moving {dxy}')
        nx = pos + dxy
        if not (0 < nx.real < width) or not (0 < nx.imag < height):
            continue
        # check if box
        chk = nx
        to_move = []
        while wh[chk] == box:
            # exits if edge or empty
            logger.debug(f'box at {chk}: {wh[chk]}')
            to_move.append(chk)
            chk += dxy
        # check if wall at the end
        if wh[chk] == wall:
            continue
        # otherwise move all boxes
        pos = nx
        if to_move:
            wh[to_move[0]] = space
            wh[to_move[-1]+dxy] = box
            logger.debug(f'move box from {to_move[0]} to {to_move[-1]+dxy}')
    
    # output
    render_wh(wh, pos, width, height)
    ans = sum(100 * b.imag + b.real for b in wh if wh[b] == box)
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
