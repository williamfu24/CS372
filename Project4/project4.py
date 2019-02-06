#William Fu
#AI Project 4
#
#NOTES:
    #Takeing more then pile is just taking all
    #pile1 = 1 as opposed to your example where pile1 = 0
import random

def main():
    random.seed()
    print("pile1 = 1 not pile1 = 0 | pile2 = 2 not pile2 = 1 | pile3 = 3 not pile3 = 2\n")
    print("How many in pile 1?")
    x = int(input())
    print("How many in pile 2?")
    y = int(input())
    print("How many in pile 3?")
    z = int(input())
    print("How many runs for q-learning?")
    trialNum = int(input())

    print("Initial board is {}-{}-{}, simulating {} games".format(x,y,z,trialNum))
    table = qlearning(trialNum, x, y, z)

    print("Final Q-Values:\n")
    for i in sorted(table):
        print("Q[{0}] = {1}".format(i, table[i]))

    gameOver = 0
    print("Who starts first? (1) P1 or (2) CPU")
    startTurn = int(input())
    turn = startTurn
    pile1 = x
    pile2 = y
    pile3 = z
    while gameOver==0:
        print("BOARD: [{}][{}][{}]".format(pile1,pile2,pile3))
        if turn == 1:
            print("Player turn")
            choice = choiceFunc(pile1, pile2, pile3)
            if choice == 1:
                print("How many do you want to take?")
                takeNum = int(input())
                if takeNum > pile1:
                    pile1 = 0
                else:
                    pile1 -= takeNum
            elif choice == 2:
                print("How many do you want to take?")
                takeNum = int(input())
                if takeNum > pile2:
                    pile2 = 0
                else:
                    pile2 -= takeNum
            else:
                print("How many do you want to take?")
                takeNum = int(input())
                if takeNum > pile3:
                    pile3 = 0
                else:
                    pile3 -= takeNum
                    
        if turn == 2:
            print("CPU turn")
            if startTurn == 1:
                tempTurn = 'B'
                alt = 2
            else:
                tempTurn = 'A'
                alt = 1
            moves = []
            moves = findMoves(pile1,pile2,pile3,alt, table)
            print(moves)
            
            if tempTurn == 'A':
                maxval = -10000
                maxkey = 0
                for i in moves:
                    tempval = table[i]
                    if tempval >= maxval:
                        maxkey = i
                        maxval = tempval
                state, action = maxkey.split(',')
                CPUmove, CPUtake = action[:len(action)//2], action[len(action)//2:]
                CPUmove = int(CPUmove)
                CPUtake = int(CPUtake)
                print("Computer chooses pile {0} and removes {1}".format(CPUmove, CPUtake))
                if CPUmove == 1:
                    pile1 -= CPUtake
                elif CPUmove == 2:
                    pile2 -= CPUtake
                else: #CPUmove == 3
                    pile3 -= CPUtake
                                
            else: #tempTurn = 'B'
                minval = 10000
                minkey = 0
                for i in moves:
                    tempval = table[i]
                    if tempval <= minval:
                        minkey = i
                        minval = tempval
                state, action = minkey.split(',')
                CPUmove, CPUtake = action[:len(action)//2], action[len(action)//2:]
                CPUmove = int(CPUmove)
                CPUtake = int(CPUtake)
                print("Computer chooses pile {0} and removes {1}".format(CPUmove, CPUtake))
                if CPUmove == 1:
                    pile1 -= CPUtake
                elif CPUmove == 2:
                    pile2 -= CPUtake
                else: #CPUmove == 3
                    pile3 -= CPUtake

        #checks for loser
        loser = endGoal(pile1, pile2, pile3, turn)
        if loser != 0:
            print(pile1,pile2,pile3)
            if loser == 2:
                print("CPU lost")
            else:
                print("P1 lost")
            print("Play agane? (1)yes or (2) no")
            ans = int(input())
            if ans == 2:
                gameOver = 1
            else:
                gameOver = 0
                pile1 = x
                pile2 = y
                pile3 = z
                print("Who starts first? (1) P1 or (2) CPU")
                startTurn = int(input())
                turn = startTurn
                turn = turnChange(turn) #just to counteract the turnchange at end of while
        #END OF TURN. CHANGE TURN
        turn = turnChange(turn)


def qlearning(trialNum, x, y, z):
    table = {}
    turn = 1 #change to random later
    a = 0
    while a < trialNum: #REPEAT FOR EACH EPISODE
        random.seed()
        turn = 1
        #SET START STATE
        pile1=x
        pile2=y
        pile3=z
        gameOver = 0
        while gameOver == 0: #REPEAT FOR EACH STEP OF THE EPISODE
            #CHOOSE ACTION (RANDOM)
            move = random.randrange(1, 4) #move from pile 1 - 3
            #making sure pile is able to be taken from
            while 1:
                move = random.randrange(1,4)
                if move == 1:
                    if pile1 == 0:
                        pass
                    else: #PILE ABLE TO BE TAKEN FRON SO TAKE X STICKS
                        take = random.randrange(1, (pile1+1))
                        break
                elif move == 2:
                    if pile2 == 0:
                        pass
                    else:
                        take = random.randrange(1, (pile2+1))
                        break
                else:
                    if pile3 == 0:
                        pass
                    else:
                        take = random.randrange(1, (pile3+1))
                        break
            
            ##if turn == 1:
            if turn == 1:
                tempturn = "A" #turn id
            else:
                tempturn = "B"
            key = "{0}{1}{2}{3},{4}{5}".format(tempturn,pile1,pile2,pile3,move,take)
            if key not in table: #initalize Q[s,a] for all (s,a) pairs
                table[key] = 0
            #make move
            if move == 1:
                pile1 -= take
            elif move == 2:
                pile2 -= take
            else:
                pile3 -= take
            #new state
            altturn = turnChange(turn)
            if turn == 1:
                tempturn = "A"
            else:
                tempturn = "B"            
            #observe reward
            loser = endGoal(pile1,pile2,pile3,turn)
            if loser != 0:
                if loser == 1:
                    r = -1000
                if loser == 2:
                    r = 1000
                gameOver = 1
            else:
                r = 0
            #find all moves for all states 
            moves = []
            moves = findMoves(pile1,pile2,pile3,altturn, table)
            minval = 10000
            minkey = 0
            for i in moves:
                tempval = table[i]
                if tempval < minval:
                    minkey = i
                    minval = tempval
            maxval = -10000
            maxkey = 0
            for i in moves:
                tempval = table[i]
                if tempval > maxval:
                    maxkey = i
                    maxval = tempval
            #if r == 0 then not end state so find future value
            if r == 0:
                if turn == 1:
                    #find the next state and its list of moves and all that jazz
                    table[key] = 1*(r + .9*(table[minkey]))
                    keyAlt = minkey
                else:
                    table[key] = 1*(r + .9*(table[maxkey]))
                    keyAlt = maxkey
            else: #if not 0 then an end state
                table[key] = r
            key = keyAlt
            #change turn
            turn = turnChange(turn)
        #end game. increase trial num
        a+=1
    #when done with all runs
    return table                    
                


def findMoves(pile1,pile2,pile3,turn, table):
    moves = []    
    for i in range(pile1, 0, -1):
        if turn == 1:
            if i != 0: ############ADDED IN EACH LOOP ################### Prevents taking 0 sticks
                moves.append("A{}{}{},{}{}".format(pile1,pile2,pile3,1,i))
                if "A{}{}{},{}{}".format(pile1,pile2,pile3,1,i) not in table.keys():
                    table["A{}{}{},{}{}".format(pile1,pile2,pile3,1,i)] = 0
        else:
            if i != 0: ############ADDED IN EACH LOOP ###################
                moves.append("B{}{}{},{}{}".format(pile1,pile2,pile3,1,i))
                if "B{}{}{},{}{}".format(pile1,pile2,pile3,1,i) not in table.keys():
                    table["B{}{}{},{}{}".format(pile1,pile2,pile3,1,i)] = 0
                
    for i in range(pile2, 0, -1):
        if turn == 1:
            if i != 0: ############ADDED IN EACH LOOP ###################
                moves.append("A{}{}{},{}{}".format(pile1,pile2,pile3,2,i))
                if "A{}{}{},{}{}".format(pile1,pile2,pile3,2,i) not in table.keys():
                    table["A{}{}{},{}{}".format(pile1,pile2,pile3,2,i)] = 0
        else:
            if i != 0: ############ADDED IN EACH LOOP ###################
                moves.append("B{}{}{},{}{}".format(pile1,pile2,pile3,2,i))
                if "B{}{}{},{}{}".format(pile1,pile2,pile3,2,i) not in table.keys():
                    table["B{}{}{},{}{}".format(pile1,pile2,pile3,2,i)] = 0
                
    for i in range(pile3, 0, -1):
        if turn == 1:
            if i != 0: ############ADDED IN EACH LOOP ###################
                moves.append("A{}{}{},{}{}".format(pile1,pile2,pile3,3,i))
                if "A{}{}{},{}{}".format(pile1,pile2,pile3,3,i) not in table.keys():
                    table["A{}{}{},{}{}".format(pile1,pile2,pile3,3,i)] = 0
        else:
            if i != 0: ############ADDED IN EACH LOOP ###################            
                moves.append("B{}{}{},{}{}".format(pile1,pile2,pile3,3,i))
                if "B{}{}{},{}{}".format(pile1,pile2,pile3,3,i) not in table.keys():
                    table["B{}{}{},{}{}".format(pile1,pile2,pile3,3,i)] = 0
    return moves
    
def choiceFunc(pile1, pile2, pile3):
    temp = 1
    while temp == 1:
        print("What pile do you want to take from?")
        choice = int(input())
        if choice == 1:
            if pile1==0:
                print("Pile 1 is empty. choose again")
                pass
            else:
                return choice
        if choice == 2:
            if pile2==0:
                print("Pile 2 is empty. choose again")
                pass
            else:
                return choice
        if choice == 3:
            if pile3==0:
                print("Pile 3 is empty. choose again")
                pass
            else:
                return choice

def endGoal(pile1, pile2, pile3, turn):
    gameOver = 0
    loser = 0
    if (pile1 == 0 and pile2 == 0 and pile3 == 0):
        gameOver = 1
        loser = turn
    return loser
    
def turnChange(turn):
    if turn == 1:
        turn = 2
        return turn
    else:
        turn = 1
        return turn

main()
