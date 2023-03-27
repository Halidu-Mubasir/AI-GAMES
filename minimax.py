__author__ = "Mubasir Halidu"

import sys
import copy
INF = sys.maxsize

class Game:
    """ This class represents a genereic game of game theory"""

    def __init__(self, init_state):
        self.init_state = init_state

    def __str__(self):
        return "Init_state="+str(self.init_state)

    # placeholder, to be overridden in derived class
    def terminal_test(self, state):
        return True 

    # placeholder, to be overriden in derived class
    def utility(self, state):
        return 0 

    # placeholder, to be overriden in derived class
    def actions(self, state):
        moves = []
        return moves

    # placeholder, to be overriden in derived class
    def result(self, state, action):
        return state

BLANK = '_' # Empty space in grid is represented with an underscore (_)
X = 'X'
O = 'O'
EMPTY_GRID = [[BLANK,BLANK,BLANK],
              [BLANK,BLANK,BLANK],
              [BLANK,BLANK,BLANK]]

class TicTacToe(Game):
    def __init__(self):
        super().__init__(copy.deepcopy(EMPTY_GRID))
        self.player = "X" # Represents computer player

    def terminal_test(self, state):
        # if there is no empty space then it's a terminal state
        if not (BLANK in state[0] or
                BLANK in state[1] or
                BLANK in state[2]):
            return True

        # otherwise, if there's a winner, it's a terminal state
        winner = self.winner(state)
        return winner == X or winner == O

    def winner(self, state):
        # check each row for a winning configuration
        for row in [0, 1, 2]:
            if (state[row][0] != BLANK and
                state[row][0] == state[row][1] and
                state[row][0] == state[row][2]):
                return state[row][0]

        # check each column for a winner configuration
        for col in [0, 1, 2]:
            if (state[0][col] != BLANK and
                state[0][col] == state[1][col] and
                state[0][col] == state[2][col]):
                return state[0][col]

        # check the top left to bottom right diagonal
        if (state[0][0] != BLANK and
            state[0][0] == state[1][1] and
            state[0][0] == state[2][2]):
            return state[0][0]
        
        # check the bottom left to top right diagonal
        if (state[2][0] != BLANK and
            state[2][0] == state[1][1] and
            state[2][0] == state[0][2]):
            return state[2][0]

        return None

    def utility(self, state):
        winner = self.winner(state)
        if winner == X:
            return 1
        elif winner == O:
            return -1
        else:
            return 0
        
    def actions(self, state):
        moves = []
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if state[row][col] == BLANK:
                    moves.append((row,col))
        return moves

    def result(self, state, action, player):
        res_state = copy.deepcopy(state)
        res_state[action[0]][action[1]] = player
        return res_state

n_levels = 0
n_states = 0
n_terminal_states = 0
states = dict()
terminal_states = set()

def minimax_decision(game, state):
    global n_levels, n_states, n_terminal_states, states, terminal_states
    n_levels = n_states = n_terminal_states = 0
    states = dict()
    terminal_states = set()
    
    value = -INF
    best_action = None
    actions = game.actions(state)
    for i in range(len(actions)):
        result_state = game.result(state, actions[i], X)
        statestr = grid_to_str(result_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = min_value(game,result_state,1)
            states[statestr] = next_state_value
        if (next_state_value > value):
            value = next_state_value
            best_action = actions[i]
    return best_action
 
def max_value(game, state, level):
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = -INF
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, X)
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = min_value(game,next_state,level+1)
            states[grid_to_str(next_state)] = next_state_value
        value = max(value, next_state_value)
    return value

def min_value(game, state, level):
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        #print_grid("Reached terminal state with utility "+str(util)+":",state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = INF
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, O)
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = max_value(game,next_state,level+1)
            states[grid_to_str(next_state)] = next_state_value
        value = min(value, next_state_value)
    return value

def print_grid(title,grid):
    print(title)
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            print(grid[row][col],end = " ")
        print()

def grid_to_str(grid):
    """ Returns a string version of the grid"""
    return "".join(grid[0])+"".join(grid[1])+"".join(grid[2])

def play_game():
    game = TicTacToe()
    test_again = "Y"
    grid = copy.deepcopy(EMPTY_GRID)
    print("Hello! Welcome to the Tic Tac Toe game")
    player_name = input("Please enter your name: ")
    print("Have a wonderful game with the AI, " + player_name + "\nMay the best player wins")
    choice = input("Would like to go first? (y/n)")
    if choice == "y":
        player = "O" # Represents human player
    else:
        player = "X"
    print_grid("Current grid:", grid)
    
    while (not game.terminal_test(grid)):
        if player == O:
            print(player_name + " it's your turn to play")
            ans = input("Enter the row and col to play: ")
            rowStr, colStr = ans.split()
            row, col = int(rowStr), int(colStr)
            print("You Playered ", row, col)
        else:
            ans = minimax_decision(game,grid)
            row, col = ans[0], ans[1]
            print("It's Computer's turn to play")
            print("Computer Playered ", row, col)
        if (grid[row][col] == BLANK):
            grid[row][col] = player
            if (player == O):
                player = X
            else:
                player = O
            print_grid("Current grid:",grid)

    winner = game.winner(grid)
    if (winner == "X"):
        print("Computer wins!")
    elif (winner == "O"):
        print("Congratulations! "+ player_name + "Wins")
    else:
        print("It is a draw.")

if __name__ == "__main__":
   play_game()
    
