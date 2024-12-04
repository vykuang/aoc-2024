#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from functools import reduce

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def memmul(csum: int, grps: re.match) -> int:
    return csum + int(grps.group(1)) * int(grps.group(2))

def main(sample: bool, part_two: bool, loglevel: str):
    """
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    mems = "".join(line for line in read_line(fp))
    # execute
    ans = 0
    if not part_two:
        p = re.compile(r"mul\((\d+),(\d+)\)")
        ans = reduce(memmul, p.finditer(mem), 0)
    else:
        pa = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")
        enable = True
        for a, b, do, dn in pa.findall(mems):
            # findall returns all hits sequentially
            if a and b:
                ans += int(a) * int(b) * enable
            elif do or dn:
                # if only don't() found, bool(do) = False
                # since do will be None
                enable = bool(do)
    return ans

        # attempt to split the string was not successful
        # answer too high
    #     p_do = re.compile(r"do\(\)")
    #     p_donot = re.compile(r"don't\(\)")
    #     # find all indices of the two
    #     idx_do = deque([m.end() for m in p_do.finditer(mems)])
    #     idx_dn = deque([m.start() for m in p_donot.finditer(mems)])
    #     logger.info(f'{idx_do} do() and {idx_dn} dont()')
    #     # handle beginning as edge case
    #     span = idx_dn.popleft()
    #     ans = reduce(memmul, p.finditer(mems[:span]), ans)
    #     logger.debug(f'first span {span} holds {ans}')
    #     while idx_do:
    #         # find do() after span
    #         do = idx_do.popleft()
    #         while idx_do and do < span:
    #             logger.debug('discard do')
    #             do = idx_do.popleft()
    #         logger.debug(f'next start {do}')
    #         dn = idx_dn.popleft()
    #         while idx_dn and dn < do:
    #             logger.debug('discard dont')
    #             dn = idx_dn.popleft()
    #         logger.debug(f'next span {dn}')
    #         # process new span of do()
    #         span = dn
    #         ans = reduce(memmul, p.finditer(mems[do:span]), ans)
    #         logger.debug(f'ans updated to {ans}')
    #     if idx_do:
    #         ans = reduce(memmul, p.finditer(mems[idx_do.pop():]), ans)
    #     else:
    #         logger.debug(f'mul disabled from {span}')    
    # # output
    # return ans

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
