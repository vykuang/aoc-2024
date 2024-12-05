#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
from collections import defaultdict
import re
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

    # read input
    rules = defaultdict(lambda: defaultdict(set))
    p_rule = re.compile(r'(\d+)\|(\d+)')
    lines = read_line(fp)
    for line in lines:
        if line.strip() == '':
            # move onto update section
            break
        m = p_rule.match(line)
        a, b = int(m.group(1)), int(m.group(2))
        rules[a]['post'].add(b)
        rules[b]['pre'].add(a)
    logger.debug(f'rules:\n{rules}')
    # read updates
    def is_valid(u: list[int]) -> bool:
        """Assumes rules[pg] to exist"""
        for i, pg in enumerate(u):
            # check all both pre and post rules
            for chk in rules[pg]['pre']:
                if chk not in u:
                    continue
                if u.index(chk) > i:
                    return False
            for chk in rules[pg]['post']:
                if chk not in u:
                    continue
                if u.index(chk) < i:
                    return False
        return True

    # execute
    ans = 0
    for line in lines:
        u = eval('[' + line + ']')
        ans += u[len(u) // 2] if is_valid(u) else 0

            
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
    logger.info(f"runtime: {(tstop-tstart):.3f} ms")
    print('ans ', ans)
