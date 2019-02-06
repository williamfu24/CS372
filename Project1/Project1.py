#William Fu
#AI
#Project 1

from pqueue import*
import math 
def distance_on_unit_sphere(lat1, long1, lat2, long2):
    lat1 = float(lat1)
    long1 = float(long1)
    lat2 = float(lat2)
    long2 = float(long2)
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
    math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc
    

class Node:
    def __init__(self):
        self.state = 0
        self.parent = 0
        self.g = 0 #dist between starting and current node
        self.h = 0 #dist between current and end node
        self.f = 0
        self.street = 0

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash((self.state))

    def __ne__(self, other):
        return self.state != other.state


def main():
    print("Debug y/n?: ")
    user_in = input()
    if(user_in == 'y'):
        debug = True
    else:
        debug = False
    print('Enter a filename: ')
    filename = input()
    infile = open(filename)
    #read in file
    location={}
    road = {}
    for word in infile:
        word = word.replace("\n", "")
        #for each line if theres a new line character delete it
        if (len(word)== 0):
            break
        #ends if there is nothing left (==0)
        if(word[0] == 'l'):
            word = word.split('|')
            location[int(word[1])]=[float(word[2]),float(word[3])]
        #if its a location add it to the location dictionary with the id as key
            #and longitue/lattitude as values

        if(word[0] =='r'):
            word = word.split('|')
            #for roads
            if (int(word[1]) in location):
                #if id is in location then it exists
                information = word[2] + " " + word[3] + " mph " + word[4]
                if(int(word[1]) not in road):
                    #if id not in road add new entry
                    road[int(word[1])]=[information]
                else:
                    #if id in road then append road to list
                    road[int(word[1])].append((information))
            if (int(word[2]) in location):
                information = word[1] + " " + word[3] + " mph " + word[4]
                if(int(word[2]) not in road):
                    road[int(word[2])]=[information]
                else:
                    road[int(word[2])].append((information))
    infile.close()
        
    #loop to keep the search location running
    while True:
        print('Enter the start location or zero to quit: ')
        x = int(input())
        if x == 0: break
        if (x in location):
            for key in location:
                if(x==key):
                    temp=location[x]
                    start_lat=temp[1]
                    start_long=temp[0]
        else:
            print("First location does not exist")
        print('Enter the destination or zero to quit: ')
        y = int(input())
        if y == 0: break
        if (y in location):
            for key in location:
                if(y==key):
                    temp=location[y]
                    dest_lat=temp[1]
                    dest_long=temp[0]
        else:
            print("Second location does not exist")

        #A* algorithm
        counter = -1
        path = []
        street = []
        
        node = Node()
        node.state = int(x)
        node.g = 0
        node.h = ((distance_on_unit_sphere(start_lat, start_long, dest_lat, dest_long)*3960)/(65/60))
        node.f = node.g + node.h
        node.parent = None
        frontier = PQueue()
        frontier.enqueue(node, node.f)
        explored = set() #cant make it work without 0
        while (1):
            if (frontier.empty()):
                raise Exception("Error frontier empty")
            node = frontier.dequeue()
            counter = counter + 1
            if(debug):
                print("\nNode Visited:", node.state,", g=", node.g, ", h=", node.h, " .f=", node.f)
            if (node.state == int(y)):
                #return solution because node state == y (destination)
                print ("\nGoal: ", node.state)
                print ("  Nodes Visited = ", counter)
                print ("  Total Travel Time = ", node.g, " mins")
                while (node.state != int(x)):
                    path.append(node)
                    node = node.parent
                path.reverse()
                print ("  Path:")
                print (x, " (starting location)")
                for q in path:
                    print(q.state, q.street)
                return
            if (node.state in location):
                temp_node = location[node.state]
                node_lat = temp_node[1]
                node_long = temp_node[0]
            #explored.add(int(node.state)) #add node.state to explored set
            explored.add(node)
            #loop through children
            for rd in road[node.state]: 
                part = rd.split(" ")
                rd_mph = float(part[1])
                child_nd = Node()
                child_nd.state = int(part[0])
                temp = location[child_nd.state]
                child_lat = temp[1]
                child_long = temp[0]
                child_nd.g = ((((distance_on_unit_sphere(node_lat, node_long, child_lat, child_long)*3960)/(rd_mph/60))+node.g))
                child_nd.h = ((distance_on_unit_sphere(dest_lat, dest_long, child_lat, child_long)*3960)/(65/60))
                child_nd.f = child_nd.g + child_nd.h
                child_nd.parent = node
                child_nd.street = part[3]
                
                #if child_node.state is not in explored add to frontier
                if ((child_nd not in explored) and (not frontier.contains(child_nd))):
                    #print("adding to frontier")
                    frontier.enqueue(child_nd, child_nd.f)
                    if (debug):
                        print("  Adding: ", child_nd.state, ", g=", child_nd.g, " h=", child_nd.h," .f=", child_nd.f)
                #else if child_node.state is already in frontier, but child_node.f is better than the frontier. replace
                elif (frontier.contains(child_nd)):
                    if (child_nd.f<frontier.get_priority(child_nd)):
                        frontier.change_priority(child_nd, -1)
                        oldNode = frontier.dequeue()
                        frontier.enqueue(child_nd, child_nd.f)
                        if (debug):
                            print("  Update on frontier: ", child_nd.state)
                            print("    Old: ", oldNode.state, " g=", oldNode.g, " h=", oldNode.h, " f=", oldNode.f)
                            print("    New: ", child_nd.state, " g=", child_nd.g, " h=", child_nd.h, " f=", child_nd.f)


main()

