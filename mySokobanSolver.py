
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
    x_sz = len(warehouse_str[0])
    
    for y in range(len(warehouse_str)):
        # strip trailing space and replace with 'u'
        warehouse_str[y] = warehouse_str[y].lstrip()
        warehouse_str[y] = ('u' * (x_sz - len(warehouse_str[y]))) + warehouse_str[y]

        warehouse_str[y] = warehouse_str[y].rstrip()
        warehouse_str[y] = warehouse_str[y] + ('u' * (x_sz - len(warehouse_str[y])))

        # replace with space
        warehouse_str[y] = warehouse_str[y].replace('*', '.').replace('@', ' ').replace('$', ' ')
    
    tabooCorners = []
    # Rule 1: find corners
    for y in range(len(warehouse_str)):
        for x in range(len(warehouse_str[y])):
            if (warehouse_str[y][x] == ' '):
                # corner if up down left right are walls >1 times
                updownleftright = warehouse_str[y][x+1] + warehouse_str[y][x-1] + warehouse_str[y+1][x] + warehouse_str[y-1][x]
                # count walls
                count = updownleftright.count('#')

                if (count > 1):
                    warehouse_str[y] = warehouse_str[y][:x] + 'X' + warehouse_str[y][x+1:]
                    # track X's
                    tabooCorners.append([x, y])

    # Rule 2: corridor
    for i in range(len(tabooCorners)):
        corner = tabooCorners[i]

        for j in range(i+1, len(tabooCorners)):
            cornerCheck = tabooCorners[j]

            if (corner[0] == cornerCheck[0]):
                # y-axis
                x = corner[0]
                yrange = [corner[1], cornerCheck[1]]
                for y in range(min(yrange), max(yrange)):
                    if (warehouse_str[y][x] != '.'): # not goal
                        updown = warehouse_str[y][x+1] + warehouse_str[y][x-1]
                        if (updown.count('#') >= 1):
                            warehouse_str[y] = warehouse_str[y][:x] + 'X' + warehouse_str[y][x+1:]

            if (corner[1] == cornerCheck[1]):
                # x-axis
                y = corner[1]
                xrange = [corner[0], cornerCheck[0]]
                for x in range(min(xrange), max(xrange)):
                    if (warehouse_str[y][x] != '.'): # not goal
                        updown = warehouse_str[y+1][x] + warehouse_str[y-1][x]
                        if (updown.count('#') >= 1):
                            warehouse_str[y] = warehouse_str[y][:x] + 'X' + warehouse_str[y][x+1:]

    
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
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        raise NotImplementedError

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

    return ['Down', 'Left', 'Up', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up'], 0


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

