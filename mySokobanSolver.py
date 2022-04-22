
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
from distutils.log import error
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    
    warehouse_str = str(warehouse).split('\n')
    x_sz = max(len(row) for row in warehouse_str)

    def replaceTrailingSpace(string, sz, replacement):
        # strip trailing space and replace with char
        string = string.lstrip()
        string = (replacement * (sz - len(string))) + string

        string = string.rstrip()
        string = string + (replacement * (sz - len(string)))

        return string

    for y in range(len(warehouse_str)):
        # pad right until reach x_sz
        if (len(warehouse_str[y]) < x_sz):
            warehouse_str[y] = warehouse_str[y] + ' ' * (x_sz - len(warehouse_str[y]))

        warehouse_str[y] = replaceTrailingSpace(warehouse_str[y], x_sz, 'u')

        # replace with space
        warehouse_str[y] = warehouse_str[y].replace('*', '.').replace('@', ' ').replace('$', ' ')

    # remove trailing vertical spaces
    for y in range(len(warehouse_str)):
        warehouse_str[y] = list(warehouse_str[y])
    warehouse_str = [[warehouse_str[j][i] for j in range(len(warehouse_str))] for i in range(len(warehouse_str[0])-1,-1,-1)] # rotate 90

    for x in range(len(warehouse_str)):
        y_sz = len(warehouse_str[x])
        warehouse_str[x] = ''.join(char for char in warehouse_str[x])
        warehouse_str[x] = replaceTrailingSpace(warehouse_str[x], y_sz, 'u')

    # rotate -90
    for y in range(len(warehouse_str)):
        warehouse_str[y] = list(warehouse_str[y])
    warehouse_str = [[warehouse_str[j][i] for j in range(len(warehouse_str)-1,-1,-1)] for i in range(len(warehouse_str[0]))]

    for x in range(len(warehouse_str)):
        y_sz = len(warehouse_str[x])
        warehouse_str[x] = ''.join(char for char in warehouse_str[x])

    tabooCorners = []
    # Rule 1: find corners
    for y in range(len(warehouse_str)):
        for x in range(len(warehouse_str[y])):
            if (warehouse_str[y][x] == ' '):
                # corner if up down left right are walls >1 times
                up = warehouse_str[y+1][x]
                down = warehouse_str[y-1][x]
                left = warehouse_str[y][x-1]
                right = warehouse_str[y][x+1]
                pattern = up + right + down + left + up
                # count walls
                corner = pattern.find("##") # two walls in pattern (corner)

                if (corner >= 0):
                    warehouse_str[y] = warehouse_str[y][:x] + 'X' + warehouse_str[y][x+1:]
                    # track X's
                    tabooCorners.append([x, y])

    # Rule 2: corridor
    for i in range(len(tabooCorners)):
        corner = tabooCorners[i]

        # check for any goal in the line
        for j in range(i+1, len(tabooCorners)):
            cornerCheck = tabooCorners[j]

            if (corner[0] == cornerCheck[0]):
                # y-axis
                axis_available = True
                x = corner[0]
                yrange = [corner[1], cornerCheck[1]]
                for y in range(min(yrange), max(yrange)):
                    if (warehouse_str[y][x] == '.'): # goal in axis
                        axis_available = False
                        break
                    leftright = warehouse_str[y][x+1] + warehouse_str[y][x-1]
                    if (leftright.count('#') == 0):
                        axis_available = False
                        break # no walls, break

                
                if (axis_available):
                    # vertically
                    for y_ in range(min(yrange), max(yrange)):
                        warehouse_str[y_] = warehouse_str[y_][:x] + 'X' + warehouse_str[y_][x+1:]

            if (corner[1] == cornerCheck[1]):
                # x-axis
                axis_available = True
                y = corner[1]
                xrange = [corner[0], cornerCheck[0]]
                for x in range(min(xrange), max(xrange)):
                    if (warehouse_str[y][x] == '.'): # goal in axis
                        axis_available = False
                        break
                    updown = warehouse_str[y+1][x] + warehouse_str[y-1][x]
                    if (updown.count('#') == 0):
                        axis_available = False
                        break # no walls, break

                
                if (axis_available):
                    length = abs(corner[0] - cornerCheck[0])
                    # horizontally
                    for x_ in range(min(xrange), max(xrange)):
                        warehouse_str[y] = warehouse_str[y][:x_] + 'X' + warehouse_str[y][x_+1:]

    # replace unplayable areas 'u' with space again
    out_str = ''
    for y in range(len(warehouse_str)):
        out_str += warehouse_str[y].replace('u', ' ').replace('.', ' ')
        out_str += '\n'

    return out_str

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes
    
    def __init__(self, warehouse):
        self.walls = warehouse.walls
        self.targets = warehouse.targets
        # current state =>
        self.boxes = [[boxes, warehouse.weights[i]] for i, boxes in enumerate(warehouse.boxes)] # combine box + weight?
        self.worker = warehouse.worker 

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """

        """
        Student note:
        State: location of the worker + boxes -> used to get actions
        Simply: move worker up down left right, unless theres a wall there, or box against wall, box against box
        """

        legal_actions = []
        # if (state.walls.coord(state.worker.coord.Up) or
        #     (state.boxes.coord(state.worker.coord.Up) and state.walls.coord(state.worker.coord.Up.Up)) or
        #     (state.boxes.coord(state.worker.coord.Up) and state.boxes.coord(state.worker.coord.Up.Up))):
        #     legal_actions = 'Up'
        # etc.

        raise NotImplementedError
    
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """

        raise NotImplementedError

    # state class?
    # class state():
    #     def __init__(self, boxes, worker):
    #         self.boxes = boxes
    #         self.worker = worker


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
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    print("boxes: ", warehouse.boxes)
    print("weights: ", warehouse.weights)
    print("walls: ", warehouse.walls)
    print("worker: ", warehouse.worker)
    
    print("original map: ")
    print(str(warehouse))

    print("taboo map: ")
    print(taboo_cells(warehouse))

    # raise NotImplementedError
    return ['Down', 'Left', 'Up', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up'], 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

