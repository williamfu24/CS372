#WIlliam FU
#AI Project 2: Connect 3|4
#Wins cond cited from StackOverflow
#drawBoard cited from StackOverflow

import copy
import sys
import math
import time
INF = 1000000

class minimaxInfo:
    def __init__(self, utility, action):
        self.minimax = utility
        self.action = action
class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def changePlayer(self):
        if (self.player == 'MAX'):
            self.player = 'MIN'
        else:
            self.player = 'MAX'
    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        tupleList = []
        for i in range(len(self.board)):
            newtuple = tuple(self.board[i])
            tupleList.append(newtuple)
        return hash(tuple(tupleList))

def main():
    table = dict() 
    print("How many cols: ")
    col = int(input())
    print("How many rows: ")
    row = int(input())
    userTile, compTile = ['O', 'X']
    board = []
    for x in range(row):
        board.append([" "]*col)
    state = State(board,'MAX')
    print("Game A or B")
    game_type = input()
    
    if(game_type=='A'):
        print("Connect 3 or Connect 4: ")
        while (1):
            win_cond = int(input())
            if (win_cond == 3) or (win_cond ==4):
                break
            else:
                print("Value must be either 3 or 4")
                
        print("Playing game with rows=", row, ", cols=", col, ", and n-in-a-row=", win_cond)
        print("Computer/MAX will be X, User/MIN will be O")
        print("Calculating minimax for entire game tree")
        print()
        
        start = time.time()
        val = minimax(state, table, win_cond)
        end = time.time()
        length = end - start
        
        print("Transposition table has", len(table), "states")
        print("Minimax value of start state is ", (-1*val))
        print("Minimax calculations in ", length," s")
        
        if (val < 0):
            print("MAX has a guaranteed win")
        elif (val > 0):
            print("MIN has a guaranteed win")
        elif (val == 0):
            print("Game ends in tie")

        print("Game Start")
        print()
        
        while True:
            if state.player == "MIN":
                print("User's Turn")
                drawBoard(state.board)
                cur = table[state]
                print("The minimax value for this state is: ", (cur.minimax*-1))
                print("The best move is: ", cur.action)
                
                while True:
                    print("Which column do you want to insert? (0-%s or quit)" % (col-1))
                    move = input()
                    if (move.startswith('q')):
                        sys.exit()
                    if not (move.isdigit()):
                        continue
                    move = int(move)
                    if validMove(state.board, move):
                        break
                    
                makeMove(state, move)
                print()
                
                if winner(state, win_cond):
                    player_win = "MIN"
                    break            
                state.changePlayer()
                
            else:
                print("Computer's Turn")
                drawBoard(state.board)
                cur = table[state]
                
                print("The minimax value for this state is: ", (cur.minimax*-1))
                print("The best move is: ", cur.action)
                print("Computer picks: ", cur.action)
                makeMove(state, cur.action)
                print()
                
                if winner(state, win_cond):
                    player_win = "MAX"
                    break
                state.changePlayer()
                
            if boardFull(state.board):
                player_win = 'tie'
                break
            
        drawBoard(state.board)
        print("Winner = ", player_win)

    if(game_type == 'B'):
        win_cond = 4
        print("Enter cutoff depth: ")
        depth = int(input())
        print("Playing game with rows=", row, ", cols=", col, ", and n-in-a-row=", win_cond)
        print("Game Start")
        print()
        ABtable = dict()
        while True:
            if state.player == "MIN":
                print("User's Turn")
                drawBoard(state.board)
                print()
                start = time.time()
                ABtable.clear
                counter = 0
                val = minimaxAB(state, ABtable, alpha, beta, depth, counter, win_cond)
                end = time.time()
                length = end - start
                cur = ABtable[state]
                print("Transposition table has", len(ABtable), "states")
                print("Minimax value of state is ", (-1*val))
                print("Minimax calculations in ", length," s")
                print("The best move is: ", cur.action)
                while True:
                    print("Which column do you want to insert? (0-%s or quit)" % (col-1))
                    move = input()
                    if (move.startswith('q')):
                        sys.exit()
                    if not (move.isdigit()):
                        continue
                    move = int(move)
                    if validMove(state.board, move):
                        break
                makeMove(state, move)
                print()
                if winner(state, win_cond):
                    player_win = "MIN"
                    break
                state.changePlayer()
            else:
                alpha = -INF
                beta = INF
                print("Computer's Turn")
                drawBoard(state.board)
                print()
                start = time.time()
                ABtable.clear
                counter = 0
                val = minimaxAB(state, ABtable, alpha, beta, depth, counter, win_cond)
                end = time.time()
                length = end - start
                cur = ABtable[state]
                print("Transposition table has", len(ABtable), "states")
                print("Minimax value of state is ", (-1*val))
                print("Minimax calculations in ", length," s")
                print("The best move is: ", cur.action)
                makeMove(state, cur.action)
                print("Computer moves: ", cur.action)
                print()
                if winner(state, win_cond):
                    player_win = "MAX"
                    break
                state.changePlayer()
            if boardFull(state.board):
                player_win = 'tie'
                break
        drawBoard(state.board)
        print("Winner = ", player_win)


def drawBoard(board):
    print()
    BOARDWIDTH = len(board[0])
    BOARDHEIGHT = len(board)
    print(' ', end='')
    for x in range(BOARDWIDTH):
        print(' %s  ' % x, end='')
    print()
    print('-----' + ('----' * (BOARDWIDTH - 1)))
    for y in range(BOARDHEIGHT):
        print('|', end='')
        for x in range(BOARDWIDTH):
            print(' %s |' % board[y][x], end='')
        print()
        print('-----' + ('----' * (BOARDWIDTH - 1)))


def validMove(board, move):
    BOARDHEIGHT = len(board)
    BOARDWIDTH = len(board[0])
    if (move < 0 or move >= BOARDWIDTH):
        return False
    elif (board[0][move] == ' '):
        return True

def makeMove(state, move):
    BOARDHEIGHT = len(state.board)
    for y in range(BOARDHEIGHT-1,-1,-1):
        if state.board[y][move] == ' ':
            if (state.player == 'MAX'):
                state.board[y][move] = 'X'
            else:
                state.board[y][move] = 'O'
            return

def boardFull(board): #tie
    BOARDWIDTH = len(board[0])
    for x in range(BOARDWIDTH):
        if (board[0][x] == ' '):
            return False
    return True

def winner(state, win_cond):
    board = state.board
    BOARDWIDTH = len(state.board[0])
    BOARDHEIGHT = len(state.board)
    if (win_cond == 4):
        #hoizontal check
        for x in range(BOARDHEIGHT): #col
            for y in range (BOARDWIDTH -3): #row
                if board[x][y] == 'X' and board[x][y+1] == 'X' and board[x][y+2] == 'X' and board[x][y+3] == 'X':
                    return True
                if board[x][y] == 'O' and board[x][y+1] == 'O' and board[x][y+2] == 'O' and board[x][y+3] == 'O':
                    return True
        #vertical check
        for x in range(BOARDHEIGHT - 3):
            for y in range(BOARDWIDTH):
                if board[x][y] == 'X' and board[x+1][y] == 'X' and board[x+2][y] == 'X' and board[x+3][y] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y] == 'O' and board[x+2][y] == 'O' and board[x+3][y] == 'O':
                    return True                    
        #\ diagonal check
        for x in range(BOARDHEIGHT-3):
            for y in range(BOARDWIDTH-3):
                if board[x][y] == 'X' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X' and board[x+3][y+3] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O' and board[x+3][y+3] == 'O':
                    return True
        #/ diagonal check
        for x in range(BOARDHEIGHT-3):
            for y in range(3, BOARDWIDTH):
                if board[x][y] == 'X' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X' and board[x+3][y-3] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O' and board[x+3][y-3] == 'O':
                    return True
    if (win_cond == 3):
        #hoizontal check
        for x in range(BOARDHEIGHT):
            for y in range(BOARDWIDTH-2):
                if board[x][y] == 'X' and board[x][y+1] == 'X' and board[x][y+2] == 'X':
                    return True
                if board[x][y] == 'O' and board[x][y+1] == 'O' and board[x][y+2] == 'O':
                    return True
        #vertical check
        for x in range(BOARDHEIGHT-2):
            for y in range(BOARDWIDTH):
                if board[x][y] == 'X' and board[x+1][y] == 'X' and board[x+2][y] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y] == 'O' and board[x+2][y] == 'O':
                    return True
        #\ diagonal check
        for x in range(BOARDHEIGHT-2):
            for y in range(BOARDWIDTH-2): 
                if board[x][y] == 'X' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O':
                    return True
        #/ diagonal check
        for x in range(BOARDHEIGHT-2):
            for y in range(2, BOARDWIDTH):
                if board[x][y] == 'X' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X':
                    return True
                if board[x][y] == 'O' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O':
                    return True


#MINIMAX
    
def terminalTest(state, win_cond):
    if (boardFull(state.board) or winner(state, win_cond)):
        return True
    else:
        return False

def utility(state):
    BOARDWIDTH = len(state.board[0])
    BOARDHEIGHT = len(state.board)
    move_counter = 0
    for x in range (BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if state.board[y][x] != ' ':
                move_counter = move_counter + 1
    if (boardFull(state.board)):
        return 0
    elif (state.player == 'MAX'):
        return int(10000 * BOARDWIDTH * BOARDHEIGHT / move_counter)
    else:
        return -int(10000 * BOARDWIDTH * BOARDHEIGHT / move_counter)
    
def action(state):
    BOARDWIDTH = len(state.board[0])
    valid = []
    for x in range (BOARDWIDTH):
        if (validMove(state.board, x)):
            valid.append(x)
    return valid

def result(state, move):
    childBoard = copy.deepcopy(state.board)
    childState = State(childBoard, state.player)
    makeMove(childState, move)
    childState.changePlayer()
    return childState

def PlayerWhoMovesNext(state):
    if state.player == 'MAX':
        return 'MIN'
    else:
        return 'MAX'
    
def minimax(state, table, win_cond):
    if state in table.keys(): 
        return table[state].minimax

    elif terminalTest(state, win_cond):
        u = utility(state)
        table[state] = minimaxInfo(u, None) 
        return u

    elif (PlayerWhoMovesNext(state) == 'MAX'):
        bestMinimaxSoFar = -INF
        bestMoveForState = None 
        for x in action(state):
            childState = result(state, x)
            minimaxOfChild = minimax(childState, table, win_cond)
            if (minimaxOfChild > bestMinimaxSoFar):
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = x
        table[state] = minimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
    
    else:
        bestMinimaxSoFar = INF
        bestMoveForState = None
        for x in action(state):
            childState = result(state, x)
            minimaxOfChild = minimax(childState, table, win_cond)
            if (minimaxOfChild < bestMinimaxSoFar):
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = x
        table[state] = minimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar

def evalFunc(state):
    board = state.board
    BOARDWIDTH = len(board[0])
    BOARDHEIGHT = len(board)
    e = 0
    #Attacks
    #2 in a row
    #hoizontal check
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH-1):
            if board[x][y] == 'X' and board[x][y+1] == 'X':
                e = e+10
            if board[x][y] == 'O' and board[x][y+1] == 'O':
                e = e-10
    #vertical check
    for x in range(BOARDHEIGHT-1):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y] == 'X':
                e = e+10
            if board[x][y] == 'O' and board[x+1][y] == 'O':
                e = e-10
    #\ diagonal check
    for x in range(BOARDHEIGHT-1):
        for y in range(BOARDWIDTH-1): 
            if board[x][y] == 'X' and board[x+1][y+1] == 'X':
                e = e+10
            if board[x][y] == 'O' and board[x+1][y+1] == 'O':
                e = e-10
    #/ diagonal check
    for x in range(BOARDHEIGHT-1):
        for y in range(2, BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y-1] == 'X':
                e = e+10
            if board[x][y] == 'O' and board[x+1][y-1] == 'O':
                e = e-10

    #2 and space on end _XX
    #hoizontal check
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH-2):
            if board[x][y] == ' ' and board[x][y+1] == 'X' and board[x][y+2] == 'X':
                e = e+20
            if board[x][y] == ' ' and board[x][y+1] == 'O' and board[x][y+2] == 'O':
                e = e-20
    #vertical check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y] == 'X' and board[x+2][y] == 'X':
                e = e+20
            if board[x][y] == ' ' and board[x+1][y] == 'O' and board[x+2][y] == 'O':
                e = e-20
    #\ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH-2): 
            if board[x][y] == ' ' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X':
                e = e+20
            if board[x][y] == ' ' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O':
                e = e-20
    #/ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(2, BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X':
                e = e+20
            if board[x][y] == ' ' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O':
                e = e-20
    #XX_
    #hoizontal check
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH-2):
            if board[x][y] == 'X' and board[x][y+1] == 'X' and board[x][y+2] == ' ':
                e = e+20
            if board[x][y] == 'O' and board[x][y+1] == 'O' and board[x][y+2] == ' ':
                e = e-20
    #vertical check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y] == 'X' and board[x+2][y] == ' ':
                e = e+20
            if board[x][y] == 'O' and board[x+1][y] == 'O' and board[x+2][y] == ' ':
                e = e-20
    #\ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH-2): 
            if board[x][y] == 'X' and board[x+1][y+1] == 'X' and board[x+2][y+2] == ' ':
                e = e+20
            if board[x][y] == 'O' and board[x+1][y+1] == 'O' and board[x+2][y+2] == ' ':
                e = e-20
    #/ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(2, BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y-1] == 'X' and board[x+2][y-2] == ' ':
                e = e+20
            if board[x][y] == 'O' and board[x+1][y-1] == 'O' and board[x+2][y-2] == ' ':
                e = e-20
    
    #3 in a row
    #hoizontal check
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH-2):
            if board[x][y] == 'X' and board[x][y+1] == 'X' and board[x][y+2] == 'X':
                e = e+25
            if board[x][y] == 'O' and board[x][y+1] == 'O' and board[x][y+2] == 'O':
                e = e-25
    #vertical check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y] == 'X' and board[x+2][y] == 'X':
                e = e+25
            if board[x][y] == 'O' and board[x+1][y] == 'O' and board[x+2][y] == 'O':
                e = e-25
    #\ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(BOARDWIDTH-2): 
            if board[x][y] == 'X' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X':
                e = e+25
            if board[x][y] == 'O' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O':
                e = e-25
    #/ diagonal check
    for x in range(BOARDHEIGHT-2):
        for y in range(2, BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X':
                e = e+25
            if board[x][y] == 'O' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O':
                e = e-25
    
    #2 with empty on either sides (4) _XX_
    #hoizontal check
    for x in range(BOARDHEIGHT): #col
        for y in range (BOARDWIDTH -3): #row
            if board[x][y] == ' ' and board[x][y+1] == 'X' and board[x][y+2] == 'X' and board[x][y+3] == ' ':
                e = e+30
            if board[x][y] == ' ' and board[x][y+1] == 'O' and board[x][y+2] == 'O' and board[x][y+3] == ' ':
                e = e-30
    #vertical check
    for x in range(BOARDHEIGHT - 3):
        for y in range(BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y] == 'X' and board[x+2][y] == 'X' and board[x+3][y] == ' ':
                e = e+30
            if board[x][y] == ' ' and board[x+1][y] == 'O' and board[x+2][y] == 'O' and board[x+3][y] == ' ':
                e = e-30
    #\ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(BOARDWIDTH-3):
            if board[x][y] == ' ' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X' and board[x+3][y+3] == ' ':
                e = e+30
            if board[x][y] == ' ' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O' and board[x+3][y+3] == ' ':
                e = e-30
    #/ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(3, BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X' and board[x+3][y-3] == ' ':
                e = e+30
            if board[x][y] == ' ' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O' and board[x+3][y-3] == ' ':
                e = e-30

    #2 empty 1 or 1 empty 2 (4) XX_X
    #hoizontal check
    for x in range(BOARDHEIGHT): #col
        for y in range (BOARDWIDTH -3): #row
            if board[x][y] == 'X' and board[x][y+1] == 'X' and board[x][y+2] == ' ' and board[x][y+3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x][y+1] == 'O' and board[x][y+2] == ' ' and board[x][y+3] == 'O':
                e = e-50
    #vertical check
    for x in range(BOARDHEIGHT - 3):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y] == 'X' and board[x+2][y] == ' ' and board[x+3][y] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y] == 'O' and board[x+2][y] == ' ' and board[x+3][y] == 'O':
                e = e-50
    #\ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(BOARDWIDTH-3):
            if board[x][y] == 'X' and board[x+1][y+1] == 'X' and board[x+2][y+2] == ' ' and board[x+3][y+3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y+1] == 'O' and board[x+2][y+2] == ' ' and board[x+3][y+3] == 'O':
                e = e-50
    #/ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(3, BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y-1] == 'X' and board[x+2][y-2] == ' ' and board[x+3][y-3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y-1] == 'O' and board[x+2][y-2] == ' ' and board[x+3][y-3] == 'O':
                e = e-50
    #X_XX
    #hoizontal check
    for x in range(BOARDHEIGHT): #col
        for y in range (BOARDWIDTH -3): #row
            if board[x][y] == 'X' and board[x][y+1] == ' ' and board[x][y+2] == 'X' and board[x][y+3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x][y+1] == ' ' and board[x][y+2] == 'O' and board[x][y+3] == 'O':
                e = e-50
    #vertical check
    for x in range(BOARDHEIGHT - 3):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y] == ' ' and board[x+2][y] == 'O' and board[x+3][y] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y] == ' ' and board[x+2][y] == 'X' and board[x+3][y] == 'O':
                e = e-50
    #\ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(BOARDWIDTH-3):
            if board[x][y] == 'X' and board[x+1][y+1] == ' ' and board[x+2][y+2] == 'X' and board[x+3][y+3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y+1] == ' ' and board[x+2][y+2] == 'O' and board[x+3][y+3] == 'O':
                e = e-50
    #/ diagonal check
    for x in range(BOARDHEIGHT-3):
        for y in range(3, BOARDWIDTH):
            if board[x][y] == 'X' and board[x+1][y-1] == ' ' and board[x+2][y-2] == 'X' and board[x+3][y-3] == 'X':
                e = e+50
            if board[x][y] == 'O' and board[x+1][y-1] == ' ' and board[x+2][y-2] == 'O' and board[x+3][y-3] == 'O':
                e = e-50
    
    #3 with empty on either sides (5)
    #hoizontal check
    for x in range(BOARDHEIGHT): #col
        for y in range (BOARDWIDTH -4): #row
            if board[x][y] == ' ' and board[x][y+1] == 'X' and board[x][y+2] == 'X' and board[x][y+3] == 'X' and board[x][y+4] == ' ':
                e = e+100
            if board[x][y] == ' ' and board[x][y+1] == 'O' and board[x][y+2] == 'O' and board[x][y+3] == 'O' and board[x][y+4] == ' ':
                e = e-100
    #vertical check
    for x in range(BOARDHEIGHT - 4):
        for y in range(BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y] == 'X' and board[x+2][y] == 'X' and board[x+3][y] == 'X' and board[x+4][y] == ' ':
                e = e+100
            if board[x][y] == ' ' and board[x+1][y] == 'O' and board[x+2][y] == 'O' and board[x+3][y] == 'O' and board[x+4][y] == ' ':
                e = e-100
    #\ diagonal check
    for x in range(BOARDHEIGHT-4):
        for y in range(BOARDWIDTH-4):
            if board[x][y] == ' ' and board[x+1][y+1] == 'X' and board[x+2][y+2] == 'X' and board[x+3][y+3] == 'X' and board[x+4][y+4] == ' ':
                e = e+100
            if board[x][y] == ' ' and board[x+1][y+1] == 'O' and board[x+2][y+2] == 'O' and board[x+3][y+3] == 'O' and board[x+4][y+4] == ' ':
                e = e-100
    #/ diagonal check
    for x in range(BOARDHEIGHT-4):
        for y in range(3, BOARDWIDTH):
            if board[x][y] == ' ' and board[x+1][y-1] == 'X' and board[x+2][y-2] == 'X' and board[x+3][y-3] == 'X' and board[x+4][y-4] == ' ':
                e = e+100
            if board[x][y] == ' ' and board[x+1][y-1] == 'O' and board[x+2][y-2] == 'O' and board[x+3][y-3] == 'O' and board[x+4][y-4] == ' ':
                e = e-100
             
    #1 tile = 1 point
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH):
            if board[x][y] == 'X':
                e = e+1
            if board[x][y] == 'O':
                e = e-1
    return e

def minimaxAB(state, table, alpha, beta, depth, counter, win_cond):
    if state in table.keys():
        return table[state].minimax

    elif terminalTest(state, win_cond):
        u = utility(state)
        table[state] = minimaxInfo(u, None)
        return u

    elif counter > depth: 
        e = evalFunc(state)
        return e

    elif PlayerWhoMovesNext(state) == 'MAX':
        bestMinimaxSoFar = -INF
        bestMoveForState = None
        for x in action(state):
            childState = result(state, x)
            minimaxOfChild = minimaxAB(childState, table, alpha, beta, depth, counter+1, win_cond)
            if minimaxOfChild > bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = x
            if bestMinimaxSoFar >= beta:
                return bestMinimaxSoFar
            alpha = max(alpha, bestMinimaxSoFar)
        table[state] = minimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
    else:
        bestMinimaxSoFar = INF
        bestMoveForState = None
        for x in action(state):
            childState = result(state, x)
            minimaxOfChild = minimaxAB(childState, table, alpha, beta, depth, counter+1, win_cond)
            if minimaxOfChild < bestMinimaxSoFar:
                bestMinimaxSoFar = minimaxOfChild
                bestMoveForState = x
            if bestMinimaxSoFar <= alpha:
                return bestMinimaxSoFar
            beta = min(beta, bestMinimaxSoFar)
        table[state] = minimaxInfo(bestMinimaxSoFar, bestMoveForState)
        return bestMinimaxSoFar
            



        
main()
