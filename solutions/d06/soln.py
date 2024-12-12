#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
from collections import defaultdict, namedtuple
#from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

Point = namedtuple('Point', ['row', 'col'])

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def main_one(sample: bool, part_two: bool, loglevel: str, guard: str = '^'):
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
    # find starting pos
    p_obs = re.compile(r'#')
    p_g = re.compile(r'\^')
    colmap = defaultdict(list)
    rowmap = defaultdict(list)
    pos = None
    for i, line in enumerate(read_line(fp)):
        m_obs = p_obs.finditer(line)
        for m in m_obs:
            colmap[m.start()].append(i)
            rowmap[i].append(m.start())
        if not pos and (m_g := p_g.search(line)):
            pos = Point(i, m_g.start())
    height, width = i, len(line)
    visited = set([pos])
    # real: row movement; imag: col movement; 0, -1 = -1j -> moving up
    dxy = complex(0, -1)
    # exit con: if guard is at the edge, they will always exit
    while 0 < pos.row < height-1 and 0 < pos.col < width-1:
        # move the guard
        if dxy.real == -1:
            logger.debug('moving left')
            # populate lane with possible obs, and check if any
            lane = [o for o in rowmap[pos.row] if o < pos.col]
            # when pos updates to 0, it will exit from while
            obs = -1 if not lane else max(lane)
            logger.debug(f'obs @ {pos.row, obs}')
            path = [Point(pos.row, col) for col in range(obs+1, pos.col)]
            pos = Point(pos.row, obs + 1)
            # look for max
        elif dxy.real == 1:
            logger.debug('moving right')
            lane = [o for o in rowmap[pos.row] if o > pos.col]
            obs = width+1 if not lane else min(lane)
            logger.debug(f'obs @ {pos.row, obs}')
            path = [Point(pos.row, col) for col in range(pos.col, obs)]
            pos = Point(pos.row, obs - 1)
        elif dxy.imag == -1:
            logger.debug('moving up')
            lane = [o for o in colmap[pos.col] if o < pos.row]
            obs = -1 if not lane else max(lane)
            logger.debug(f'obs @ {obs, pos.col}')
            path = [Point(row, pos.col) for row in range(obs+1, pos.row)]
            pos = Point(obs + 1, pos.col)
        elif dxy.imag == 1:
            logger.debug('moving down')
            lane = [o for o in colmap[pos.col] if o > pos.row]
            obs = height+1 if not lane else min(lane)
            logger.debug(f'obs @ {obs, pos.col}')
            path = [Point(row, pos.col) for row in range(pos.row, obs)]
            pos = Point(obs-1, pos.col)
        
        logger.debug(f'update path: {path}')
        # turn CW 90deg
        dxy /= -1j
        logger.debug(f'new pos {pos} facing {dxy}')
        visited.update(path)
    # output
    ans = len(visited)
    return ans

def main_two(sample: bool, part_two: bool, loglevel: str, guard: str = '^'):
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

    # read input
    # execute
    # find starting pos
    p_obs = re.compile(r'#')
    p_g = re.compile(r'\^')
    obsmap = set()
    pos = None
    for i, line in enumerate(read_line(fp)):
        m_obs = p_obs.finditer(line)
        obsmap.update({complex(m.start(), i) for m in m_obs})
        if not pos and (m_g := p_g.search(line)):
            pos = complex(m_g.start(), i)
            logger.debug(f'pos {pos}')
    height, width = i, len(line)
    logger.debug(f'height {height} width {width}')
    # real: col movement; imag: row movement; 0, -1 = -1j -> moving up
    dxy = complex(0, -1)
    visited = set()
    jmap = defaultdict(list)
    imap = defaultdict(list)
    visited.add(dxy)
    # exit con: if guard is at the edge, they will always exit
    cross = 0
    while 0 < pos.imag < height and 0 < pos.real < width:
        while pos + dxy in obsmap:
            # turn right
            logger.debug(f'obs at {pos + dxy}; turn to {dxy/-1j}')
            dxy /= -1j
            # don't turn and walk; turn or walk
        pos += dxy
        logger.debug(f'move to {pos}')
        # checking for cross is insufficient
        # if pos in visited and dxy / -1j in visited[pos]:
        #     logger.debug(f'cross at {pos}')
        #     cross += 1
        # look to the right of new pos
        chkdir = dxy / -1j
        # look for prev path in this dir
        if dxy in (-1j, 1j):
            # if current dir is vertical, look in jmap (up-down)
            prev_paths = [col for col, d in jmap[pos.imag] if d == chkdir]
            # if going up, -1j, look for nearest where col > pos
            # elif going down, +1j, look for nearest col < pos
            if dxy == -1j:
                near = min((i for i in prev_paths if i > pos.real), default=None)
            else:
                near = max((i for i in prev_paths if i < pos.real), default=None)
            # look for obs between near and pos.real
            if near:
                chkobs = [o for o in obsmap if o.imag == pos.imag and (near < o.real < pos.real or near > o.real > pos.real)]
            else: chkobs = None
        else:
            # look in imap (left-right)
            prev_paths = [row for row, d in imap[pos.real] if d == chkdir]
            if dxy == -1:
                near = max((j for j in prev_paths if j < pos.imag), default=None)
            else:
                near = min((j for j in prev_paths if j > pos.imag), default=None)
            if near:
                chkobs = [o for o in obsmap if o.real == pos.real and (near < o.imag < pos.imag or near > o.imag > pos.imag)]
            else: chkobs = None
        #cross += 0 if chkobs else 1
        if near and not chkobs and pos + dxy not in visited:
           cross += 1
           logger.debug(f'{cross}th obs found @ {pos+dxy}') 
        jmap[pos.imag].append((pos.real, dxy))
        imap[pos.real].append((pos.imag, dxy))
        visited.add(pos)
    logger.info(f'{cross} crosses')
    return len(visited)

def main(sample: bool, part_two: bool, loglevel: str, guard: str = '^'):
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
    pos = None
    for i, line in enumerate(read_line(fp)):
        m_obs = p_obs.finditer(line)
        obsmap.update({complex(m.start(), i) for m in m_obs})
        # find starting pos
        if not pos and (m_g := p_g.search(line)):
            pos = complex(m_g.start(), i)
            logger.debug(f'pos {pos}')
    height, width = i, len(line)
    logger.info(f'height {height} width {width}')
    # real: col movement; imag: row movement; 0, -1 = -1j -> moving up
    dxy = complex(0, -1)
    path = [(pos, dxy)]
    # exit con: if guard is at the edge, they will always exit
    start = pos
    while 0 < pos.imag < height and 0 < pos.real < width:
        while pos + dxy in obsmap:
            # turn right
            logger.debug(f'obs at {pos + dxy}; turn to {dxy/-1j}')
            dxy /= -1j
            # don't turn and walk; turn or walk
        pos += dxy
        logger.debug(f'move to {pos} towards {dxy}')
        path.append((pos, dxy))

    logger.info(f'{len(set(p[0] for p in path))} unique spots')
    if part_two:
        # simulate again, but try placing obstacles along visited path
        # and test for loop while retracing path
        visited = set()
        pos = start
        dxy = complex(0, -1)
        count = 0
        for pos, dxy in path:
            # add path to history as we retrace so that not entire
            # history is used for reference from beginning
            visited.add((pos, dxy))
            # after orienting, simulate placing obstacle in next pos
            # and loop until a. same pos and dir traversed (loop)
            # or step count > size of map * dir
            if (pos + dxy) in obsmap:
                continue
            sim_pos, sim_dxy = pos, dxy
            obsmap.add(pos + dxy)
            steps = 0
            #logger.debug(f'simulating obs @ {pos+dxy}')
            while steps < 4 * height * width and 0 < sim_pos.real < width and 0 < sim_pos.imag < height:
                while (sim_pos + sim_dxy) in obsmap:
                    sim_dxy /= -1j
                    #logger.debug(f'turn to {sim_dxy}')
                sim_pos += sim_dxy
                #logger.debug(f'sim move to {sim_pos}')
                steps += 1
                if (sim_pos, sim_dxy) in visited:
                    count += 1
                    #logger.debug(f'{count} obs found at {pos+dxy}')
                    break
            obsmap.remove(pos+dxy)
    return len(visited), count

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
