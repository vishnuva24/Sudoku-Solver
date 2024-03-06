from random import randint
from collections import Counter
from tkinter import *

matrix_ref = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 0): 3, (1, 1): 4, (1, 2): 5, (2, 0): 6, (2, 1): 7, (2, 2): 8}
class sudoku:
    def __init__(self, d):
        self.orig = d
        self.matrix = [[] for i in range(9)]
        self.row = [[] for i in range(9)]
        self.col = [[] for i in range(9)]
        for i in d:
            m_id = 0
            self.matrix[matrix_ref[((i[0] - i[0] % 3) // 3, (i[1] - i[1] % 3) // 3)]].append(d[i])
            self.row[i[0]].append(d[i])
            self.col[i[1]].append(d[i])
def check(s: sudoku):
    m = [s.matrix, s.row, s.col]
    for x in m:
        for i in x:
            i_counter = dict(Counter(i))
            for j in i_counter:
                if j != 0:
                    if i_counter[j] > 1:
                        return False
                    else:
                        continue
    return True
def finalcheck(s: sudoku):
    for i in s.row:
        for x in i:
            if x == 0:
                return False
    return True


t = {}
for i in range(9):
    for j in range(9):
        t[(i, j)] = 0
print(t)
def generate(t):
    print("Generating...")
    isbroken = True
    while isbroken:
        isbroken = False
        the_dict = t.copy()
        for i in range(1, 10):
            for j in matrix_ref:
                positions = set()
                is_invalid = True
                while is_invalid:
                    posx = j[0] * 3 + randint(0, 2)
                    posy = j[1] * 3 + randint(0, 2)
                    if len(positions) == 9:
                        isbroken = True
                        break
                    positions.add((posx, posy))
                    if the_dict[(posx, posy)] == 0:
                        cop = the_dict.copy()
                        cop[(posx, posy)] = i
                        is_invalid = not check(sudoku(cop))
                    else:
                        continue
                the_dict = cop
                if isbroken:
                    break
            if isbroken:
                break
        if isbroken:
            continue
        else:
            break
    the_dict = cop
    r = [[] for dcw in range(9)]
    for qwer in cop:
        r[qwer[0]].append(cop[qwer])
    for qwer in r:
        print(qwer)

generate(t)
counter_for_step1 = [0]
numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
def solver1(t):
    t = sudoku(t)
    counter_for_step1[0] += 1
    # Base condition for recursion
    if finalcheck(t):
        print("------------solved-----------")
        for qwer in t.row:
            print(qwer)
        return 0
    position_options_dict = {}
    for pos in t.orig:
        if not t.orig[pos]:
            m = ((pos[0] - pos[0] % 3) // 3, (pos[1] - pos[1] % 3) // 3)
            mat = numbers - set(t.matrix[matrix_ref[m]])
            ro = numbers - set(t.row[pos[0]])
            co = numbers - set(t.col[pos[1]])
            possibilities = mat & ro & co
            if len(possibilities) == 1:
                t.orig[pos] = possibilities.pop()
            else:
                position_options_dict[pos] = list(possibilities)
        if counter_for_step1[0] >= 10000: # method 2 after max possible method 1 independently
            t = sudoku(t.orig)
            for matrix in matrix_ref:
                number_to_positions_dict = {no:[] for no in range(1, 10)}
                tl = (matrix[0]*3, matrix[1]*3)
                br = (matrix[0]*3 + 2, matrix[1]*3 + 2)
                for i in position_options_dict:
                    if tl[0] <= i[0] <= br[0] and tl[1] <= i[1] <= br[1]:
                        for iterator in position_options_dict[i]:
                            number_to_positions_dict[iterator].append(i)
                #print(matrix, number_to_positions_dict)
                for i in number_to_positions_dict:
                    if len(number_to_positions_dict[i]) == 1:
                        t.orig[number_to_positions_dict[i][0]] = i
            for row in range(9):
                if 0 in t.row[row]:
                    cpy = set.difference(numbers, set(t.row[row].copy()))
                    if len(cpy) == 1:
                        for i in range(9):
                            if t.row[row][i] == 0:
                                t.orig[(row, i)] = cpy.pop()
            for colu in range(9):
                if 0 in t.col[colu]:
                    nmp = set.difference(numbers, set(t.col[colu].copy()))
                    if len(nmp) == 1:
                        for i in range(9):
                            if t.col[colu][i] == 0:
                                t.orig[(i, colu)] = nmp.pop()
            continue
    for qwer in t.row:
        print(qwer)
    print("------------------------------")
    '''print(position_options_dict)'''
    solver1(t.orig)
    return 0


