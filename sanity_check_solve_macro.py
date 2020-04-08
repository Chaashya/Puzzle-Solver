 
'''

Sanity check script to test your submission 'mySokobanSolver.py'


A different script (with different inputs) will be used for marking your code.

Make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse

from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_elem_action_seq
from mySokobanSolver import (can_go_there, 
                               solve_sokoban_macro )


def test_solve_sokoban_macro():
    '''
    # Some basic testing of the method of extracting location data from the warehouse
    '''
    #puzzle_t2 ='#######\n#@ $ .#\n#######'
    wh = Warehouse()    
    #wh.from_string(puzzle_t2)
    wh.load_warehouse("./warehouses/warehouse_47.txt")
    answer=solve_sokoban_macro(wh)

    
    #expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
    expected_answer = [((4, 3), 'Right'), ((4, 4), 'Right')]
    fcn = test_solve_sokoban_macro
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
    

if __name__ == "__main__":
    pass    
    test_solve_sokoban_macro()   

