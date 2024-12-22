#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import heapq
from collections import defaultdict
from math import inf

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

class Deer:
    """
    Custom class for heapq to sort only by the score
    otherwise heapq sorts by all elements of the tuple???
    """
    def __init__(self, score, pos, dxy, steps=[]):
        self.score = score
        self.pos = pos
        self.dxy = dxy
        self.steps = steps
    def __lt__(self, other):
        return self.score < other.score

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main(sample: bool, part_two: bool, loglevel: str, cmove=1, cturn=1000, wall='#'):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    maze = {complex(x, y): ch for y, line in enumerate(read_line(fp))
            for x, ch in enumerate(line.strip())}

    deer = [p for p in maze if maze[p] == 'S'][0]
    fin = [p for p in maze if maze[p] == 'E'][0]
    # finding all best paths means allowing going through same spots
    # for different paths
    todo = [Deer(0, deer, 1+0j)] # heapq by default sorts by 0th tuple element
    heapq.heapify(todo)
    best = None
    # keep map of (pos, dx) and best past score
    visited = defaultdict(lambda: inf)
    while todo:
        curr = heapq.heappop(todo)
        #logger.debug(f'@ {curr.pos, curr.dxy}')
        if curr.pos == fin:
            # curr.steps += [fin] # just add 1 at the end
            if not best:
                # use first path found as the standard
                best = curr.score
                paths = set(curr.steps)
                logger.info(f'first path score {best} with {len(curr.steps)+1} tiles')
            elif curr.score == best:
                paths.update(curr.steps)
                logger.info(f'another path found; tiles updated to {len(paths)+1}')
            else:
                break
        elif curr.pos in curr.steps or \
            maze[curr.pos] == wall or \
            curr.score > visited[(curr.pos, curr.dxy)]:
            # prune
            continue
        # child nodes: turn 90deg or move forward
        visited[(curr.pos, curr.dxy)] = curr.score
        heapq.heappush(todo, Deer(curr.score+cmove, curr.pos + curr.dxy, curr.dxy, curr.steps + [curr.pos]))
        heapq.heappush(todo, Deer(curr.score+cturn, curr.pos, curr.dxy / -1j, curr.steps))
        heapq.heappush(todo, Deer(curr.score+cturn, curr.pos, curr.dxy * -1j, curr.steps))

    # output
    ans = best, len(paths)
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
