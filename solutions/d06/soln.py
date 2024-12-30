#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def patrol(obsmap, height, width, start, dxy=-1j) -> bool:
    """
    Returns True if loop has been detected
    """
    path = set()
    pos = start
    # exit con: if guard is at the edge, they will always exit
    while 0 < pos.imag < height and 0 < pos.real < width:
        while pos + dxy in obsmap:
            # turn right
            # logger.debug(f'obs at {pos + dxy}; turn to {dxy/-1j}')
            dxy /= -1j
            # don't turn and walk; turn or walk
        # now oriented correctly
        if (pos, dxy) in path:
            logger.debug('loop found')
            return True
        path.add((pos, dxy))
        # move forward
        pos += dxy
        # logger.debug(f'move to {pos} towards {dxy}')
    return False

def main(sample: bool, part_two: bool, loglevel: str):
    """ 
    complex as coords
    col as real (left and right), and row as imag;
    as grid goes down, row incr, and imag comp increases
    """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    p_obs = re.compile(r'#')
    p_g = re.compile(r'\^')
    obsmap = set()
    start = None
    for i, line in enumerate(read_line(fp)):
        m_obs = p_obs.finditer(line)
        obsmap.update({complex(m.start(), i) for m in m_obs})
        # find starting start
        if not start and (m_g := p_g.search(line)):
            start = complex(m_g.start(), i)
            logger.debug(f'start {start}')
    height, width = i, len(line)
    logger.info(f'height {height} width {width}')
    dxy = -1j # moving up
    pos = start
    path = [(pos, dxy)]
    # exit con: if guard is at the edge, they will always exit
    while 0 < pos.imag < height and 0 < pos.real < width:
        while pos + dxy in obsmap:
            # turn right
            # logger.debug(f'obs at {pos + dxy}; turn to {dxy/-1j}')
            dxy /= -1j
            # don't turn and walk; turn or walk
        pos += dxy
        # logger.debug(f'move to {pos} towards {dxy}')
        path.append((pos, dxy))

    pos_uniqs = set(p[0] for p in path)
    logger.info(f'{len(pos_uniqs)} unique spots')
    ans = 0
    if part_two:
        # simulate again, but try placing obstacles along visited path
        # and test for loop while retracing path
        for pos in pos_uniqs:
            obsmap.add(pos)
            # logger.debug(f'placing obs at {pos}')
            ans += patrol(obsmap, height, width, start)
            obsmap.remove(pos)
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
