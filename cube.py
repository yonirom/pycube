from functools import partial
import random

"""""
    The names of the facelet positions of the cube
                  |************|
                  |* 0** 1** 2*|
                  |************|
                UW|* 3** X** 4*|
                  |************|
                  |* 5** 6** 7*|
                  |************|     RR          BB
     |************|************|************|************|
     |*24**25**26*|* 8** 9**10*|*32**33**34*|*40**41**42*|
   LO|************|************|************|************|
     |*27** X**28*|*11** X**12*|*35** X**36*|*43** X**44*|
     |************|************|************|************|
     |*29**30**31*|*13**14**15*|*37**38**39*|*45**46**47*|
     |************|************|************|************|
                  |************|\
                  |*16**17**18*| \
                  |************|  FG
                DY|*19** X**20*|
                  |************|
                  |*21**22**23*|
                  |************|
UW - UP/WHITE
FG - FRONT/GREEN
DY - DOWN/YELLOW
LO - LEFT/ORANGE
RR - RIGHT/RED
BB - BACK/BLUE

import colored
colored.fore.RED '\x1b[38;5;1m'
colored.fore.GREEN '\x1b[38;5;2m'
colored.fore.BLUE '\x1b[38;5;4m'
colored.fore.WHITE '\x1b[38;5;15m'
colored.fore.ORANGE_1 '\x1b[38;5;214m'
colored.fore.YELLOW_1 '\x1b[38;5;226m'
colored.style.RESET '\x1b[0m'

"""
S = list(range(48))   # Initial cube

COLORS = ['\x1b[38;5;15m'] * 8 + ['\x1b[38;5;2m'] * 8 + ['\x1b[38;5;226m'] * 8 + ['\x1b[38;5;214m'] * 8 + ['\x1b[38;5;1m'] * 8 + ['\x1b[38;5;4m'] * 8

TRANSFORMS = {
        'U': [5, 3, 0, 6, 1, 7, 4, 2, 32, 33, 34, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9, 10, 27, 28, 29, 30, 31, 40, 41, 42, 35, 36, 37, 38, 39, 24, 25, 26, 43, 44, 45, 46, 47],
        'R': [0, 1, 10, 3, 12, 5, 6, 15, 8, 9, 18, 11, 20, 13, 14, 23, 16, 17, 45, 19, 43, 21, 22, 40, 24, 25, 26, 27, 28, 29, 30, 31, 37, 35, 32, 38, 33, 39, 36, 34, 7, 41, 42, 4, 44, 2, 46, 47],
        'L': [47, 1, 2, 44, 4, 42, 6, 7, 0, 9, 10, 3, 12, 5, 14, 15, 8, 17, 18, 11, 20, 13, 22, 23, 29, 27, 24, 30, 25, 31, 28, 26, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 21, 43, 19, 45, 46, 16],
        'D': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 29, 30, 31, 21, 19, 16, 22, 17, 23, 20, 18, 24, 25, 26, 27, 28, 45, 46, 47, 32, 33, 34, 35, 36, 13, 14, 15, 40, 41, 42, 43, 44, 37, 38, 39],
        'F': [0, 1, 2, 3, 4, 31, 28, 26, 13, 11, 8, 14, 9, 15, 12, 10, 37, 35, 32, 19, 20, 21, 22, 23, 24, 25, 16, 27, 17, 29, 30, 18, 5, 33, 34, 6, 36, 7, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47],
        'B': [34, 36, 39, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 27, 29, 2, 25, 26, 1, 28, 0, 30, 31, 32, 33, 23, 35, 22, 37, 38, 21, 45, 43, 40, 46, 41, 47, 44, 42]
}

# U_ = [2, 4, 7, 1, 6, 0, 3, 5, 24, 25, 26, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 40, 41, 42, 27, 28, 29, 30, 31, 8, 9, 10, 35, 36, 37, 38, 39, 32, 33, 34, 43, 44, 45, 46, 47]
# R_ = [0, 1, 45, 3, 43, 5, 6, 40, 8, 9, 2, 11, 4, 13, 14, 7, 16, 17, 10, 19, 12, 21, 22, 15, 24, 25, 26, 27, 28, 29, 30, 31, 34, 36, 39, 33, 38, 32, 35, 37, 23, 41, 42, 20, 44, 18, 46, 47]
# L_ = [8, 1, 2, 11, 4, 13, 6, 7, 16, 9, 10, 19, 12, 21, 14, 15, 47, 17, 18, 44, 20, 42, 22, 23, 26, 28, 31, 25, 30, 24, 27, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 5, 43, 3, 45, 46, 0]
# D  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 37, 38, 39, 18, 20, 23, 17, 22, 16, 19, 21, 24, 25, 26, 27, 28, 13, 14, 15, 32, 33, 34, 35, 36, 45, 46, 47, 40, 41, 42, 43, 44, 29, 30, 31]
# F_ = [0, 1, 2, 3, 4, 32, 35, 37, 10, 12, 15, 9, 14, 8, 11, 13, 26, 28, 31, 19, 20, 21, 22, 23, 24, 25, 7, 27, 6, 29, 30, 5, 18, 33, 34, 17, 36, 16, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
# B_ = [29, 27, 24, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 39, 36, 34, 21, 25, 26, 22, 28, 23, 30, 31, 32, 33, 0, 35, 1, 37, 38, 2, 42, 44, 47, 41, 46, 40, 43, 45]


def A(cube, transform):
    return [cube[i] for i in transform]


U = partial(A, transform=TRANSFORMS['U'])
R = partial(A, transform=TRANSFORMS['R'])
L = partial(A, transform=TRANSFORMS['L'])
D = partial(A, transform=TRANSFORMS['D'])
F = partial(A, transform=TRANSFORMS['F'])
B = partial(A, transform=TRANSFORMS['B'])

U2 = partial(A, transform=U(U(S)))
Ut = partial(A, transform=U(U(U(S))))
R2 = partial(A, transform=R(R(S)))
Rt = partial(A, transform=R(R(R(S))))
L2 = partial(A, transform=L(L(S)))
Lt = partial(A, transform=L(L(L(S))))
D2 = partial(A, transform=D(D(S)))
Dt = partial(A, transform=D(D(D(S))))
F2 = partial(A, transform=F(F(S)))
Ft = partial(A, transform=F(F(F(S))))
B2 = partial(A, transform=B(B(S)))
Bt = partial(A, transform=B(B(B(S))))


def print_cube(c):
    def f(i):
        return COLORS[i] + "\u2588\u2588"

    print("      {}{}{}".format(f(c[0]), f(c[1]), f(c[2])))
    print("      {}{}{}".format(f(c[3]), f(0),    f(c[4])))
    print("      {}{}{}".format(f(c[5]), f(c[6]), f(c[7])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[24]), f(c[25]), f(c[26]), f(c[8]), f(c[9]), f(c[10]), f(c[32]), f(c[33]), f(c[34]), f(c[40]), f(c[41]), f(c[42])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[27]), f(24),    f(c[28]), f(c[11]), f(8), f(c[12]), f(c[35]), f(32), f(c[36]), f(c[43]), f(40), f(c[44])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[29]), f(c[30]), f(c[31]), f(c[13]), f(c[14]), f(c[15]), f(c[37]), f(c[38]), f(c[39]), f(c[45]), f(c[46]), f(c[47])))
    print("      {}{}{}".format(f(c[16]), f(c[17]), f(c[18])))
    print("      {}{}{}".format(f(c[19]), f(16),    f(c[20])))
    print("      {}{}{}".format(f(c[21]), f(c[22]), f(c[23])))
    print('\x1b[0m')


def gen_scramble() -> str:
    DIRECTIONS = ["U", "R", "L", "D", "F", "B"]
    MULTIPLIERS = ["", "2", "'"]
    s = ""
    prev_direction = random.choice(DIRECTIONS)
    DIRECTIONS.remove(prev_direction)
    for i in range(20):
        direction = random.choice(DIRECTIONS)
        DIRECTIONS.append(prev_direction)
        multiplier = random.choice(MULTIPLIERS)
        s += direction
        s += multiplier
        s += " "
        DIRECTIONS.remove(direction)
        prev_direction = direction
    return s.strip()


def run_scramble(cube: list, scramble: str) -> list:
    cube_state = cube
    for move in scramble.replace("'", "t").split():
        cube_state = globals()[move](cube_state)
    return cube_state


def main():
    cube = S
    scramble = gen_scramble()
    cube = run_scramble(cube, scramble)
    print_cube(cube)
    print("Scramble: " + scramble)


if __name__ == '__main__':
    main()
#
# for i in gen_scramble().split():
#     cube = run_scramble(cube, i)
#     print(i)
#     print_cube(cube)
#
# print()
# print_cube(L(U(S)))
