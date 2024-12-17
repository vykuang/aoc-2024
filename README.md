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
- take `start` and `span` from match
- include initial segment, `^` to first `don't`
- include last segment of `do()` and `$`
- splitting segments this way returned too high of an answer
- `findall()` with a pattern that finds both mul, do, and don't returns all hit sequentially
- allows iteration to flip enable/disable while summing the muls
- split approach:
    - split by don't()
    - process all of first segment
    - for all remaining, find first instance of do() with re.search()
    - process from that point on to end of segment

## Day 4 word search

### part i

- grid of {X, M, A, S}
- count horizontal, vertical, diag, forward, reverse
- can overlap
- look for all X as starts, iterating through rows and cols
- search 8 dir
- if M found, continue in same dir for A, S

### part ii

- look for X shaped MAS
- starts with A
- look at 4 diagonals for M, M, S, S
- always look from top left, clockwise
- rotate the mini 3x3 section clockwise before checking again
- return True if MAS found
- try next rotation if not
- catch: make sure the corners are actually clockwise

## Day 5 print queue

### part i

- input has 2 sections
    - order rules
    - order of updates
- determine which updates are correctly ordered according to rules
- from correct order, sum the middle page numbers
- a lot of lookups coming from update section
- for 75, lookup rules containing 75
    - for each rule, `re.match()` to see whether index follows the rules
- to build rules:
    - for each rule, `a|b`, add 2 entries rules[a]['post'] and rules[b]['pre'] 
    - `b` must be after `a`, so rules[a]['post'].append(b)
    - conversely, rules[b]['pre'].append(a)

### part ii

- fix the incorrectly ordered updates
- sum the newly corrected updates middle page numbers
- filter out incorrects from part i
- iterate through each line
    - at each page, check for u[j] in rules[page]['pre'], if j > i, or ['post'] if j < 1
    - if exists, swap j and i
    - nested for-loop at each line

## Day 6

### part i

- grid
    - `.` - space
    - `#` - wall
    - `^` - guard and direction
- guard always moves straight
- when obs, turn CW 90deg
- able to exit
- count distinct pos visited before guard exist map
- set() to collect distinct pos
- array manipulation to look ahead to find next obs
- our grid needs to be able to answer "is there any obstacle in this column or row, and if so where is it"
- have two dicts? one for row, another for col
- rowmap[row_n] = list[cols that contain obs]
- colmap[col_n] = list[rows that contain obs], conversely
- build as input is read
- add in-between pos to set
- init set with starting pos

### part ii

- count coords where a new obs would cause a loop
- always at locs where path crosses previously visited
- can we simply count these crosses? that would overcount
- keep track of directions: if crossing a prev path that was heading 90deg CW, increment count
- crosses is not a sufficient condition, see ex 4-6 in sample input
- for each new pos, check if there exists some prev path going to the right of current dir, and if there are any obs between pos and start of that nearest path segment
- record each segment when turning, or at the beginning
- turning also marks the end of prev segment
## Day 7 bridge repair

### part i

- each line is an equation
- test value: list[ints]
- use list of ints, and `+`, `*` to produce test val
- always eval'd left to right
- not all are possible
- sum valid test values
- use BFS? model as binary tree - each node has two children: `+` or `*` the next value of the array
- if over, prune

### part ii

- add concatenation as an additional operator
- implement as another possible child node

## day 8

### part i

- antennas denoted by all non-dot symbols
- different char = different freq
- two antennae of same freq creates two resonant antinodes
- "where one antenna is twice is far away as the other"
- locs with antenna can be an antinode
- count unique antinodes within map
- collect antenna locs
- group by freq
- create product of locs
- prune those outside bounds
- make set and count; 329

### part ii

- resonant harmonics???
- antinodes occur regardless of distance, not just when one antenna is twice as far as the other
- for each pair combination, compare with map boundary
- given a pair of antennae at (ar, ac), and (br, bc), and map boundary nr, nc:
    - calc l-dist = (br - ar, bc - ac) = (dr, dc)
    - how to determine the correct bound to check?
    - since all antinode locs need to be hashed, use while loop and check for bounds every step

## day 9 disk fragmenter

### part i

- input: `blocks-of-file blocks-of-space ...`
- each file is 0-indexed
- disk map `12345` = `0..111....22222` where digits rep file ID and . is free space
- compact by bringing data from end of each line to left-most available empty block
- start: `0..111....22222`
- end:  `022111222......`
- notice how files from ID=2 filled up space between file 0 and file 1
- ans is checksum
    - mul each block `pos` (0-indexed) with file ID contained
    - return sum
- expand the input from dense form? end up with a very long list...
- two-pointers
    - left to fill up the space
    - right to move from the end
    - if len(nums) is odd, last = file
    - else take last-1
    - file ID = len(nums) // 2
    - take last file
    - incr left and expand until enough space
    - then take from end again and repeat
    - keep expanded in mem? or mult and sum as it goes?

### part ii

- keep files together
- if file to be moved is too large, don't
- attempt each file transfer only once before moving to the next file ID
- for each file, look through all empty blocks starting from left
- empty blocks are continuously changing through the transfer process
- change the input in-place
- start the `blk` pos at first non-zero storage block for each attempted file transfer
- check `blk` vs `n_last := n_file_blks`
- while `blk < n_last`
    - not enough space
    - incr blk to next empty block
    - until `pos_chk >= right`, then break and decr `last_id`
- if `blk >= n_last`
    - move `last_id` to blk
- reset `pos_blk` to initial blk
- process stops when `left_id == last_id`
- after moving, need to check if there is remaining space
    - if yes, try to fit remaining space with last blocks as well
    - if not, `blk` pointer

## day 10 traversal

### part i 

- input: grid of heights
- good trail:
    - longest
    - uphill only; do not go down or same height
    - cardinal dir only
- trailhead is any pos with height = 0
- score: num of 9-height pos reachable from a trailhead via a *good* trail
- sum the score of all trailheads
- save grid as `{complex: height}`
- collect trailheads
- traversal: child nodes are valid only if h_child - h_parent = 1
- need to check for repeats on the same path
- add to path whether it's a peak or not

### part ii

- rating: num of distinct trails that begin at the trailhead
- trail always ends at 9
- but if a different path is taken to reach the same peak, it's a different trail
- sum the ratings
- I accidentally ran the logic for part ii when doing part i
- don't keep track of paths; incr as soon as 9 is found

## day 11 blinking stones

### part i

1. if 0, replace with 1
1. if *even number of digits*, replaced with 2 stones; left half of num to left, right half to right; 1000 -> 10 and 0
1. multiply by 2024

input is line of number-engraved stones; count num stones after 25 blinks

- array manipulation
- iterate through the array and apply each rule
- random insertion

## day 12 garden fences

### part i

- rectangular 2D plot
- types of plants
- same types form a region
- same types can from different regions if not contiguous
- find perimeter
- sum perimeter * area of each region

Implementation:

- queue with top left
- if already counted, next
- else start new region and flood search in 4 cardinal dir
    - if counted next 
    - if new type, append to queue
    - if same type, append to region
- given collection of regions... flood search again to find all edges?
    - start from any point in region
    - search 4 cardinal dir
    - if not in region or outside bounds, increment edge count
    - if in region, append to search queue
    - combine with region search into one

### part ii - bulk discount

- we're talking *sides* now, not perimeter
- `AAAA` has 4 sides, vs p = 8
- does flood search still work?
- second pass? start with a point at the edge of a region
- follow the edges, go clockwise, try all directions starting with left
- increment sides only after turning
- stop when returning to original pos
