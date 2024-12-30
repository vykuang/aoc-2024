#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from itertools import accumulate

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
    inp_init = [int(n) for n in next(read_line(fp)).strip()]
    inp = inp_init.copy()
    leng = len(inp)
    # prefix sums that rep disk pos at each block
    disk_init = list(accumulate(inp, lambda a, b: a + b))
    disk_init = [0] + disk_init
    disk = disk_init.copy()
    logger.debug(f'disk pos of each blk\n{disk}')
    if leng % 2:
        # odd: last is file
        last_id = leng // 2 
        right = leng - 1
    else:
        # even: 2nd last is file
        last_id = leng / 2 - 1
        right = leng - 2
    # init pos to after first file since ID starts at 0 which does not contribute to checksum
    blk_init = 1
    p2 = 0
    # init first block pos and store it
    if part_two:
        while last_id > 0:
            #logger.debug(f'{"-"*10}\nprocessing file id {last_id} size {inp[right]}')
            # find earlist block with enough space for n_last
            blk = blk_init
            while blk < right and inp[blk] < inp[right]:
                blk += 2 
            # break b/c of suff. space or end of line?
            if blk < right:
                # update storage
                #logger.debug(f'{inp[blk]} blk @ {blk} used {inp[right]}')
                inp[blk] -= inp[right]
                # don't update blk_init; just iterate thru the zeros
                start = disk[blk]
                # update disk[blk] after using
                disk[blk] += inp[right]
            else:
                logger.debug('no movement')
                start = disk[right]
            p2 += (2 * start + inp[right] - 1) * inp[right] / 2 * last_id
            # move onto to next
            right -= 2
            last_id -= 1
        logger.info(f'p2 chksum {p2}')
    # part one - full fragmentation
    last_id = leng // 2
    right = leng - 1
    inp = inp_init
    disk = disk_init
    blk = blk_init
    p1 = 0
    while blk < right:
        # each cycle completes 1 file ID
        #logger.debug(f'{"-"*10}\nprocessing file id {last_id} size {inp[right]}')
        while inp[right]:
            while not inp[blk]:
                blk += 2
            if blk > right:
                break
            #logger.debug(f'file {last_id} at pos {disk[blk]}')
            p1 += last_id * disk[blk]
            inp[blk] -= 1
            disk[blk] += 1
            inp[right] -= 1
            #for pos in range(disk[blk], disk[blk] + inp[blk]):
        #logger.debug(f'chksum: {p1}')
        last_id -= 1
        right -= 2
    #logger.debug(f'blk @ {blk}')
    for fid, fblk in enumerate(list(range(2, blk, 2)), start=1):
        #logger.debug(f'{"-"*10}\nprocessing file id {fid} size {inp[fblk]} at {disk[fblk]}')
        p1 += sum(fid * p for p in range(disk[fblk], disk[fblk] + inp[fblk]))
        #logger.debug(f'p1 chksum {p1}')
    logger.info(f'p1 chksum {p1}')
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
