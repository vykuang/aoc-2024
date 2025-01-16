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

def parse_schema(schema: list[str], token='#') -> list[int]:
    """
    Parse to column heights 
    """
    # take xpose and count #
    schema = list(zip(*schema))
    cols = [-1] * len(schema)    
    for i, col in enumerate(schema):
        for ch in col:
            cols[i] += (ch == token)
    return cols

    
def main(sample: bool, part_two: bool, loglevel: str):
    """
    locks are schematics that are filled from top (stalagtites), and top is always filled
    top always filled
    bottom always empty
    keys are filled from bottom (stalacmites)
    bottom always filled
    top always empty
    . - empty space
    # - filled
    convert locks to list of column heights from top
    convert keys to list of column heights from bottom
    count unique pairs that fit
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    locks = []
    keys = []
    schema = []
    for line in read_line(fp):
        if not (line := line.strip()):
            # empty line means one whole schematic has been read
            # process last schematic
            if all('#' == ch for ch in schema[0]):
                locks.append(parse_schema(schema))
            else:
                keys.append(parse_schema(schema))
            schema = []
        else:
            schema.append(line)
    if all('#' == ch for ch in schema[0]):
        locks.append(parse_schema(schema))
    else:
        keys.append(parse_schema(schema))
    logger.info(f'locks\n{locks}\nkeys\n{keys}')
    # execute

    # output
    ans = None
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
