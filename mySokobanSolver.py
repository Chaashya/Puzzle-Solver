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
from search import astar_graph_search
import math

import time

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [('n10122702', 'Chaashya', 'Fernando'), ('n9934847', 'Joseph', 'Modolo'), ('n9922121', 'Riley', 'Albiston')]

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

    def __init__(self, warehouse,allow_taboo_push = False, macro = False, weighted = False, box_weights = None):

        self.warehouse = warehouse
        self.initial = warehouse.__str__()
        self.goal_wh = warehouse.copy(boxes=warehouse.targets)
        self.goal = self.convert_state_to_mutiple_goal(warehouse)
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.taboo_warehouse = taboo_cells(self.warehouse)
        self.taboo_coords = list(sokoban.find_2D_iterator(self.taboo_warehouse,"X"))
        self.lines = self.taboo_warehouse.__str__().split(sep='\n')
        self.from_lines(self.lines)
        self.weighted = weighted
        self.box_weights = box_weights
        if weighted == True:
            self.initial = warehouse.__str__(),tuple(self.warehouse.boxes)
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """

        if self.weighted == True:
            self.warehouse.from_string(state[0])
            self.warehouse.boxes = list(state[1])
        if self.weighted == False:
            self.warehouse.from_string(state)
# checks to see if a worker can move to opposite side of a box, then checks that
# the box movement won't push into a wall/another box/taboo cell. If the movent 
# is legal, it is appended to the list LL    
        def action_macro(direction):
            # cycles through each box in the warehouse
            for i in range(0,len(self.warehouse.boxes)):
                # coordinates of the box currently being looked at
                box_loc = self.warehouse.boxes[i]
                if direction == 'Up':
                    if can_go_there_joseph(self.warehouse,(box_loc[0],box_loc[1]+1)) and (box_loc[0],box_loc[1]-1) not in self.warehouse.walls and (box_loc[0],box_loc[1]-1) not in self.warehouse.boxes and (box_loc[0],box_loc[1]-1) not in self.taboo_coords:
                        L.append('Up')
                        LL.append(box_loc)
                if direction == 'Down':   
                    if can_go_there_joseph(self.warehouse,(box_loc[0],box_loc[1]-1)) and (box_loc[0],box_loc[1]+1) not in self.warehouse.walls and (box_loc[0],box_loc[1]+1) not in self.warehouse.boxes and (box_loc[0],box_loc[1]+1) not in self.taboo_coords:
                        L.append('Down')
                        LL.append(box_loc)
                if direction == 'Left':  
                    if can_go_there_joseph(self.warehouse,(box_loc[0]+1,box_loc[1])) and (box_loc[0]-1,box_loc[1]) not in self.warehouse.walls and (box_loc[0]-1,box_loc[1]) not in self.warehouse.boxes and (box_loc[0]-1,box_loc[1]) not in self.taboo_coords:
                        L.append('Left')
                        LL.append(box_loc)
                if direction == 'Right':   
                    if can_go_there_joseph(self.warehouse,(box_loc[0]-1,box_loc[1])) and (box_loc[0]+1,box_loc[1]) not in self.warehouse.walls and (box_loc[0]+1,box_loc[1]) not in self.warehouse.boxes and (box_loc[0]+1,box_loc[1]) not in self.taboo_coords:
                        L.append('Right')
                        LL.append(box_loc)
# handles both weighted and elem solutions. Checks for legal movement directions
 # and appends them to the list L. If weighted is True, it also appends the cost 
 # of the current movement to the list L_weighted.
        def action(direction):

            if direction == 'Up':
                x1 = x                  
                x2 = x
                y1 = y-1
                y2 = y-2
            if direction == 'Down':
                x1 = x
                x2 = x
                y1 = y+1
                y2 = y+2
            if direction == 'Left':
                x1 = x-1
                x2 = x-2
                y1 = y
                y2 = y
            if direction == 'Right':
                x1 = x+1
                x2 = x+2
                y1 = y
                y2 = y
                        
            if ((x1, y1)) not in self.warehouse.walls:
                if ((x1, y1)) not in self.warehouse.boxes:
                    if self.weighted == True:
                        # if the worker is moving without a box being pushed it will set the cost to 1 for this action
                        L_weighted.append(1)
                    L.append(direction)
                if ((x1, y1)) in self.warehouse.boxes:
                    index = self.warehouse.boxes.index((x1,y1))
                    if self.allow_taboo_push:        
                        if ((x2, y2)) not in self.warehouse.boxes and ((x2, y2)) not in self.warehouse.walls:
                            if self.weighted == True:     
                                # sets the cost of the action taken equal to the wight of the moved box
                                L_weighted.append(self.box_weights[index])
                            L.append(direction)
                    if self.allow_taboo_push is False:
                        if ((x2, y2)) not in self.taboo_coords:
                            if ((x2, y2)) not in self.warehouse.boxes and ((x2, y2)) not in self.warehouse.walls:
                                if self.weighted == True:    
                                    # sets the cost of the action taken equal to the wight of the moved box
                                    L_weighted.append(self.box_weights[index])
                                L.append(direction)

        L = []  #   List of considered directions 
        LL = [] #   List of coordinates of the boxes being considered
        L_weighted = [] #   List of the considered box weights
        x, y = self.warehouse.worker    #   x,y refer to the x and y coordinates of the worker in the current warehouse
        if self.macro == False:
            action('Up')
            action('Down')
            action('Left')
            action('Right')
            if self.weighted == False:
                return L
            if self.weighted == True:
                #combines the directions moved and the cost of each move associated
                z = list(zip(L, L_weighted))
                return z
        if self.macro == True:
            action_macro('Up')
            action_macro('Down')
            action_macro('Left')
            action_macro('Right')
            # reverses the coordinates from (x,y) to (y,x)
            LL = Reverse(LL)
            # combines the coorditates and the directions moved into one list
            z = list(zip(LL, L))

            return (z)

# Deals with elem, macro and weighted solutions. Will return a string representation of the 
# warehouse after an action for elem and macro. For weighted, will return a string representation
# of the warehouse after an action and the coordinates of the boxes(this is because as the 
# warehouse is built from a string, the order of boxes changes depending where they are located)
# by keeping track of the box locations, the box weights will be applied to the appropriate box)
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if self.weighted == True:
            self.warehouse.from_string(state[0])
            self.warehouse.boxes = list(state[1])
        if self.weighted == False:
            self.warehouse.from_string(state)
        if self.macro == False:
            
            if self.weighted == False:
                x, y = self.warehouse.worker
                if action == 'Up':
                    if (x, y-1) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x, y-1))
                        self.warehouse.boxes[index] = (x, y-2)
                    self.warehouse.worker = (x, y-1)
                if action == 'Down':
                    if ((x, y+1)) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x, y+1))
                        self.warehouse.boxes[index] = ((x, y+2))
                    self.warehouse.worker = ((x, y+1))
                if action == 'Left':
                    if ((x-1, y)) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x-1, y))
                        self.warehouse.boxes[index] = ((x-2, y))
                    self.warehouse.worker = ((x-1, y))
                if action == 'Right':
                    if ((x+1, y)) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x+1, y))
                        self.warehouse.boxes[index] = ((x+2, y))
                    self.warehouse.worker = ((x+1, y))
                    
                return self.warehouse.__str__()
    
            if self.weighted == True:
                x, y = self.warehouse.worker
                if action[0] == 'Up':
                    if (x, y-1) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x, y-1))
                        self.warehouse.boxes[index] = (x, y-2)
                    self.warehouse.worker = (x, y-1)
                if action[0] == 'Down':
                    if ((x, y+1)) in self.warehouse.boxes:                        
                        index = self.warehouse.boxes.index((x, y+1))
                        self.warehouse.boxes[index] = ((x, y+2))
                    self.warehouse.worker = ((x, y+1))
                if action[0] == 'Left':
                    if ((x-1, y)) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x-1, y))
                        self.warehouse.boxes[index] = ((x-2, y))
                    self.warehouse.worker = ((x-1, y))
                if action[0] == 'Right':
                    if ((x+1, y)) in self.warehouse.boxes:
                        index = self.warehouse.boxes.index((x+1, y))
                        self.warehouse.boxes[index] = ((x+2, y))
                    self.warehouse.worker = ((x+1, y))
                    
                return self.warehouse.__str__(),tuple(self.warehouse.boxes)
        
        
        if self.macro == True:
            x,y = self.warehouse.worker  
            new_action = (action[0][1],action[0][0])

            if action[1] == 'Up':
                if new_action in self.warehouse.boxes:
                    x = self.warehouse.boxes.index(new_action)
                    self.warehouse.worker = self.warehouse.boxes[x]
                    self.warehouse.boxes[x] = (new_action[0],new_action[1]-1)
            if action[1] == 'Down':
                if new_action in self.warehouse.boxes:
                    x = self.warehouse.boxes.index(new_action)
                    self.warehouse.worker = self.warehouse.boxes[x]
                    self.warehouse.boxes[x] = (new_action[0],new_action[1]+1)
            if action[1] == 'Left':
                if new_action in self.warehouse.boxes:
                    x = self.warehouse.boxes.index(new_action)
                    self.warehouse.worker = self.warehouse.boxes[x]
                    self.warehouse.boxes[x] = (new_action[0]-1,new_action[1])
            if action[1] == 'Right':
                if new_action in self.warehouse.boxes:
                    x = self.warehouse.boxes.index(new_action)
                    self.warehouse.worker = self.warehouse.boxes[x]
                    self.warehouse.boxes[x] = (new_action[0]+1,new_action[1])
                    
            return self.warehouse.__str__()

# print_solution is used for visualizing how the solve functions are behaving 
    def print_solution(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        sequence = []
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        if goal_node is None:
            print('Impossible')
        else: 
            path = goal_node.path()
#         print the solution
            print("Path Cost is",goal_node.path_cost)
            print("Solution takes {0} steps from the initial state".format(len(path)-1))
            if self.weighted == True:
                print(path[0].state[0])
                print("to the goal state")
                print(path[-1].state[0])
            if self.weighted == False:
                print(path[0].state)
                print("to the goal state")
                print(path[-1].state)
            print("to the goal state")

        print("\nBelow is the sequence of moves\n")
        action_counter = 0
        for node in path:
            if node.action is not None:
                if self.weighted == True:
                    action_counter += node.action[1]
                    print('current cost of actions: ',action_counter)
                print(format(node.action))
                if self.weighted == True:
                    sequence.append(node.action[0])
                if self.weighted == False:
                    sequence.append(node.action)
#            # COMMENT OUT THE NEXT FOUR LINES TO MAKE IT EASIER TO SEE STEPS TAKEN TO GOAL
            # if self.weighted == True:
            #     print(node.state[0])
            # if self.weighted == False:
            #     print(node.state)
        print(sequence)
        
# used to return the appropriate answer for the elem problem. (returns the sequence of actions taken to the arrive at the goal)                
    def solution_elem(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        sequence = []
        if goal_node is None:
            return'Impossible'
        else: 
            path = goal_node.path()
        for node in path:
            if node.action is not None:
                sequence.append(node.action)
        return sequence
    
# used to return the appropriate answer for the weighted problem. (returns a combination of the sequence of actions taken to the goal and the coordinates that the box was moved from)
    def solution_macro(self, goal_node):
        sequence = []
        if goal_node is None:
            return'Impossible'
        else: 
            path = goal_node.path()
        for node in path:
            if node.action is not None:
                sequence.append(node.action)
        return sequence
# used to return the appropriate answer for the weighted problem. (returns the sequence of actions taken to the arrive at the goal)    
    def solution_weighted(self, goal_node):
        sequence = []
        if goal_node is None:
            return 'Impossible'
        else: 
            path = goal_node.path()
        for node in path:
            if node.action is not None:
                sequence.append(node.action[0])
        return sequence
    

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
# tests to see if the initial state is already in a goal state
        if self.weighted == False:
            if self.warehouse.targets == self.warehouse.boxes:
                return True
# tests to see if the current state is in the list of goal states
            if state in self.goal:
                return True
# tests to see if the current state is in the list of goal states
        if self.weighted == True:
            if state[0] in self.goal:
                return True

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
# adds the current cost to the cost of the new action. This depends on the weights of the boxes being moved        
        if self.weighted == True:
            return c + action[1]
# returns a cost value of 1 per step if weighted is False
        if self.weighted == False:
            return c + 1
        

    def h(self, n):
        '''
        Heurtistic - Uses Manhattan Distance
        To make the heuristic admissible it should be optimisitc. It should
        underestimate the cost from the current state to the goal state.

        Possible option: Use the sum of the manhattan distance of each box 
        to it's nearest target.

        returns a int value which is an estimate of the puzzles distance to
        the goal state.
        '''
        b = self.warehouse.boxes
        t = self.warehouse.targets
    
        h = []
        for i in range(0,len(t)):
            h.append(abs(b[i][0] - t[i][0]) + abs(b[i][1] - t[i][1]))

        heuristic = sum(h)
        return heuristic
# used to convert the initial state of the wearhosue into a list of all possible goal states.     
    def convert_state_to_mutiple_goal(self, warehouse):
        list_of_goal_possible_states = []
        list_of_goal_worker_coords = []
        list_of_states = []
        
        t = self.goal_wh.targets
        # makes a list of coordintates that surround each target
        for i in range(0,len(t)):
            list_of_goal_worker_coords.append((t[i][0],t[i][1]-1))
            list_of_goal_worker_coords.append((t[i][0],t[i][1]+1))
            list_of_goal_worker_coords.append((t[i][0]-1,t[i][1]))
            list_of_goal_worker_coords.append((t[i][0]+1,t[i][1]))
        for i in range(0,len(list_of_goal_worker_coords)):
            if list_of_goal_worker_coords[i] not in self.warehouse.walls and list_of_goal_worker_coords[i] not in self.warehouse.targets:
                list_of_goal_possible_states.append(list_of_goal_worker_coords[i]) 
# this makes sure there is no copies of the same goal state in the list
        def removeDuplicates(lst): 
            return list(set([i for i in lst]))  
        
        list_of_goal_possible_states = removeDuplicates(list_of_goal_possible_states)
        for i in range(0,len(list_of_goal_possible_states)):
            self.goal_wh.worker = list_of_goal_possible_states[i]
            list_of_states.append(self.goal_wh.__str__())
        return(list_of_states)
            
# this was taken from the sokoban.py and adapted so that the correct coordinates of the taboo cells 
    def from_lines(self,lines):
        first_row_brick, first_column_brick = None, None
        for row, line in enumerate(lines):
            brick_column = line.find('#')
            if brick_column>=0: 
                if  first_row_brick is None:
                    first_row_brick = row # found first row with a brick
                if first_column_brick is None:
                    first_column_brick = brick_column
                else:
                    first_column_brick = min(first_column_brick, brick_column)
        if first_row_brick is None:
            raise ValueError('Warehouse with no walls!')
        canonical_lines = [line[first_column_brick:] 
                           for line in lines[first_row_brick:] if line.find('#')>=0]
        self.extract_locations(canonical_lines)      
# this was taken from the sokoban.py and adapted so that the correct coordinates of the taboo cells    
    def extract_locations(self,lines):
        self.taboo_coords = list(sokoban.find_2D_iterator(lines, "X"))


opp_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# this class is used for the purpose of finding that a path is possible from the workers initial location to the workers desired location. It is only used for the macro solver
class PathFinderJoseph(search.Problem):

        def __init__(self, warehouse,dst):

            self.dst = dst# coordinates of the desired location for the worker to move to
            self.warehouse = warehouse
            self.initial = warehouse.__str__()# initial is a string representation of the warehouse(this will be the initial state that all other states will stem from)
            self.goal_wh = warehouse.copy(worker = self.dst)#   copies the current warehouse except now has the worker at the desired location(this is the warehouse goal layout)
            self.goal = self.goal_wh.__str__()# converts the goal warehouse into a string representation for the later use of checking if he current state is in the goal state or not
            
        def actions(self, state):
# converts the current state which is a string representation of the warehouse into a warehouse 
            self.warehouse.from_string(state)
# defines the x and y coordinates of the worker in the current warehouse
            x,y = self.warehouse.worker
# List of legal actions
            L = []
# appends the appropriate action to the list L            
            if (x,y-1) not in self.warehouse.walls and (x,y-1) not in self.warehouse.boxes:
                L.append('Up')
            if (x,y+1) not in self.warehouse.walls and (x,y+1) not in self.warehouse.boxes:
                L.append('Down')
            if (x-1,y) not in self.warehouse.walls and (x-1,y) not in self.warehouse.boxes:
                L.append('Left')    
            if (x+1,y) not in self.warehouse.walls and (x+1,y) not in self.warehouse.boxes:
                L.append('Right')
            return L
# (state) is a string representation of a warehouse and (action) is a string of either 'Up', 'Down', 'Left', 'Right'          
        def result(self, state, action):
# converts the current state which is a string representation of the warehouse into a warehouse 
            self.warehouse.from_string(state)
# defines the x and y coordinates of the worker in the current warehouse            
            x,y = self.warehouse.worker
# moves the worker to the new location depending on the input action            
            if action == 'Up':
                self.warehouse.worker = (x,y-1)
            if action == 'Down':
                self.warehouse.worker = (x,y+1)
            if action == 'Left':
                self.warehouse.worker = (x-1,y)
            if action == 'Right':
                self.warehouse.worker = (x+1,y)
            return self.warehouse.__str__()
# checks to see if the current state is the goal state and if it is, it will return True           
        def goal_test(self, state):
            if state == self.goal:
                return True
# Used to visualise how the solver found the path and what the path chosen was 
        def print_solution(self, goal_node):
            """
                Shows solution represented by a specific goal node.
                For example, goal node could be obtained by calling 
                    goal_node = breadth_first_tree_search(problem)
            """
            sequence = []
            # path is list of nodes from initial state (root of the tree)
            # to the goal_node
            if goal_node is None:
                # print('Impossible')
                return False
            else: 
                path = goal_node.path()
            # print the solution
            #     print("Solution takes {0} steps from the initial state".format(len(path)-1))
            #     print(path[0].state)
            #     print("to the goal state")
            #     print(path[-1].state)
            # print("\nBelow is the sequence of moves\n")
            for node in path:
                if node.action is not None:
                    # print(format(node.action))
                    sequence.append(node.action)
# COMMENT OUT THIS LINE TO MAKE IT EASIER TO SEE STEPS TAKEN TO GOAL
            #     print(node.state)
            # print(sequence)
            return True
            
        def h(self, n):
            # worker coordinates
            x,y = self.warehouse.worker
            #desired location for the worker to move to
            x2,y2 = self.dst
            #a heuristic which finds the Manhatten distance from the worker position to the desired position
            h = abs(x-x2)+abs(y-y2)
            return h
# This sets the cost of one movement of the worker to 1.    
        def path_cost(self, c, state1, action, state2):
            """Return the cost of a solution path that arrives at state2 from
            state1 via action, assuming cost c to get up to state1. If the problem
            is such that the path doesn't matter, this function will only look at
            state2.  If the path does matter, it will consider c and maybe state1
            and action. The default method costs 1 for every step in the path."""
            return c + 1
                
            


class PathFinder(search.Problem):
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse

    def value(self, state):
        # cost = 1 for a single movement
        return 1

    def result(self, state, action):
        # result = old state with action applied
        new_state = state[0] + action[0], state[1] + action[1]
        return new_state

    def actions(self, state):
        for opp in opp_states:
            new_state = state[0] + opp[0], state[1] + opp[1]
            # check loc != wall or box
            if new_state not in self.warehouse.boxes and new_state not in self.warehouse.walls:
                yield opp


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
                    print(
                        "Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
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
                    print(
                        "Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
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
                    print(
                        "Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
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
                    print(
                        "Failed because player can't push 2 boxes at once, or tried to push a box into a wall.")
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
#   creates a problem class that initializes the class to solve for an elementary problem
    SBE = SokobanPuzzle(warehouse,allow_taboo_push=False)
#   uses the astar graph search to find the solution to the problem
    solution = search.astar_graph_search(SBE)
#   runs the solution_elem fuction which returns the list of actions taken to solve the specified warehouse problem
#   If no path is found, it will return the string 'Impossible'
#   If the puzzle is already in a goal state, it will return []
    return SBE.solution_elem(solution)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#   Uses an astar graph serach to determine if there is a path from the worker 
#   to the specified destination (Only used in the macro solver)
#   warehouse must be a warehouse object
#   dst must be a valid coordinate within the warehouse
def can_go_there_joseph(warehouse, dst):
    cgt = PathFinderJoseph(warehouse,(dst))
    solve = search.astar_graph_search(cgt)
    CGT = cgt.print_solution(solve)
    return CGT


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    @param warehouse: a valid Warehouse object
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    def heuristic(n):
        state = n.state
        print(state)
        return math.sqrt(((state[1] - dst[1]) ** 2) + ((state[0] - dst[0]) ** 2))

    dst = (dst[1], dst[0])

    node = astar_graph_search(PathFinder(
        warehouse.worker, warehouse, dst), heuristic)

    return node is not None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Reverses the coordinates from (x,y) to (y,x), used only in the macro solver
def Reverse(tuples):
    new_list = []
    new_tup = ()
    for i, k in tuples:
        new_tup = (k, i)
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
    def h(n):
        '''
        Heuristic - Uses Manhattan Distance
        To make the heuristic admissible it should be optimisitc. It should
        underestimate the cost from the current state to the goal state.

        Possible option: Use the sum of the manhattan distance of each box 
        to it's nearest target.

        returns a int value which is an estimate of the puzzles distance to
        the goal state.
        '''
        warehouse.extract_locations(n.state.split('\n'))
        worker, targets, boxes = warehouse.worker, warehouse.targets, warehouse.boxes
        heuristic = 0
        for box in boxes:
            for target in targets:
                heuristic += abs(box[0]-target[0]) + abs(box[1]-target[1])
        heuristic = heuristic // len(boxes)
        return heuristic

    M = search.astar_graph_search(SokobanPuzzle(warehouse, allow_taboo_push=False, macro = True), h)

    if M is None:
        return 'Impossible'

    path = M.path()
    actions = [e.action for e in path]
    del actions[0]

    return actions

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
#   creates a problem class that initializes the class to solve for weighted problem
    SBW = SokobanPuzzle(warehouse,allow_taboo_push=False, macro = False, weighted = True, box_weights = push_costs)
#   uses the astar graph search to find the solution to the problem
    solution = search.astar_graph_search(SBW)
#   runs the solution_weighted fuction which returns the list of actions taken to solve the specified warehouse problem
#   If no path is found, it will return the string 'Impossible'
    return SBW.solution_weighted(solution)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':

    '''
    #
    # testing the SokobanPuzzle() class
    #
    '''

    # test_string = "##############\n# ##    #    #\n#.#     #    #\n#       #    #\n#$      #    #\n#@$  .  #    #\n##############"
#    test_string = "#############\n#    .      #\n#           #\n#           #\n#      $    #\n#    #.#    #\n#    #$#    #\n#    #@#    #\n#############"
#    test_string = "##########\n#   .... #\n#        #\n#$       #\n#$       #\n#@$$     #\n##########"
    wh = sokoban.Warehouse()
    # wh.from_string(test_string)
    wh.load_warehouse("./warehouses/warehouse_81.txt")

# UNCOMMENT THE NEXT THREE LINES TO RUN SOKOBAN WEIGHTED (MAKE SURE THERE IS THE SAME AMOUNT OF BOX WEIGHTS AS THERE ARE BOXES IN THE CHOSEN WAREHOUSE)
    # SBW = SokobanPuzzle(wh,allow_taboo_push=False, macro = False, weighted = True, box_weights = [3,9,2])
    # sol_ts = search.astar_graph_search(SBW)
    # SBW.print_solution(sol_ts) # go to print_solution to edit what the result will print
    
# UNCOMMENT THE NEXT THREE LINES TO RUN SOKOBAN ELEM 
    # SBE = SokobanPuzzle(wh,allow_taboo_push=False)
    # sol_ts = search.astar_graph_search(SBE)
    # SBE.print_solution(sol_ts) # go to print_solution to edit what the result will print

# UNCOMMENT THE NEXT THREE LINES TO RUN SOKOBAN MACRO
    SB = SokobanPuzzle(wh,allow_taboo_push=False,macro = True)
    sol_ts = search.astar_graph_search(SB)
    SB.print_solution(sol_ts) # go to print_solution to edit what the result will print

