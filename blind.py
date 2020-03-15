from functools import partial
from collections import namedtuple
import random
import sys

"""""
    The names of the facelet positions of the cube
                  |************|
                  |* 0** 1** 2*|
                  |************|
                UW|* 3** 4** 5*|
                  |************|
                  |* 6** 7** 8*|
                  |************|     RR          BB
     |************|************|************|************|
     |*27**28**29*|* 9**10**11*|*36**37**38*|*45**46**47*|
   LO|************|************|************|************|
     |*30**31**32*|*12**13**14*|*39**40**41*|*48**49**50*|
     |************|************|************|************|
     |*33**34**35*|*15**16**17*|*42**43**44*|*51**52**53*|
     |************|************|************|************|
                  |************|\
                  |*18**19**20*| \
                  |************|  FG
                DY|*21**22**23*|
                  |************|
                  |*24**25**26*|
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


TRANSFORMS = {
        'U': [6, 3, 0, 7, 4, 1, 8, 5, 2, 36, 37, 38, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 9, 10, 11, 30, 31, 32, 33, 34, 35, 45, 46, 47, 39, 40, 41, 42, 43, 44, 27, 28, 29, 48, 49, 50, 51, 52, 53],
        'Ut': [2, 5, 8, 1, 4, 7, 0, 3, 6, 27, 28, 29, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 45, 46, 47, 30, 31, 32, 33, 34, 35, 9, 10, 11, 39, 40, 41, 42, 43, 44, 36, 37, 38, 48, 49, 50, 51, 52, 53],
        'R': [0, 1, 11, 3, 4, 14, 6, 7, 17, 9, 10, 20, 12, 13, 23, 15, 16, 26, 18, 19, 51, 21, 22, 48, 24, 25, 45, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 39, 36, 43, 40, 37, 44, 41, 38, 8, 46, 47, 5, 49, 50, 2, 52, 53],
        'Rt': [0, 1, 51, 3, 4, 48, 6, 7, 45, 9, 10, 2, 12, 13, 5, 15, 16, 8, 18, 19, 11, 21, 22, 14, 24, 25, 17, 27, 28, 29, 30, 31, 32, 33, 34, 35, 38, 41, 44, 37, 40, 43, 36, 39, 42, 26, 46, 47, 23, 49, 50, 20, 52, 53],
        'L': [53, 1, 2, 50, 4, 5, 47, 7, 8, 0, 10, 11, 3, 13, 14, 6, 16, 17, 9, 19, 20, 12, 22, 23, 15, 25, 26, 33, 30, 27, 34, 31, 28, 35, 32, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 24, 48, 49, 21, 51, 52, 18],
        'Lt': [9, 1, 2, 12, 4, 5, 15, 7, 8, 18, 10, 11, 21, 13, 14, 24, 16, 17, 53, 19, 20, 50, 22, 23, 47, 25, 26, 29, 32, 35, 28, 31, 34, 27, 30, 33, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 6, 48, 49, 3, 51, 52, 0],
        'D': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 33, 34, 35, 24, 21, 18, 25, 22, 19, 26, 23, 20, 27, 28, 29, 30, 31, 32, 51, 52, 53, 36, 37, 38, 39, 40, 41, 15, 16, 17, 45, 46, 47, 48, 49, 50, 42, 43, 44],
        'Dt': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 42, 43, 44, 20, 23, 26, 19, 22, 25, 18, 21, 24, 27, 28, 29, 30, 31, 32, 15, 16, 17, 36, 37, 38, 39, 40, 41, 51, 52, 53, 45, 46, 47, 48, 49, 50, 33, 34, 35],
        'F': [0, 1, 2, 3, 4, 5, 35, 32, 29, 15, 12, 9, 16, 13, 10, 17, 14, 11, 42, 39, 36, 21, 22, 23, 24, 25, 26, 27, 28, 18, 30, 31, 19, 33, 34, 20, 6, 37, 38, 7, 40, 41, 8, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
        'Ft': [0, 1, 2, 3, 4, 5, 36, 39, 42, 11, 14, 17, 10, 13, 16, 9, 12, 15, 29, 32, 35, 21, 22, 23, 24, 25, 26, 27, 28, 8, 30, 31, 7, 33, 34, 6, 20, 37, 38, 19, 40, 41, 18, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
        'B': [38, 41, 44, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 27, 30, 33, 2, 28, 29, 1, 31, 32, 0, 34, 35, 36, 37, 26, 39, 40, 25, 42, 43, 24, 51, 48, 45, 52, 49, 46, 53, 50, 47],
        'Bt': [33, 30, 27, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 44, 41, 38, 24, 28, 29, 25, 31, 32, 26, 34, 35, 36, 37, 0, 39, 40, 1, 42, 43, 2, 47, 50, 53, 46, 49, 52, 45, 48, 51],
        'X': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 53, 52, 51, 50, 49, 48, 47, 46, 45, 29, 32, 35, 28, 31, 34, 27, 30, 33, 42, 39, 36, 43, 40, 37, 44, 41, 38, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        'Xt': [53, 52, 51, 50, 49, 48, 47, 46, 45, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 33, 30, 27, 34, 31, 28, 35, 32, 29, 38, 41, 44, 37, 40, 43, 36, 39, 42, 26, 25, 24, 23, 22, 21, 20, 19, 18],
        'Y': [6, 3, 0, 7, 4, 1, 8, 5, 2, 36, 37, 38, 39, 40, 41, 42, 43, 44, 20, 23, 26, 19, 22, 25, 18, 21, 24, 9, 10, 11, 12, 13, 14, 15, 16, 17, 45, 46, 47, 48, 49, 50, 51, 52, 53, 27, 28, 29, 30, 31, 32, 33, 34, 35],
        'Yt': [2, 5, 8, 1, 4, 7, 0, 3, 6, 27, 28, 29, 30, 31, 32, 33, 34, 35, 24, 21, 18, 25, 22, 19, 26, 23, 20, 45, 46, 47, 48, 49, 50, 51, 52, 53, 9, 10, 11, 12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41, 42, 43, 44],
        'Z': [33, 30, 27, 34, 31, 28, 35, 32, 29, 15, 12, 9, 16, 13, 10, 17, 14, 11, 42, 39, 36, 43, 40, 37, 44, 41, 38, 18, 21, 24, 19, 22, 25, 20, 23, 26, 6, 3, 0, 7, 4, 1, 8, 5, 2, 51, 48, 45, 52, 49, 46, 53, 50, 47],
        'Zt': [36, 39, 42, 37, 40, 43, 38, 41, 44, 11, 14, 17, 10, 13, 16, 9, 12, 15, 29, 32, 35, 28, 31, 34, 27, 30, 33, 8, 5, 2, 7, 4, 1, 6, 3, 0, 26, 23, 20, 25, 22, 19, 24, 21, 18, 47, 50, 53, 46, 49, 52, 45, 48, 51],
        }

class Cube():

    COLORS = ['\x1b[38;5;15m'] * 9 + ['\x1b[38;5;2m'] * 9 + ['\x1b[38;5;226m'] * 9 + ['\x1b[38;5;214m'] * 9 + ['\x1b[38;5;1m'] * 9 + ['\x1b[38;5;4m'] * 9

    def __init__(self, cube=None):
        if cube:
            self.transform = cube.transform
            self.revtransform = cube.revtransform

    def set_transforms(self, transform, revtransform):
        self.transform = transform
        self.revtransform = revtransform

    def _negate(self):
        self.transform, self.revtransform = self.revtransform, self.transform

    def solved(self):
        return self == I

    def _apply(self, cube):
        c = Cube()
        c.set_transforms([self.transform[i] for i in cube.transform], [cube.revtransform[i] for i in self.revtransform])
        return c

    def __add__(self, other):
        return self._apply(other)

    def __mul__(self, exp):
        c = Cube(self)
        if exp == -1:
            return -c
        for i in range(abs(exp) - 1):
            if exp > 0:
                c = self + c
            else:
                c = self - c
        return c

    def __neg__(self):
        c = Cube(self)
        c._negate()
        return c

    def __sub__(self, other):
        return self._apply(-other)

    def __eq__(self, other):
        return self.transform == other.transform

    def __repr__(self):
        return str(self.transform)

    # def print_target(self):
    #     c = self.transform
    #     def f(i):
    #         return self.COLORS[i] + "\u2588\u2588"  #f'{i:2d}'#
    #     print(f'{f(c[3])}\n{f(c[28])}\x1b[0m')

    def __str__(self):
        c = self.transform
        def f(i):
            if c[i] == I.transform[i]:
                return self.COLORS[c[i]] + "\u2592\u2592"  #f'{i:2d}'#
            return self.COLORS[c[i]] + "\u2588\u2588"  #f'{i:2d}'#

        return \
f"""
      {f(0)}{f(1)}{f(2)}
      {f(3)}{f(4)}{f(5)}
      {f(6)}{f(7)}{f(8)}
{f(27)}{f(28)}{f(29)}{f(9)}{f(10)}{f(11)}{f(36)}{f(37)}{f(38)}{f(45)}{f(46)}{f(47)}
{f(30)}{f(31)}{f(32)}{f(12)}{f(13)}{f(14)}{f(39)}{f(40)}{f(41)}{f(48)}{f(49)}{f(50)}
{f(33)}{f(34)}{f(35)}{f(15)}{f(16)}{f(17)}{f(42)}{f(43)}{f(44)}{f(51)}{f(52)}{f(53)}
      {f(18)}{f(19)}{f(20)}
      {f(21)}{f(22)}{f(23)}
      {f(24)}{f(25)}{f(26)}
\x1b[0m"""

I = Cube()
I.set_transforms(list(range(54)), list(range(54)))

U = Cube()
U.set_transforms(TRANSFORMS['U'], TRANSFORMS['Ut'])
R = Cube()
R.set_transforms(TRANSFORMS['R'], TRANSFORMS['Rt'])
L = Cube()
L.set_transforms(TRANSFORMS['L'], TRANSFORMS['Lt'])
D = Cube()
D.set_transforms(TRANSFORMS['D'], TRANSFORMS['Dt'])
F = Cube()
F.set_transforms(TRANSFORMS['F'], TRANSFORMS['Ft'])
B = Cube()
B.set_transforms(TRANSFORMS['B'], TRANSFORMS['Bt'])
X = Cube()
X.set_transforms(TRANSFORMS['X'], TRANSFORMS['Xt'])
Y = Cube()
Y.set_transforms(TRANSFORMS['Y'], TRANSFORMS['Yt'])
Z = Cube()
Z.set_transforms(TRANSFORMS['Z'], TRANSFORMS['Zt'])

M = Cube(-L + R - X)
E = Cube(-Y -D + U)
S = Cube(Z + B - F)

r = Cube(-M + R)
l = Cube(M + L)
f = Cube(S + F)
d = Cube(E + D)

#  Blind edges
BE = {
        'A': Cube(-l * 2 - D + L * 2),
        'C': Cube(l - D - L - d + L),
        'D': Cube(I),
        'E': Cube(-L + d -L),
        'F': Cube(-d + L),
        'G': Cube(-L -d + L),
        'H': Cube(d - L),
        'I': Cube(l + D + L * 2),
        'J': Cube(d * 2 + L),
        'K': Cube(-D - L -d + L),
        'L': Cube(-L),
        'N': Cube(d + L),
        'O': Cube(D * 2 - L - d + L),
        'P': Cube(-d - L),
        'Q': Cube(-l + D + L * 2),
        'R': Cube(L),
        'S': Cube(-l - D + L * 2),
        'T': Cube(d * 2 - L),
        'U': Cube(-D + L * 2),
        'V': Cube(D * 2 + L * 2),
        'W': Cube(D + L * 2),
        'X': Cube(L * 2),
}

def edge_swap(letter):
    return Cube(BE[letter] + PLL['T'] - BE[letter])

PLL = {
    'T': Cube(R + U - R - U - R + F + R * 2 - U - R - U + R + U - R - F),
    'Ja': Cube(X + R * 2 + F + R - F + R + U * 2 - r + U + r + U * 2 - X),
    'Jb': Cube(R + U - R - F + R + U - R - U - R + F + R * 2 - U - R - U),
    'Y': Cube(F + R - U - R - U + R + U - R - F + R + U - R - U - R + F + R - F),
}

STR_2_CUBE = {
        'U': U,
        'U\'': -U,
        'U2': U * 2,
        'R': R,
        'R\'': -R,
        'R2': R * 2,
        'L': L,
        'L\'': -L,
        'L2': L * 2,
        'D': D,
        'D\'': -D,
        'D2': D * 2,
        'F': F,
        'F\'': -F,
        'F2': F * 2,
        'B': B,
        'B\'': -B,
        'B2': B * 2,
}

SUNE = Cube(R + U - R + U + R + U*2 -R)
# print(edge_swap('U') + edge_swap('V') + edge_swap('W') + edge_swap('X'))
# print(Cube(PLL['Y'] - PLL['Y']).solved())

# Print edge targets
# for k,v in BE.items():
#     print(k)
#     v.print_target()
#     print('---')

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


def run_scramble(cube: Cube, scramble: str) -> list:
    for move in scramble.split():
        cube += STR_2_CUBE[move]
    return cube


def main():
    global I
    I += X * 2 - Y
    cube = I
    scramble = gen_scramble()
    # scramble = "D' F L F' U' F2 L R2 B' F U' B F D2 U2 R L2 B' F D"
    cube = run_scramble(cube, scramble)
    print(cube)
    print("Scramble: " + scramble)
    edges = input().upper().strip()
    print(f'Len: {len(edges)}')
    for l in edges:
        cube += edge_swap(l)
        print(l)
        print(cube)
    print(cube)


if __name__ == '__main__':
    main()
