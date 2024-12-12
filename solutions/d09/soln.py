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


def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input; single line
    inp = next(read_line(fp))
    leng = len(inp)
    if leng % 2:
        last_id = leng // 2 
        right = leng - 1
    else:
        last_id = leng / 2 - 1
        right = leng - 2
    n_last = int(inp[right])
    # init pos to after first file since ID starts at 0
    pos = int(inp[0])
    left_id = 1
    file = False
    chksum = 0
    for blk in inp[1:]:
        blk = int(blk)
        if file:
            # logger.debug(f'{blk} file ID {left_id} @ {pos}')
            # incr pos and mult
            chksum += sum(p * left_id for p in range(pos, pos+blk))
            pos += blk
            left_id += 1
        else:
            # logger.debug(f'{blk} empty @ pos {pos}')
            # move from right to pos
            for _ in range(blk):
                if n_last == 0:
                    # logger.debug(f'file ID {last_id} moved; onto block {inp[right-2]}')
                    # move to next last file
                    right -= 2
                    n_last = int(inp[right])
                    last_id -= 1
                chksum += pos * last_id
                pos += 1
                n_last -= 1
        # logger.debug(f'chksum {chksum} new pos {pos}')
        if last_id <= left_id:
            # logger.debug(f'break at ID {last_id}')
            break
        file = not file
    for _ in range(n_last):
        chksum += pos * last_id
        pos += 1
    # output
    ans = chksum
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
