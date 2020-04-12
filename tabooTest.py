from __future__ import print_function
from __future__ import division


from mySokobanSolver import taboo_cells
from sokoban import Warehouse, find_2D_iterator

expected_answer_3 = '''
#######
#X    #
#    X#
#######'''

puzzle_t3 = '''
#######
#@ $ .#
#. $  #
#######'''

"""def taboo_cells_tester(n):
    test_file = "./warehouses/warehouse_%s.txt" % str(n)
    wh = Warehouse()
    wh.load_warehouse(test_file)
    answer = taboo_cells(wh)
    print(set(find_2D_iterator(answer.split('\n'), "X")))
    print(answer)


if __name__ == "__main__":
    print("enter 'quit' to exit\n")
    c = input('Warehouse number: ')
    while c != 'quit':
        try:
            taboo_cells_tester(c)
        except FileNotFoundError as e:
            print("Warehouse %s does not exist\n" % str(c))
        c = input('Warehouse number: ')"""


def same_multi_line_strings(s1, s2):
    '''
    Auxiliary function to test two multi line string representing warehouses
    '''
    L1 = [s.rstrip() for s in s1.strip().split('\n')]
    L2 = [s.rstrip() for s in s2.strip().split('\n')]
    S1 = '\n'.join(L1)
    S2 = '\n'.join(L2)
    return S1 == S2


def taboo_cells_tester():
    wh = Warehouse()
    wh.extract_locations(puzzle_t3.split(sep='\n'))
    answer = taboo_cells(wh)
    print(answer)
    print(len(answer))
    print(expected_answer_3)
    print(len(expected_answer_3))
    if same_multi_line_strings(answer, expected_answer_3):
        print('Test taboo_cells passed\n')
    else:
        print('** Test taboo_cells failed\n')


if __name__ == "__main__":

    taboo_cells_tester()
