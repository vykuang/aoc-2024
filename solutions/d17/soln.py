#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

class Computer:
    def __init__(self, regs={}, prog=[]):
        self.regA = regs['A']
        self.regB = regs['B']
        self.regC = regs['C']
        self.prog = prog

    def combo(self, oprnd):
        if 0 <= oprnd < 4:
            return oprnd
        elif oprnd == 4:
            return self.regA
        elif oprnd == 5:
            return self.regB
        elif oprnd == 6:
            return self.regC
        else:
            raise ValueError('operand not valid')
    def exe(self):
        """
        executes the instructions on the regs
        """
        self.ptr = 0
        self.output = []
        while self.ptr < len(self.prog)-1:
            opcode = self.prog[self.ptr]
            oprnd = self.prog[self.ptr+1]
            combo = self.combo(oprnd)
            # logger.debug(f'opcode {opcode} oprnd {oprnd}')
            match opcode:
                case 0:
                    self.regA = int(self.regA / pow(2, combo))
                case 6:
                    self.regB = int(self.regA / pow(2, combo))
                case 7:
                    self.regC = int(self.regA / pow(2, combo))
                case 1: # XOR
                    self.regB = self.regB ^ oprnd
                case 2:
                    self.regB = combo % 8
                case 3:
                    # how to implement jnz?
                    # instance need prog context
                    if self.regA != 0:
                        # end of prog: 3,0 - prog repeats until regA = 0
                        # - 2 to offset the default +2
                        self.ptr = oprnd - 2
                case 4:
                    self.regB = self.regB ^ self.regC
                case 5:
                    self.output.append(combo % 8)
            self.ptr += 2
            # logger.debug(f'current out: {self.output}')
        return self.output


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
    inp = read_line(fp)
    regs = {}
    for line in inp:
        if not line.strip():
            break
        parts = line.strip().split(':')
        reg = parts[0].split()[1]
        val = int(parts[1].strip())
        regs[reg] = val

    prog = [int(n) for n in next(inp).split(':')[1].split(',')]
    # execute
    logger.info(f'regs:{regs}\nprog: {prog}')
    cpu = Computer(regs, prog)
    p1 = cpu.exe()
    ans1 = ','.join(str(n) for n in p1)

    #regs['A'] += 1
    A_init = 0
    for i in range(len(prog)-1):
        A_init += prog[i] * pow(8, i+1)

    A_init = 1
    regs['A'] = A_init
    p2 = Computer(regs, prog).exe()
    logger.debug(f'regA = {regs["A"], oct(regs["A"])}\noutput {p2}')
    # search for upper bound
    # while p2 != prog:
    ones = []
    for i in range(int('200', base=8), int('300', base=8)):
    #     regs['A'] *= 2
    #     p2 = Computer(regs, prog).exe()
    #     logger.debug(f'regA = {oct(regs["A"])}\noutput {p2}')
        # regs['A'] += 1
        regs['A'] = i
        p2 = Computer(regs, prog).exe()
        ones.append(p2[0])
        if i % 8 == 7:
            logger.debug(f'a = {oct(i)}\t tens {p2[1]}\tones {ones}')
            ones = []
        # logger.debug(f'regA = {oct(regs["A"])}\noutput {p2}')
        # regs['A'] -= 1
        # input()
    ans2 = regs['A']
    logger.info(f'regA {regs["A"]}\np2: {",".join(str(n) for n in p2)}')
    # output
    return ans1, ans2

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
