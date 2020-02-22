from functools import partial
import random

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
I = list(range(54))   # Initial cube

COLORS = ['\x1b[38;5;15m'] * 9 + ['\x1b[38;5;2m'] * 9 + ['\x1b[38;5;226m'] * 9 + ['\x1b[38;5;214m'] * 9 + ['\x1b[38;5;1m'] * 9 + ['\x1b[38;5;4m'] * 9

TRANSFORMS = {
        'U': [6, 3, 0, 7, 4, 1, 8, 5, 2, 36, 37, 38, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 9, 10, 11, 30, 31, 32, 33, 34, 35, 45, 46, 47, 39, 40, 41, 42, 43, 44, 27, 28, 29, 48, 49, 50, 51, 52, 53],
        'R': [0, 1, 11, 3, 4, 14, 6, 7, 17, 9, 10, 20, 12, 13, 23, 15, 16, 26, 18, 19, 51, 21, 22, 48, 24, 25, 45, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 39, 36, 43, 40, 37, 44, 41, 38, 8, 46, 47, 5, 49, 50, 2, 52, 53],
        'L': [53, 1, 2, 50, 4, 5, 47, 7, 8, 0, 10, 11, 3, 13, 14, 6, 16, 17, 9, 19, 20, 12, 22, 23, 15, 25, 26, 33, 30, 27, 34, 31, 28, 35, 32, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 24, 48, 49, 21, 51, 52, 18],
        'D': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 33, 34, 35, 24, 21, 18, 25, 22, 19, 26, 23, 20, 27, 28, 29, 30, 31, 32, 51, 52, 53, 36, 37, 38, 39, 40, 41, 15, 16, 17, 45, 46, 47, 48, 49, 50, 42, 43, 44],
        'F': [0, 1, 2, 3, 4, 5, 35, 32, 29, 15, 12, 9, 16, 13, 10, 17, 14, 11, 42, 39, 36, 21, 22, 23, 24, 25, 26, 27, 28, 18, 30, 31, 19, 33, 34, 20, 6, 37, 38, 7, 40, 41, 8, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
        'B': [38, 41, 44, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 27, 30, 33, 2, 28, 29, 1, 31, 32, 0, 34, 35, 36, 37, 26, 39, 40, 25, 42, 43, 24, 51, 48, 45, 52, 49, 46, 53, 50, 47],
        'X': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 53, 52, 51, 50, 49, 48, 47, 46, 45, 29, 32, 35, 28, 31, 34, 27, 30, 33, 42, 39, 36, 43, 40, 37, 44, 41, 38, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        'Y': [6, 3, 0, 7, 4, 1, 8, 5, 2, 36, 37, 38, 39, 40, 41, 42, 43, 44, 20, 23, 26, 19, 22, 25, 18, 21, 24, 9, 10, 11, 12, 13, 14, 15, 16, 17, 45, 46, 47, 48, 49, 50, 51, 52, 53, 27, 28, 29, 30, 31, 32, 33, 34, 35],
        'Z': [33, 30, 27, 34, 31, 28, 35, 32, 29, 15, 12, 9, 16, 13, 10, 17, 14, 11, 42, 39, 36, 43, 40, 37, 44, 41, 38, 18, 21, 24, 19, 22, 25, 20, 23, 26, 6, 3, 0, 7, 4, 1, 8, 5, 2, 51, 48, 45, 52, 49, 46, 53, 50, 47],
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
X = partial(A, transform=TRANSFORMS['X'])
Y = partial(A, transform=TRANSFORMS['Y'])
Z = partial(A, transform=TRANSFORMS['Z'])

U2 = partial(A, transform=U(U(I)))
Ut = partial(A, transform=U(U(U(I))))
R2 = partial(A, transform=R(R(I)))
Rt = partial(A, transform=R(R(R(I))))
L2 = partial(A, transform=L(L(I)))
Lt = partial(A, transform=L(L(L(I))))
D2 = partial(A, transform=D(D(I)))
Dt = partial(A, transform=D(D(D(I))))
F2 = partial(A, transform=F(F(I)))
Ft = partial(A, transform=F(F(F(I))))
B2 = partial(A, transform=B(B(I)))
Bt = partial(A, transform=B(B(B(I))))
Xt = partial(A, transform=X(X(X(I))))
Yt = partial(A, transform=Y(Y(Y(I))))
Zt = partial(A, transform=Z(Z(Z(I))))
M  = partial(A, transform=(Xt(R(Lt(I)))))
Mt = partial(A, transform=(M(M(M(I)))))
E  = partial(A, transform=(U(Dt(Yt(I)))))
Et = partial(A, transform=(E(E(E(I)))))
S  = partial(A, transform=(Ft(B(Z(I)))))
St  = partial(A, transform=(S(S(S(I)))))

r = partial(A, transform=(R(Mt(I))))
rt = partial(A, transform=(Rt(M(I))))
l = partial(A, transform=(L(M(I))))
lt = partial(A, transform=(Lt(Mt(I))))
f = partial(A, transform=(F(S(I))))
ft = partial(A, transform=(Ft(St(I))))

Tperm = partial(A, transform=(Ft(Rt(U(R(Ut(Rt(Ut(R2(F(Rt(Ut(Rt(U(R(I))))))))))))))))
Yperm = partial(A, transform=(R(U(R2(U(Lt(U2(R(Ut(Rt(U2(R(L(Ut(R(Ut(Rt(I))))))))))))))))))

JAperm = partial(A, transform=(Xt(U2(r(U(rt(U2(R(Ft(R(F(R2(X(I))))))))))))))




def print_cube(c):
    def f(i):
        return COLORS[i] + "\u2588\u2588"  #f'{i:2d}'#

    print("      {}{}{}".format(f(c[0]), f(c[1]), f(c[2])))
    print("      {}{}{}".format(f(c[3]), f(c[4]), f(c[5])))
    print("      {}{}{}".format(f(c[6]), f(c[7]), f(c[8])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[27]), f(c[28]), f(c[29]), f(c[9]), f(c[10]), f(c[11]), f(c[36]), f(c[37]), f(c[38]), f(c[45]), f(c[46]), f(c[47])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[30]), f(c[31]), f(c[32]), f(c[12]), f(c[13]), f(c[14]), f(c[39]), f(c[40]), f(c[41]), f(c[48]), f(c[49]), f(c[50])))
    print("{}{}{}{}{}{}{}{}{}{}{}{}".format(f(c[33]), f(c[34]), f(c[35]), f(c[15]), f(c[16]), f(c[17]), f(c[42]), f(c[43]), f(c[44]), f(c[51]), f(c[52]), f(c[53])))
    print("      {}{}{}".format(f(c[18]), f(c[19]), f(c[20])))
    print("      {}{}{}".format(f(c[21]), f(c[22]), f(c[23])))
    print("      {}{}{}".format(f(c[24]), f(c[25]), f(c[26])))
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
    # for move in scramble.replace("'", "t").split():
    #    cube_state = globals()[move](cube_state)
    return cube_state


def main():
    cube = I
    scramble = gen_scramble()
    cube = run_scramble(cube, scramble)
    print_cube(cube)
    print_cube(Xt(JAperm(X((cube)))))
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
