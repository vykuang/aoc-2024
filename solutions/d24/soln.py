#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time
import re
import operator
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

class Gate:
    def __init__(self, a, b, opname, q):
        self.a = a
        self.b = b
        self.opname = opname
        if 'X' not in opname:
            self.opname += '_'
        self.op = eval(f'operator.{self.opname.lower()}')
        self.q = q
    def exe(self):
        pass
    def __repr__(self):
        return f'{self.a} {self.opname} {self.b} -> {self.q}'

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
    p_init = re.compile(r'([x,y]\d+): ([0,1])')
    p_gates = re.compile(r'([a-z|0-9]{3,}) ([ANDXOR]{2,3}) ([a-z|0-9]{3,}).*([a-z|0-9]{3,})')
    file = read_line(fp)
    wires = {}
    for line in file:
        if not (line := line.strip()):
            break
        # initial states
        m = p_init.search(line)
        wires[m.group(1)] = int(m.group(2))
    gates = []
    for line in file:
        m = p_gates.search(line.strip())
        gates.append(Gate(a=m.group(1), b=m.group(3), opname=m.group(2), q=m.group(4)))
    # execute
    todo = deque(gates)
    p1 = 0
    while todo:
        gate = todo.popleft()
        if gate.a in wires and gate.b in wires:
            # both inputs present
            wires[gate.q] = gate.op(wires[gate.a], wires[gate.b])
            if 'z' == gate.q[0] and wires[gate.q]:
                p1 += pow(2, int(gate.q[1:]))
                #logger.debug(f'{gate.q} {wires[gate.q]}\tans = {ans}')
        else:
            todo.append(gate)
    # output
    # part ii - find the swapped gates
    # sum x and y
    z_exp = 0
    for wire in wires:
        if wire[0] in 'xy' and wires[wire]:
            z_exp += pow(2, int(wire[1:]))
    logger.info(f'x + y = {z_exp}')
    return p1

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
