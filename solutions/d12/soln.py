#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import deque, defaultdict
from itertools import accumulate

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


dxys = [-1,1,-1j,1j]

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def count_sides(edges: dict) -> int:
    """
    Look for gaps in the value
    """
    sides = 0
    for k in edges:
        logger.debug(f'edges {k}: {edges[k]}')
        sides += 1
        if len(edges[k]) < 2:
            logger.debug(f'add 1 side: {sides}')
            continue
        # vital to look for gaps
        edges[k].sort()
        prev = edges[k][0]
        for e in edges[k][1:]:
            sides += (e - prev) > 1
            prev = e
        logger.debug(f'{sides} sides')
    return sides

def side_search(pos, garden, visited):
    """
    collect all edges
    references
    """
    # base cases
    search = deque([pos])
    hedges = defaultdict(list)
    vedges = defaultdict(list)
    area = 0
    edges = 0
    while search:
        pos = search.popleft()
        #logger.debug(f'checking {garden[pos]} at pos {pos}')
        if pos in visited:
            #logger.debug(f'{pos} already visited')
            continue
        area += 1
        logger.debug(f'{area}th {garden[pos]} at {pos}')
        visited.add(pos)
        for nx in [pos + dxy for dxy in dxys]:
            if nx not in garden or garden[nx] != garden[pos]:
                edges += 1
                # collect edges to count sides
                if (d := (nx - pos)) in [-1, 1]:
                    # vertical edges
                    col = pos.real if d == -1 else pos.real+1
                    vedges[col, d].append(pos.imag)
                else:
                    # horiz edge
                    row = pos.imag if d == -1j else pos.imag+1
                    hedges[row, d].append(pos.real)
                #logger.debug(f'{edges}th edge at {nx}: bounds')
                continue
            # otherwise, in garden and same type
            search.append(nx)
    # count sides
    logger.debug(f'hori edges: {hedges}\nvert edges {vedges}')
    sides = sum(count_sides(e) for e in (hedges, vedges))
    logger.debug(f'total sides {sides}')
    return area, edges, sides, visited

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input into map
    garden = {}
    for j, line in enumerate(read_line(fp)):
        for i, plant in enumerate(line.strip()):
            garden[complex(i, j)] = plant

    # flood search
    # tuple(pos, heading)
    visited = set()
    p1 = p2 = 0
    for pos in garden:
        if pos in visited:
            continue
        logger.info(f'{"-"*10} {garden[pos]} @ {pos}')
        a, e, s, visited = side_search(pos, garden, visited)
        logger.info(f'area {a}\tedges {e}\t sides {s}')
        p1 += a * e
        p2 += a * s
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
