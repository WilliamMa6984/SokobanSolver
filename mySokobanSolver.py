
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
    return [ (10491694, 'William', 'Ma'), (10474609, 'David', 'Truong') ]

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

    # Preprocessing
    for y in range(len(warehouse_str)):
        # pad right until reach x_sz
        if (len(warehouse_str[y]) < x_sz):
            warehouse_str[y] = warehouse_str[y] + ' ' * (x_sz - len(warehouse_str[y]))

        # replace with space
        warehouse_str[y] = warehouse_str[y].replace('*', '.').replace('!', '.').replace('@', ' ').replace('$', ' ')

    warehouse_str = mark_inaccessible(warehouse_str, warehouse)
    
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
                    if (warehouse_str[y][x] == '.' or warehouse_str[y][x] == '#'): # goal or wall in axis
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
                    if (warehouse_str[y][x] == '.' or warehouse_str[y][x] == '#'): # goal in axis
                        axis_available = False
                        break
                    updown = warehouse_str[y+1][x] + warehouse_str[y-1][x]
                    if (updown.count('#') == 0):
                        axis_available = False
                        break # no walls, break

                
                if (axis_available):
                    # horizontally
                    for x_ in range(min(xrange), max(xrange)):
                        warehouse_str[y] = warehouse_str[y][:x_] + 'X' + warehouse_str[y][x_+1:]

    # replace unplayable areas 'u' with space again
    out_str = ''
    for y in range(len(warehouse_str)):
        out_str += warehouse_str[y].replace('u', ' ').replace('.', ' ')
        out_str += '\n'

    return out_str[0:len(out_str)-1]

def mark_inaccessible(warehouse_str, warehouse):
    """
    Marks cells that are never accesible by the worker as 'u'.

    @param
        warehouse_str: string representation of the warehouse that is to be edited
        warehouses: the warehouse object
    @return Returns the edited warehouse_str
    """
    for y, string in enumerate(warehouse_str):
        x_arr = [i for i, letter in enumerate(list(string)) if letter == ' ']
        
        for x in x_arr:
            # Check if a path exists from the player to the current space (ignoring boxes)
            if path_to_location(warehouse, (x, y), ignoreBox=True) == None:
                warehouse_str[y] = warehouse_str[y][:x] + 'u' + warehouse_str[y][x+1:]

    return warehouse_str

def any_box_in_taboo(map_str, tabooMap_str):
    """
    Checks whether any box in the input map also occupies a taboo cell.

    @param
        map: The input map that keeps track of the box
        tabooMap: The map containing the taboo cell information
    @return
        Returns true if a box is in a taboo cell.
    """
    
    map_arr = map_str.split('\n')
    tabooMap_arr = tabooMap_str.split('\n')

    assert len(map_arr) == len(tabooMap_arr)

    for i, taboo_row in enumerate(tabooMap_arr):
        for j, taboo_letter in enumerate(list(taboo_row)):
            if taboo_letter == 'X' and map_arr[i][j] == '$':
                return True

    return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class HashedWarehouseState:
    """
    The Warehouse state as a hashable object
    @param: worker, boxes, targets
    """

    def __init__(self, warehouse):
        self.worker = warehouse.worker
        self.boxes = warehouse.boxes
        self.targets = warehouse.targets
        self.string = str(warehouse)

    def __hash__(self):
        """
        Object hash - same state must be equal
        """
        return hash(self.string)

    def __eq__(self, other):
        """
        Equality comparison for the state
        """
        assert isinstance(other, HashedWarehouseState)

        return (self.worker == other.worker) and (set(self.boxes) == set(other.boxes))
    
    def __lt__(self, other):
        """
        Check if this state is less optimal than the other state.
        """
        assert isinstance(other, HashedWarehouseState)
        
        return len(set(self.boxes) - set(self.targets)) < len(set(other.boxes) - set(other.targets))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    def __init__(self, warehouse):
        # Statics
        self.warehouse = warehouse

        self.taboo_map = taboo_cells(warehouse) # string rep
        
        # State
        self.initial = HashedWarehouseState(warehouse)
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        Must be a list of dictionary with {'direction': 'Up', 'boxIndex': 1},
        with each entry moving a single box once
        """
        
        legal_actions = []
        directions = ['Up', 'Down', 'Left', 'Right']
        warehouse = self.warehouse.copy(worker = state.worker, boxes = state.boxes.copy())

        # Worker movement
        for direction in directions:
            legalMap = check_elem_action_seq(warehouse, [direction])
            if legalMap == 'Impossible':
                continue
            isTaboo = any_box_in_taboo(legalMap, self.taboo_map)
            if isTaboo == False:
                nextCoord = movement(direction, warehouse.worker)
                if nextCoord in warehouse.boxes:
                    boxId = warehouse.boxes.index(nextCoord)
                else:
                    boxId = None
                legal_actions.append({'direction': direction, 'boxIndex': boxId})
                
        return legal_actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        boxID = action['boxIndex']
        boxes_update = state.boxes.copy()
        
        if (boxID is not None):
            boxes_update[boxID] = movement(action['direction'], state.boxes[boxID])
        
        worker_update = movement(action['direction'], state.worker)

        warehouse = self.warehouse.copy(worker = worker_update, boxes = boxes_update)

        return HashedWarehouseState(warehouse)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""

        # count number of boxes not in target square using string representation
        return set(state.boxes) == set(state.targets)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        # cost = length of all actions except last, + box weight of the box
        boxId = action['boxIndex']
        w = 0
        if boxId is not None:
            w = self.warehouse.weights[boxId]
        return c + 1 + w
        
    def h(self, node):
        """Heuristic: the distance for each box from any nearest target"""
        return h_overall(self.warehouse.targets, node.state.boxes, self.warehouse.weights)
        

def h_overall(targets, boxes, weights):
    """
    Calculate the overall heuristic of the current warehouse: based on the
    distance between each box, and between its nearest target

    @param
        warehouse: a valid warehouse object
    """
    
    h = 0
    for i, box in enumerate(boxes):
        h = h + get_closest_target(targets, box, weights[i])
        if i > 0:
            h = h + manhattan(box, boxes[i-1])

    return h

def get_closest_target(targets, boxCoord, boxWeight):
    """
    Get the closest target for the input box and return the path cost
    to move the box to it.
    
    @param
        targets: a list of target coordinates to find the closest target
        boxCoord: the coordinate of the box
        boxWeight: the weight of the box
    @return Returns the distance (including weight)
    """

    closestTarget = manhattan(boxCoord, targets[0]) * (boxWeight)
    
    for target in targets:
        targetDistance = manhattan(boxCoord, target) * (boxWeight)
        if closestTarget > targetDistance:
            closestTarget = targetDistance
    
    return closestTarget

def manhattan(a, b):
    """Get manhattan distance between two coordinates."""
    return abs((a[0] - b[0]) + abs(a[1] - b[1]))

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
    
    warehouse_out = copy_warehouse_fully(warehouse) # copy the warehouse so that changes do not spill over to the actual warehouse
    
    for i in action_seq:
        warehouse_out.worker = movement(i, warehouse_out.worker)
        if warehouse_out.worker in warehouse_out.boxes:
            boxToMoveInds = [i for i, x in enumerate(warehouse_out.boxes) if warehouse_out.worker == x]
            for boxInd in boxToMoveInds:
                newBoxCoord = movement(i, warehouse_out.boxes[boxInd])
                if newBoxCoord in warehouse_out.boxes or newBoxCoord in warehouse_out.walls:
                    return 'Impossible'
                warehouse_out.boxes[boxInd] = newBoxCoord
        elif warehouse_out.worker in warehouse_out.walls:
            return 'Impossible'
    
    return str(warehouse_out)

def copy_warehouse_fully(warehouse):
    """
    Creates an unlinked copy of the warehouse, so changes to a warehouse
    inside a function does not spill over to the parent function.
    """
    warehouse_out = warehouse.copy()
    warehouse_out.boxes = warehouse.boxes.copy()
    return warehouse_out

def movement(direction, coord):
    """
    Gives the resulting coordinate after applying the 1-space move

    @param
        direction: direction of the movement
        coord: the old coordinated

    @return the new coordinate
    """
    if direction == "Up":
        return tuple((coord[0], coord[1] - 1))
    if direction == "Down":
        return tuple((coord[0], coord[1] + 1))
    if direction == "Left":
        return tuple((coord[0] - 1, coord[1]))
    if direction == "Right":
        return tuple((coord[0] + 1, coord[1]))


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

    sol_node = search.astar_graph_search(SokobanPuzzle(warehouse))

    if (sol_node == None):
        return 'Impossible', None

    route = []
    cost = 0
    for action in sol_node.solution():
        route.append(action['direction'])

        boxId = action['boxIndex']
        w = 0
        if (boxId is not None):
            w = warehouse.weights[boxId]
        cost = cost + 1 + w

    return route, cost


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def path_to_location(warehouse, goal, ignoreBox):
    """
    Gets the path from the current worker location to the goal location
    @param
        warehouse: Current warehouse configuration
        goal: Goal location (single (x, y) tuple)
        ignoreBox: Whether to ignore boxes or go around the box when path finding
    @return
        The solution path - a list of directions, None if no solution is found. Path cost is equivalent to the length of the solution.
    """

    out = search.astar_graph_search(WorkerPathing(warehouse, goal, ignoreBox))

    if out == None:
        return None
    else:
        return out.solution()

class WorkerPathing(search.Problem):
    '''
    Worker Pathing search problem
    '''
    
    def __init__(self, warehouse, goal, ignoreBox):
        if (ignoreBox):
            self.obstacles = warehouse.walls
        else:
            self.obstacles = warehouse.walls + warehouse.boxes
        self.goal = goal
        self.initial = warehouse.worker
    
    def actions(self, state):
        """
        Return the list of worker actions that can be executed in the given state.
        """

        legal_actions = []
        
        upDownLeftRight = ['Up', 'Down', 'Left', 'Right']
        
        for i, direction in enumerate(upDownLeftRight):
            next = movement(direction, state)
            if next not in self.obstacles:
                legal_actions.append(upDownLeftRight[i])

        return legal_actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """

        return movement(action, state)
    
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
    
    def h(self, node):
        """Heuristic"""
        return abs(self.goal[0] - node.state[0]) + abs(self.goal[1] - node.state[1])