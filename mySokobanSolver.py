'''
    2020 CAB320 Sokoban assignment
The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.
You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and results in a fail for the test of your code.
This is not negotiable!
'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import search
import sokoban


import time

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [ (1234567, 'Chaashya', 'Fernando'), (1234568, 'Joseph', 'Hopper'), ('n9922121', 'Riley', 'Albiston') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''
    Identify the taboo cells of a warehouse. A cell inside a warehouse is
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes,
    only consider the walls and the target  cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of
             these cells is a target.

    @param warehouse:
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with
       a '#' and the taboo cells marked with a 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''

    # IDENTIFIERS
    taboo_cell = 'X'
    wall_cell = '#'
    ignore = ['$', '@']
    target = ['!', '*', '.']
    space = ' '

    def corner_check(warehouse, x, y, wall=0):
        '''
        Check to see if current cell is a corner; if there is a wall
        above/below and a wall to the left/right.
        '''
        ab_walls = 0
        lr_walls = 0

        for (dx, dy) in [(0, 1), (0, -1)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                ab_walls += 1

        for (dx, dy) in [(1, 0), (-1, 0)]:
            if warehouse[y + dy][x + dx] == wall_cell:
                lr_walls += 1

        if wall:
            return (ab_walls >= 1) or (lr_walls >= 1)
        else:
            return (ab_walls >= 1) and (lr_walls >= 1)

    # Represent in single string
    final_warehouse = str(warehouse)

    # remove if not wall/ target
    for item in ignore:
        final_warehouse = final_warehouse.replace(item, space)

    # 2D array representation
    warehouse_array = [list(line) for line in final_warehouse.split('\n')]

    # Check for corners that are not targets through iteration
    for y in range(len(warehouse_array) - 1):
        inside = False
        for x in range(len(warehouse_array[0]) - 1):
            # while going through rows, if first wall is hit:
            # then we are inside the warehouse
            if not inside:
                if warehouse_array[y][x] == wall_cell:
                    inside = True
            else:
                # if all cells to the right of current cell are empty;
                # empty space until the end
                # then we are now outside the warehouse
                if all([cell == ' ' for cell in warehouse_array[y][x:]]):
                    break
                if warehouse_array[y][x] not in target:
                    if warehouse_array[y][x] != wall_cell:
                        if corner_check(warehouse_array, x, y):
                            warehouse_array[y][x] = taboo_cell

    # Fill in taboo_cells
    for y in range(1, len(warehouse_array) - 1):
        for x in range(1, len(warehouse_array[0]) - 1):
            # Find taboo cell
            if warehouse_array[y][x] == taboo_cell and corner_check(warehouse_array, x, y):
                row = warehouse_array[y][x + 1:]
                col = [row[x] for row in warehouse_array[y + 1:][:]]
                # Fill in taboo L - R
                for x2 in range(len(row)):
                    if row[x2] in target or row[x2] == wall_cell:
                        break
                    if row[x2] == taboo_cell \
                            and corner_check(warehouse_array, x2 + x + 1, y):
                        if all([corner_check(warehouse_array, x3, y, 1)
                                for x3 in range(x + 1, x2 + x + 1)]):
                            for x4 in range(x + 1, x2 + x + 1):
                                warehouse_array[y][x4] = 'X'

                # Fill in taboo_cells moving U - D
                for y2 in range(len(col)):
                    if col[y2] in target or col[y2] == wall_cell:
                        break
                    if col[y2] == taboo_cell \
                            and corner_check(warehouse_array, x, y2 + y + 1):
                        if all([corner_check(warehouse_array, x, y3, 1)
                                for y3 in range(y + 1, y2 + y + 1)]):
                            for y4 in range(y + 1, y2 + y + 1):
                                warehouse_array[y4][x] = 'X'

    # convert warehouse back into string
    final_warehouse = '\n'.join([''.join(line) for line in warehouse_array])

    # remove target cells
    for item in target:
        final_warehouse = final_warehouse.replace(item, space)

    return final_warehouse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse):
        
        self.warehouse = warehouse
        self.initial = warehouse.__str__()
#        self.goal = self.convert_state_to_goal(warehouse)
        self.goal = self.convert_state_to_test_goal(warehouse)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        self.warehouse.from_string(state)
        wall_check_coords = self.check_for_wall(self.warehouse)
        L = []
        
        if wall_check_coords[0] not in list(self.warehouse.walls):
            L.append('Up')
        if wall_check_coords[1] not in list(self.warehouse.walls):
            L.append('Down')
        if wall_check_coords[2] not in list(self.warehouse.walls):
            L.append('Left')
        if wall_check_coords[3] not in list(self.warehouse.walls):
            L.append('Right')
            
        return L

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        self.warehouse.from_string(state)
#        assert action in self.actions(self.warehouse)
        worker_coords = list(self.warehouse.worker)
        
        if action == 'Up':
            worker_coords[1] -= 1
            self.warehouse.worker = tuple(worker_coords)
            return self.warehouse.__str__()
        if action == 'Down':
            worker_coords[1] += 1
            self.warehouse.worker = tuple(worker_coords)
            return self.warehouse.__str__()
        if action == 'Left':
            worker_coords[0] -= 1
            self.warehouse.worker = tuple(worker_coords)
            return self.warehouse.__str__()
        if action == 'Right':
            worker_coords[0] += 1
            self.warehouse.worker = tuple(worker_coords)
            return self.warehouse.__str__()
        
    def print_solution(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        path = goal_node.path()
        # print the solution
        print ("Solution takes {0} steps from the initial state".format(len(path)-1))
        print (path[0].state)
        print ("to the goal state")
        print (path[-1].state)
        print ("\nBelow is the sequence of moves\n")
        for node in path:
            if node.action is not None:
                print (format(node.action))
            print (node.state)
        
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1    
    def h(self, n):
        return 0

        
    def convert_state_to_goal(self,warehouse):
        goal_wh = warehouse.copy(boxes = warehouse.targets) 
        return goal_wh.__str__()
    def convert_state_to_test_goal(self,warehouse):
        goal_wh = warehouse.copy(worker = warehouse.targets[0])
        return goal_wh.__str__()
    
    def check_for_wall(self,state):
        worker_coords = list(state.worker) 
        wall_check_coords = [(worker_coords[0],worker_coords[1]-1),
                             (worker_coords[0],worker_coords[1]+1),
                             (worker_coords[0]-1,worker_coords[1]),
                             (worker_coords[0]+1,worker_coords[1])]
        return wall_check_coords


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def check_elem_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object
    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    failed = 'Impossible'
    x, y = warehouse.worker
    walls = warehouse.walls
    boxes = warehouse.boxes

    # iterate through each action from the action sequence
    for action in action_seq:
        if(action == 'Left'):
            x -= 1
            print(action)
            print(x, y)
            # check if the action will put the player into a wall
            if(x, y) in walls:
                print("Failed because the player moved into a wall")
                return failed
            # check if the next postion contains a box
            if(x, y) in boxes:
                # check if position next to the box contains another box or wall
                if (x-1, y) in boxes or (x-1, y) in walls:
                    print("Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
                    return failed


        elif(action == 'Right'):
            x += 1
            print(action)
            print(x, y)
            # check if the action will put the player into a wall
            if(x, y) in walls:
                print("Failed because the player moved into a wall")
                return failed
            # check if the next postion contains a box
            if(x, y) in boxes:
                # check if position next to the box contains another box or wall
                if (x+1, y) in boxes or (x+1, y) in walls:
                    print("Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
                    return failed


        elif(action == 'Up'):
            y -= 1
            print(action)
            print(x, y)
            # check if the action will put the player into a wall
            if(x, y) in walls:
                print("Failed because the player moved into a wall")
                return failed
            # check if the next postion contains a box
            if(x, y) in boxes:
                # check if position next to the box contains another box or wall
                if (x, y-1) in boxes or (x, y-1) in walls:
                    print("Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
                    return failed

        elif(action == 'Down'):
            y += 1
            print(action)
            print(x, y)
            # check if the action will put the player into a wall
            if(x, y) in walls:
                print("Failed because the player moved into a wall")
                return failed
            # check if the next postion contains a box
            if(x, y) in boxes:
                # check if position next to the box contains another box or wall
                if (x, y+1) in boxes or (x, y+1) in walls:
                    print("Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
                    return failed
    
    # move the worker to the new postion
    warehouse.worker = x, y
    print(str(warehouse))

    return str(warehouse)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    In this scenario, the cost of all (elementary) actions is one unit.
    @param warehouse: a valid Warehouse object
    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    # "INSERT YOUR CODE HERE"

    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    @param warehouse: a valid Warehouse object
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    warehouse_squares = str(warehouse).split('\n')

    index = 0
    for strings in warehouse_squares:
        warehouse_squares[index] = list(strings)
        index += 1

    x_size = len(warehouse_squares[0])
    y_size = len(warehouse_squares)

    workerx = warehouse.worker[0]
    workery = warehouse.worker[1]

    dstx = dst[0]
    dsty = dst[1]
    
    for box in warehouse.boxes:
        boxx = box[0]
        boxy = box[1]
        
        # box is on goal - worker cannot move here
        if box == dst: 
            return False 
        
        # If box y location is within worker y and goal y 
        if boxy in range(workery, dsty) :
            # If box is in same row - will collide 
            if boxx == workerx:
                return False 
        
        # If box x location is within worker x and goal x 
        if boxx in range(workerx, dstx) :
            # If box is in same column - will collide 
            if boxy == workery: 
                return False     
        
        # If goal is out of the x bounds of the warehouse 
        if dstx <= 0 or dstx > x_size:
            return False
       
        # If goal is out of the y bounds of the warehouse 
        if dsty <= 0 or dsty > y_size:
            return False
    
    return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def Reverse(tuples): 
    new_list  =[]
    new_tup = () 
    for i, k in tuples: 
        new_tup = (k,i) 
        new_list.append(new_tup)
    return new_list  


def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    In this scenario, the cost of all (macro) actions is one unit. 
    @param warehouse: a valid Warehouse object
    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''

    '''
    Test puzzle layout from sanity_check.py

     0123456  
    0#######
    1#@ $ .#
    2#######

    possible moves by the box: ['Left', 'Right']
    '''

    '''
     012345678910    
    0  #######
    1###     #
    2# $ $   #
    3# ### #####
    4# @ . .   #
    5#   ###   #
    6##### #####
    '''

    
    '''
    failed = 'Impossible'
    x, y = warehouse.worker
    walls = warehouse.walls
    boxes = warehouse.boxes
    targets = warehouse.targets
    rows = warehouse.nrows
    cols = warehouse.ncols

    print("Initial Worker x, y:",x, y)
    print("Initial Boxes x, y:", boxes)
    print("Targets:", targets)
#    print("Walls:", walls)
    print("Rows:", rows)
    print("Cols:", cols)
    print()
    '''

    def h(n):
        '''
        Heurtistic - Uses Manhattan Distance
        To make the heuristic admissible it should be optimisitc. It should
        underestimate the cost from the current state to the goal state.

        Possible option: Use the sum of the manhattan distance of each box 
        to it's nearest target.

        returns a int value which is an estimate of the puzzles distance to
        the goal state.
        '''
        print("\nFrom heuristic function:")

        state = n.state
        print(state)
        
        w = warehouse.worker
        b = warehouse.boxes
        t = warehouse.targets[0]
        print(w)
        print(b)
        print(t)

        heuristic = abs(w[0]-t[0]) + abs(w[1]-t[1])
        print(heuristic)

        return heuristic

    M = search.astar_graph_search(SokobanPuzzle(warehouse), h)

    '''
    SB = SokobanPuzzle(warehouse)
    print("\nInital set of possible actions:")
    print(SB.actions(SB.initial))
    '''

    p = M.path()
    print('\nPath actions:')
    p_actions = [e.action for e in p]
    print(p_actions)
    print('\nPath states:')
    p_state = [e.state for e in p]
    print(p_state)
    
    worker_loc = []
    for s in p_state:
        #print('\nstate:')
        #print(s)
        warehouse.extract_locations(s.split(sep='\n'))
        #print(warehouse.worker)
        worker_loc.append(warehouse.worker)


    print('\nWorker locations (x, y)')
    print(worker_loc)
    print('\nWorker locations (y, x)')
    new_list = Reverse(worker_loc)
    print(new_list) 


    z = list(zip(new_list, p_actions))
    print('\nWorker location and action zipped together and the starting state removed:')
    del z[0]
    print(z)

    '''
    # Test distance for boxes to targets (heuristic, manhattan distance?!?)

    for this test manhattan distance == 2 (1 box and 1 target)

    1. Test possible moves of the box(s)

    2. Test if the worker can move to the OPPOSITE side of the possible box moves

    3. Choose next move

    if (M == None):
        puzzle Impossible

    if (box == goal):
        puzzle solved
    
    '''

    return z

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    The ith box is initially at position 'warehouse.boxes[i]'.
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)
    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
    pass
    
    '''
    #
    # testing the SokobanPuzzle() class
    #
    '''  
    ''' 
    test_string = "#############\n#@##        #\n#           #\n#  .        #\n#       $   #\n#           #\n#############"  
    wh = sokoban.Warehouse()
#    wh.load_warehouse("./warehouses/warehouse_47.txt")
    
    wh.from_string(test_string)
    SB = SokobanPuzzle(wh)
    print("Initial state:")
    print(SB.initial)
    print("\nGoal state:")
    print(SB.goal)
    print("\nInital set of possible actions:")
    print(SB.actions(SB.initial))

    
    t0 = time.time()
    sol_ts = search.astar_graph_search(SB)  # graph search version
    t1 = time.time()
    print ('\nA* Solver took {:.6f} seconds'.format(t1-t0))


    SB.print_solution(sol_ts)
    
#    print(SB.result(wh.__str__(),'Down'))
#    print(SB.result(wh.__str__(),'Right'))
    '''


    '''
    puzzle_t2 ='#######\n#@ $ .#\n#######'
    wh = sokoban.Warehouse()    
    wh.from_string(puzzle_t2)

    solve_sokoban_macro(wh)
    '''