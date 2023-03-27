"""eight_puzzle: Implementation of eight puzzle problem."""
__author__ = "Mubasir Halidu"

import copy

class Problem:
    """ This class represents a generic Problem to be solved by search."""

    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state

    def __str__(self):
        return (type(self).__name__ + ": Init state=" + str(self.init_state) +
                ", goal state=" + str(self.goal_state))

    def goal_test(self, state):
        return False

    def actions(self, state):
        return None, None

EMPTY = 0 # Empty space in grid is represented with a zero (0)
EMPTY_GRID = [[EMPTY,EMPTY,EMPTY],
              [EMPTY,EMPTY,EMPTY],
              [EMPTY,EMPTY,EMPTY]]

def set_init_state(prompt, grid):
    """ This function is used to set initial state of the problem by user """

    print(prompt)
    for row in range(3):
        vals = input()
        str_vals = vals.split()
        for col in range(len(str_vals)):
            grid[row][col] = int(str_vals[col])

def swap_tile(state,row, col, action):
    """ This function swaps the zero tile with adjacent tiles"""

    res_state = copy.deepcopy(state)
    empty_tile = res_state[row][col]

    # Swaps zero tile with down tile
    if action == 'D':
        temp_var = res_state[row+1][col]
        res_state[row][col] = temp_var
        res_state[row+1][col] = empty_tile

    # Swaps zero tile with up tile 
    if action == 'U':
        temp_var = res_state[row-1][col]
        res_state[row][col] = temp_var
        res_state[row-1][col] = empty_tile
    
    # Swaps zero tile with left tile
    if action == 'L':
        temp_var = res_state[row][col-1]
        res_state[row][col] = temp_var
        res_state[row][col-1] = empty_tile
    
    # Swaps zero tile with right tile
    if action == 'R':
        temp_var = res_state[row][col+1]
        res_state[row][col] = temp_var
        res_state[row][col+1] = empty_tile
        
    return res_state


class EightPuzzle(Problem):
    """ This class represents the Eight puzzle problem where a state is a 2D grid.
    """

    def __init__(self, init_state, goal_state):
        super().__init__(init_state, goal_state)

    def goal_test(self, state):
        return (state == self.goal_state)

    def actions(self, state):
        actions = []
        succ_states = []
        for row in range(len(state)):
            for col in range(len(state)):
                if state[row][col] == 0: # finds the row and column that correspond to the empty tile
                    
                    # U action results in (row-1, col)
                    if (row-1 >= 0 and state[row-1][col] != 0):
                        actions.append("U")
                        succ_state = swap_tile(state, row, col, "U")
                        succ_states.append(succ_state) 

                    # R action results in (row, col+1)
                    if (col+1 < len(state) and state[row][col+1] != 0):
                        actions.append("R")
                        succ_state = swap_tile(state, row, col, "R")
                        succ_states.append(succ_state)

                    # D action results in (row+1, col)
                    if (row+1 < len(state) and state[row+1][col] != 0):
                        actions.append("D")
                        succ_state = swap_tile(state, row, col, "D")
                        succ_states.append(succ_state)

                    # L action results in (row, col-1)
                    if (col-1 >= 0 and state[row][col-1] != 0):
                        actions.append("L")
                        succ_state = swap_tile(state, row, col, "L")
                        succ_states.append(succ_state)

        return actions, succ_states

    def print_prob(self):
        """ Prints the problem as grid"""

        print("__EightPuzzle__")
        print("init_state =", self.init_state)
        print("goal_state =", self.goal_state)

        print("Initial state")
        for i in range(len(self.init_state)):
            print("|", end="")
            for j in range(len(self.init_state[i])):
                print(str(self.init_state[i][j])+"|", end='')
            print()

        print()

        print("Goal state")
        for i in range(len(self.goal_state)):
            print("|", end="")
            for j in range(len(self.goal_state[i])):
                print(str(self.goal_state[i][j])+"|", end='')
            print()


def check_solvable(init_state):
    """ Checks if the initials tate for the problem entered can be solved.
        Problem can be solved if the number of inversions is even. i.e. the number
        of tiles in reverse order compared to the goal state"""
        
    array_version = []
    inversions_count = 0
    empty_tile = 0

    for i in init_state:
        for j in i:
            array_version.append(j)

    for i in range(len(array_version)):
        for j in range(i + 1, len(array_version)):
            if (array_version[j] != empty_tile and array_version[i] != empty_tile 
                and array_version[i] > array_version[j]):
                inversions_count += 1
    
    return inversions_count % 2 == 0



class Node:
    """ This class represents a node in the search tree"""
    
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):
        mystr = "Node with state=" + str(self.state)
        if (self.parent != None):
            mystr += (", parent=" + str(self.parent.state) +
                      ", action=" + str(self.action) +
                      ", path_cost=" + str(self.path_cost))
        return mystr

    # The purpose of this method is to enable two nodes  on the
    # frontier to be considered equal to each other if they represent
    # the same state (regardless of if they have different parent nodes)
    def __eq__(self, other):
        return (isinstance(other, Node) and
                self.state == other.state)

    def solution_path(self):
        # This method returns paths of the states as a list
        # and the action path as well as the overall path cost
        current_state = self.parent
        state_path = [self.state]
        action_path = [self.action]
        while current_state != None:
            state_path.insert(0, current_state.state)
            if (current_state.action != None):
                action_path.insert(0, current_state.action)
            current_state = current_state.parent

        return state_path, action_path, self.path_cost

def dfs(problem):
    print("About to do DFS on problem: ", problem)
    node = Node(problem.init_state)
    number_of_nodes_processed = 0
    len_frontier = 0

    # Checking if the initial state is same as the goal state
    if problem.goal_test(node.state):
        print("The Number of Nodes Processed is: ",
              number_of_nodes_processed)
        print("The overall length of the frontier is: ",
              len_frontier)
        return node.solution_path()

    frontier = [node]
    explored = set()
    len_frontier = 1

    while (len(frontier) > 0):
        node = frontier.pop(0) # Popping the last item from the stack to explore
        number_of_nodes_processed += 1
        explored.add(str(node.state))
        print("Popped: ", node)
        actions, successors = problem.actions(node.state)
        print("Generated successor states: ", successors)
        for i in range(len(actions)):
            child = Node(successors[i], node, actions[i],
                         node.path_cost+1)
            if (str(child.state) not in explored and
                    child not in frontier):
                if (problem.goal_test(child.state)):
                    print("Found a solution! ", child)
                    print("The Number of Nodes Processed is: ",
                          number_of_nodes_processed)
                    print("The overall length of the frontier is: ",
                          len_frontier)
                    return child.solution_path()
                frontier.append(child)
                len_frontier += 1
            else:
                continue
    return None  # failure - means no solution found


if __name__ == "__main__":
    grid = copy.deepcopy(EMPTY_GRID)
    set_init_state("Enter initial state for the problem:",grid)
    print("Thanks. You entered",grid)
    initial_state = grid
    goal = [
        [1,2,3],  
        [4,5,6],  
        [7,8,0]]

    if check_solvable(initial_state):
        print("Problem entered is solvable \nFinding solution to problem")
        myProb_1 = EightPuzzle(initial_state,goal)
        myProb_1.print_prob()
        print()
        solution = dfs(myProb_1)
        print("DFS returned", solution)
    else:
        print("SORRY!! Problem entered is not solvable")
        
