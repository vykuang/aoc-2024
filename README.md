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

## Day 6 - guard patrol

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

simulation approach:

- retrace pat
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

implement:

- if block cannot be moved, it will never be attempted again
    - calc checksum on the spot
- block id: index of input
    - used to check whether space can fit file
- pos: pos on actual disk (after expanding the input)
    - used for chksum
- keep disk[blk] as prefix sum to reference pos of each blkid
    - update when used
- almost 2s; need to apply dict, Counter, and deque

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

### part ii

- 75 cycles; cycle detection?
- no cycles with them together; how about by themselves? no, and the numbers never decrease in magnitude, implying higher powers than polynomial
- no cycles themselves, but stones will often repeat themselves
- cache the result (length of blink results) of each stone, blink key
- at blinks == 0: return 1, NOT `stone` VALUE since length == 1

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
- doesn't seem to work on paper; need to figure something else

#### corner counting

for any polygon, n(sides) = n(corners); for each cell, count the corners

#### map the edges and sort

- horiz sides: `{row: [cols]}` - top left of `grid[row][col]` going towards right
- vert sides: `{col: [rows]}` - top left of `grid[row][col]` going towards down
- sort each lists for each key
- both row and col ranges from 0 to height/width to account for the rightmost col/bottom row

```
+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+
```

A: 

- horiz: `{0: [0,1,2,3]}, {1: [0,1,2,3]}`
- vert: `{0: [0]}, {4: [0]}`
- both horiz are continuous - one side each
- both vert are singular - one side each
- 4 sides

C:

- horiz
    - 1: [2]
    - 2: [3]
    - 3: [2]
    - 4: [3]
- vert
    - 2: [1,2]
    - 3: [1,3]
    - 4: [2,3]
- each horiz += 1
- verts @ cols 2, 4 are 1 each
- verts @ col 3 have 2 segments = 2 sides
- total = 8

Foiled by the B enclosed by A example

```
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
```

In the centre, there are two horiz. fences, but current method only counts 1, since technically they are sequential along the same row

- need direction of plant -> fence
- first 2: [2, -1j]: [1, 2]
- other 2: [2, 1j]: [3, 4]

## day 13 claw contraption

### part i

- 3 tokens for A button; 1 for B
- 1 prize
- each button moves a little forward and a little to the right
- A and B moves different distances
- min moves to position claw above prize target?
- some prizes cannot be won; these require 0 tokens
- button presses < 100
- 2 degrees of freedom
- prioritize B if possible
- dynamic programming?
- top down recursion?
- 3s in WSL2 for part i

### part ii

- Add 10000000000000 to the target; much larger
- no more button limits
- recursion limits
- bottom up tabular approach?
- start with only pressing B
- decrement B until nA + mB = target
- too large to iterate the target with such relatively small steps
- any implementation needs ~~some clever modulo math~~ linear algebra

$$Ax = B$$
$$A^{-1} A x = B$$
$$Ix = A^{-1} B$$
$$x = A^{-1} B$$

- A = coefficient matrix (movement per button press, each ~~row~~ column = each button)
- x = variable (num presses required for each button)
- B = constants (target coord)

Filter out non-integer results

## day 14 restroom redoubt

### part i

- list of robots pos, and velocity, both in (x,y)
- (0,0) = top left
- robots can occupy the same tile
- robots wrap around the edge
- 100 seconds
- count robots in each quadrant
- robots on the quadrant lines do not count
- return product
- for each robot, move by their velocity
- check for bounds
- if pos_x + dx > width, pos_x = pos_x + dx % width
- or can we always use mod? if x + dx < width, then x + dx % width = x + dx

### part ii

something that looks like a christmas tree...

filter for cycles where no robots are overlapping? no cycles with no overlap...

how about when all points not on the meridian have a reflection?

from text, only *most* should arrange themselves; perhaps only check for half? 

Ultimately we're checking for some sort of alignment around the meridian; check for average of all pos.x and if it's anywhere near meridian, take a look

no dice. need to render the robot map

## day 15 warehouse woes

### part i

- input: map then list of directions the robot want to take
- in map, robot starts at `@`
- `O` are boxes
- `#` are walls
- robots can push boxes but not if boxes are against walls, at which point robot remains in place
- box coord = 100 * dist from top + dist from left (incl. edges)
- return sum of box coords after robot finishes movement sequence

Implement:

- sparse array
- collect boxes and robot pos as `dict[complex]`
- but all coords need to be updated, sometimes multiple at a time
- sparse matrix of bool?
- `class Box`?
    - self.pos
    - self.neighbors?
- for a 50 x 50 map, maybe not necessary for sparse rep?
- keep entire grid, even empty
- record char for each pos, not simply bool for box, since walls can appear within warehouse bounds

### part ii

- boxes *and walls* are now twice as wide
    - walls are '##'
    - boxes are now '[]'
- robot is still same size
- height is the same
- dist is measured between closest edge and closest side of box

## day 16 reindeer maze

### part i

- S needs to reach E in a maze of '#' and '.'
- move forward = 1 pt; turn 90deg = 1000 pt; minimize pt
- sounds like time for dijkstra?
- multiple paths can share the same minimum score

### part ii

- find *all* the best paths
- count the tiles along those paths
- KEEP VISITED - RUNNING MINIMUM SCORE AT EACH POS, DXY instead of only comparing it vs BEST- MUCH EARLIER PRUNING

## day 17 chronospatial computer

### part i

reading is difficult.

- 3 registers: A, B, C can hold any integer
- 8 instructions:
    - 0: div reg A = A / pow(2, combo)
    - 1: bxl reg B = XOR of reg B and $l
    - 2: bst B = $c % 8
    - 3: jnz 
        - no op if A = 0, 
        - else jumps to $l, and 
        - inst ptr is not inc'd by 2 after this (so that it can execute the inst it jumped to)
    - 4: bxc B = B XOR C, and exhausts one operand
    - 5: out out = $c % 8; multiple outs are comma-delim
    - 6: bdv B = A / pow(2, combo)
    - 7: cdv C = A / pow(2, combo)
- inst pointer: pos of program where next opcode is read
    - starts at 0, the first 3-bit num in prog
    - incr += 2 after each instruction, since the index immediately following an inst is the operand
    - except for `jmp`
    - halts if reading past the end
    - 0,1,2,3 would start at 0, pass 1 as operand, then exe 2, with 3 as operand, then halt
- inst also specifies type of operand
    - literal: val itself
    - combo
        - 0-3: literals
        - 4-6: A-C
        - 7: reserved
- determine comma-delim'd output 
- put everything into a class
    - regA-C
    - prog
    - program pointer
    - output
- exe until ptr > prog

### part ii

program is supposed to output *another copy of the program*

- find correct val to initialize `regA` so that output is same as program
- return lowest positive A init
- seems to require some mathing

## day 18 RAM run

### part i

- 2d grid, 0-70
- input: list of coords indicating where bytes will fall, in `x, y` format
- start at `0, 0` (top left)
- exit at bottom right (6, 6) in ex, (70, 70) in input
- once bytes land, that spot is corrupted and cannot be used
- pathfinding with a dynamic maze
- dijkstra while updating barriers every cycle
- only worked after *all the required bytes fell first*, instead of updating the falling bytes step by step; misread?

### part ii

determine the first byte that will prevent any paths from reaching the end

## day 19 linen layout

### part i

- pattern of colors
- w, u, b, r, g
- input:
    - list of available patterns (with replacement)
    - list of desired patterns
- some desired patterns are not possible
- count how many are
- dynamic prog?
    - top-down recursion with memo?
    - branch for each possible option
- BE CAREFUL OF EMPTY LAST LINES

### part ii

- get alllllll the possible combinations
- instead of returning bool, return 1 for each valid hit
- sum the possibilities instead
- still use pattern as the key, since linens are taken with replacement
- use diff cache than validation
- manual cache seems to be faster than `@cache` by 10-15%?

## day 20 race condition

- no pathfinding necessary, there is only a single path from start to end

### part i

- keep history of path and turn at each point
- look for other points in the path where manhattan distance <= cheat and picosec is further along

### part ii

extend part i by changing the cheat timer

## day 21
