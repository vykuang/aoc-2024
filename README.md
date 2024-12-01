# AoC 2024

Third AoC! Good luck and don't stay past midnight, I say to my future self.

Tiny challenge: stick to python's built-in libraries, which includes `collections` and `itertools`

## Day 1

### part i

- unique loc ID
- two lists
- pair the two lists in-order to find difference
- sum the diffs

sort the two lists and sum the diffs via a for-loop

### part ii

similarity score: for each in left, multiply by freq in right list, and sum.

Misread #1: the count is incremented for each occurrence in the left list as well. Thus, create `Counter` for both list, and return `sum(n * countleft[n] * countright[n] for n in countleft)`

## Day 2

