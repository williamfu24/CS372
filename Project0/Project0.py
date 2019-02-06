#William Fu
#AI
#Project 0

print('Enter a filename: ')
filename = input()
infile = open(filename)
#read in file

location = dict()
road = {}
#2 dictionaries to place values

for word in infile:
    word = word.replace("\n", "")
    #for each line if theres a new line character delete it
    if (len(word)== 0):
        break
    #ends if there is nothing left (==0)
    if(word[0] == 'l'):
        word = word.split('|')
        location[word[1]]=[[word[2],word[3]]]
    #if its a location add it to the location dictionary with the id as key
        #and longitue/lattitude as values

    if(word[0] =='r'):
        word = word.split('|')
        #for roads
        if (word[1] in location):
            #if id is in location then it exists
            information = word[2] + " " + word[3] + " mph " + word[4]
            if(word[1] not in road):
                #if id not in road add new entry
                road[word[1]]=[information]
            else:
                #if id in road then append road to list
                road[word[1]].append((information))
        if (word[2] in location):
            information = word[1] + " " + word[3] + " mph " + word[4]
            if(word[2] not in road):
                road[word[2]]=[information]
            else:
                road[word[2]].append((information))
                
#loop to keep the search location funning
cont = 1
while cont != 0:
    print('Enter a location or zero to quit: ')
    x = input()
    if x == '0':
        cont=0
    if (x!= '0'):
        if (x in location):
            for key in location:
                if(x==key):
                    print(road[key])
        else:
            print("Location does not exist")
    
infile.close()
