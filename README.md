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

### part i

- line = reports, reports = list[level: int]
- are each reports *safe*?
    - iterate through each list
    - check delta for safe requirement
- count number of safe reports

### part ii

- problem dampener
- allows removal of a single level
- as for-loop iterates through report, allow one bad level
- if report[n] was *tolerated*, next delta is between report[n-1] and report[n+1]
- need to check 0th element
- run another pass, but in reverse

## Day 3

### part i

- uncorrupted: `mul(int1,int2)`
- corrupted: any other character
- sum all uncorrupted mults
- simple regex? `r'mul\([0-9]{1,3},[0-9]{1,3}\)`

### part ii

- conditional
    - do() enables future mul ops
    - and don't() disables future mul ops
- mul ops are enabled from the beginning
- recalculate sum
- add `r'do\(\)'` and `r'don't\(\)'` to regex
- find all segments between `do` and `don't`
- include initial segment, `^` to first `don't`
- include last segment of `do()` and `$`
