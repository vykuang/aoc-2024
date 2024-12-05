#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from itertools import product

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

dx = [-1, 0, 1]
dxys = [p for p in product(dx, dx) if p != (0, 0)]
#corners = [p for p in product([-1,1],[-1,1])]
corners = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


            
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
    # grid of letters
    grid = [line for line in read_line(fp)]
    height = len(grid)
    width = len(grid[0])
    # execute
    starts = [(i, j) for i in range(height) 
            for j in range(width)
            if grid[i][j] == 'X']
    ans = 0
                
    word = 'XMAS'
    for xi, xj in starts:
    # initiate search in 8 dir for each 'X'
        for dx, dy in dxys:
            seq = 1
            i, j = xi, xj
            while seq < len(word) and 0 <= i + dx < height and 0 <= j + dy < width and grid[i+dx][j+dy] == word[seq]:
                seq += 1
                i += dx
                j += dy
            if seq == 4:
                ans += 1

    def check_mas(ai, aj) -> bool:
        """
        Given coordinate ai, aj, check for x-shaped MAS
        always check from top left, clockwise,
        before rotating
        """
        logger.debug(f'check A at {ai, aj}')
        for combo in ['MMSS', 'MSSM', 'SSMM', 'SMMS']:
            logger.debug(f'checking for seq {combo}')
            count = 0
            for i, (dx, dy) in enumerate(corners):
                try:
                    logger.debug(f'{grid[ai + dx][aj + dy]} = {combo[i]}?')
                except IndexError:
                    pass
                if 0 <= ai + dx < height and 0 <= aj + dy < width and grid[ai + dx][aj + dy] == combo[i]:
                    count += 1
                    logger.debug(f'count {count}')
                    if count == 4:
                        logger.debug(f'mas found at {(ai,aj)}')
                        return True
                else:
                    # move onto next combo
                    logger.debug(f'fail combo {combo}')
                    break
        return False
    starts = [(i, j) for i in range(height) 
            for j in range(width)
            if grid[i][j] == 'A']
    p2 = sum(check_mas(i, j) for i, j in starts)
    # output
    return p2

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
