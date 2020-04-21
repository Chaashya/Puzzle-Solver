 
'''

Sanity check script to test your submission 'mySokobanSolver.py'


A different script (with different inputs) will be used for marking your code.

Make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse

from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_elem_action_seq
from mySokobanSolver import (can_go_there, 
                               solve_sokoban_macro )


def test_solve_sokoban_macro_1():
    '''
    # Some basic testing of the method of extracting location data from the warehouse
    '''
    puzzle_t2 ='#######\n#@ $ .#\n#######'
    wh = Warehouse()    
    wh.from_string(puzzle_t2)
    #wh.load_warehouse("./warehouses/warehouse_47.txt")
    answer=solve_sokoban_macro(wh)

    
    expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
    #expected_answer = [((4, 3), 'Right'), ((4, 4), 'Right')]
    fcn = test_solve_sokoban_macro_1
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)


def test_solve_sokoban_macro_2():
    '''
    # Some basic testing of the method of extracting location data from the warehouse
    '''
    puzzle_t2 ='#######\n#@ $#.#\n#######'
    wh = Warehouse()    
    wh.from_string(puzzle_t2)
    #wh.load_warehouse("./warehouses/warehouse_47.txt")
    answer=solve_sokoban_macro(wh)

    
    expected_answer = 'Impossible'
    #expected_answer = [((4, 3), 'Right'), ((4, 4), 'Right')]
    fcn = test_solve_sokoban_macro_2
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)


def test_solve_sokoban_macro_3():
    '''
    # Some basic testing of the method of extracting location data from the warehouse
     012345678910    
    0   ######
    1###      ###
    2#  $ $      #
    3# .   @    .#
    4############
    '''
    wh = Warehouse()    
    wh.load_warehouse("./warehouses/cab320_warehouse_8.txt")
    answer=solve_sokoban_macro(wh)
    expected_answer = [((2, 5), 'Down'), ((2, 3), 'Down'), ((3, 3), 'Left'), ((3, 5), 'Right'), ((3, 6), 'Right'), ((3, 7), 'Right'), ((3, 8), 'Right'), ((3, 9), 'Right'), ((3, 10), 'Right')]
    fcn = test_solve_sokoban_macro_3
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
    

if __name__ == "__main__":  
    test_solve_sokoban_macro_1()   

