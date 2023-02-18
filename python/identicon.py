import hashlib
import random
import sys


def is_parity_match(c, v):
    return c == "x" or v & 1 == int(c)


def gen(c):
    v = random.getrandbits(4)
    while not is_parity_match(c, v):
        v = random.getrandbits(4)

    return v


def gen_int(pair):
    a, b = pair

    n = gen(a)
    n <<= 4
    n ^= gen(b)

    return n


def gen_matching_bytes():
    if len(sys.argv) != 2:
        sys.exit(1)

    s = sys.argv[1]  # parsed pattern string (not a grid!)

    ints = map(gen_int, s.split(" "))

    for i, n in enumerate(ints):
        print(f"bytes[{i}] = {n};")


def nibble(digest):
    # nibble the first 8 chunks in 4 bit increments, see nibbler.rs
    for byte in digest[:8]:
        hi, lo = byte & 0xF0, byte & 0x0F
        yield hi >> 4
        yield lo


def md5_test(n, pattern):
    b = bytes(str(n), "utf8")
    h = hashlib.md5(b)
    if n == 12789:
        print(n, list(nibble(h.digest())), pattern)
    return all(is_parity_match(c, v) for v, c in zip(nibble(h.digest()), pattern))


def parse_grid(grid):
    """
    converts a grid like

    K F A
    L G B
    M H C
    N I D
    O J E

    to

    ABCDEFGHIJKLMNO
    """

    rows = [row.strip().split(" ") for row in grid]
    return "".join(rows[row][col] for col in range(2, -1, -1) for row in range(0, 5))


def do_all_tests(pattern):
    for i in range(100_000_000):
        if md5_test(i, pattern):
            print(i)


def main():
    grid1 = """
00000
01110
01110
00000
00100"""

    grid2 = """
01010
11111
01110
00100
11111"""

    grid3 = """
11111
10101
11111
10101
01010"""

    grid4 = """
01010
00100
01010
10101
01110"""

    grid5 = """
10001
00100
00000
00100
11111"""

    grid6 = """
10101
10001
01110
10101
10101"""

    grid7 = """
00000
00100
10001
01010
00000"""

    grid8 = """
10001
01110
10001
00000
11011"""

    grid9 = """
00100
01110
00000
10001
10001"""

    grid10 = """
11011
11111
00000
11011
11111"""

    grids = [grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9, grid10]

    grids_ = [grid.strip().split("\n") for grid in grids]

    # grid = sys.stdin.readlines()  # uncomment this to echo your own grid
    for grid in grids_:
        pattern = parse_grid(grid)

        do_all_tests(pattern)


if __name__ == "__main__":
    main()
