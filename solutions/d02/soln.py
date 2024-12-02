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
def parse_levels(report: str) -> list[int]:
    report = list(map(int, report.split()))
    return report

def check_report(report: list[int], tol: int = 1) -> bool:
    """
    check if each report meets criteria
    First algorithm did not check if removing the 0th element
    makes it safe
    Handle by checking the reverse
    """
    delta = report[1]-report[0]
    sign = delta
    prev = report[1]
    if not 1 <= abs(delta) <= 3:
        tol -= 1
        if tol < 0:
            return False
        else:
            prev = report[0]
    for i in range(2, len(report)):
        delta = report[i]-prev
        if not (1 <= abs(delta) <= 3 and delta * sign > 0):
            # check mag
            tol -= 1
            if tol < 0:
                return False
            else:
                # don't update prev
                continue
        prev = report[i]
    return True

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

    # execute

    # output
    tol = 1 if part_two else 0
    ans = sum(
        check_report(
            parse_levels(line), tol=tol) or check_report(
                parse_levels(line)[::-1], tol=tol)
    for line in read_line(fp))
    # unsafe = [r for r in read_line(fp) if not check_report(r, tol=0)]
    # logger.setLevel("DEBUG")
    # logger.addHandler(logging.FileHandler("debug.log"))

    # dampen = [r for r in unsafe if check_report(r, tol=1)]    
    # return len(dampen)
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
