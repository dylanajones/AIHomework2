# Code to implement Towers of Corvallis

# TODO:


#   - Speed up possible for beam search of a given size

import Queue as Q
import copy
import time
import math
import cProfile

# State: [[[],[],[]],to_cost,hueristic_cost,parent]

# Function to perform the search
def search(start_state, goal_state, param, size):

    global NMAX

    at_goal = False
    num_expand = 0
    # Hash table for storing states expanded
    searched = {}

    # Priority Queue for storing states to expand
    if size != 'inf':
        q = Q.PriorityQueue(size)
    else:
        q = Q.PriorityQueue()

    # Putting in the start state
    q.put((cost(start_state),start_state))

    while not(at_goal) and num_expand < NMAX and not(q.empty()):

        current_state = q.get() # Pop first item off priority queue

        current_state = current_state[1]

        if not(searched.has_key(str(current_state[0]))):
            num_expand += 1
            searched[str(current_state[0])] = cost(current_state) # Adding in expanded nodes
            if current_state[0] == goal_state:
                at_goal = True
            else:
                to_add = expand(current_state, goal_state, param)
                for item in to_add:
                    if not(searched.has_key(str(item[0][0]))):
                        if not(q.full()):

                            q.put((cost(item),item))
                        else:

                            hold_list = []
                            while not q.empty():
                                hold_list.append(q.get())

                            hold_list.append((cost(item),item))
                            hold_list.sort()

                            for i in range(size):
                                if not(q.full()):
                                    q.put(hold_list.pop(0))


    if at_goal or num_expand == NMAX:
        return [num_expand, current_state]
    else:
        return [float('nan'), current_state]

# Returns the cost of a state -> travel to cost + hueristic cost
def cost(state):
    return state[1] + state[2]

# Makes the goal state based on the number given representing the number of blocks
def make_goal(num_size):
    goal = [[],[],[]]
    for i in range(0,num_size):
        goal[0].insert(0,i)

    return goal

# Expands a given state and returns the children states that can be reached
def expand(current_state, goal_state, param):
    # Making a list to hold all the states created by expanding the current state
    return_list = []
    # If the first tower is not empty move the top disk from it
    if current_state[0][0]:
        for i in range(1,3): # Defining the range to move to
            my_copy = copy.deepcopy(current_state)
            return_list.insert(0,my_copy) # Add a new state to the return list
            to_move = return_list[0][0][0].pop(0) # pop off the disk to move
            return_list[0][0][i].insert(0,to_move) # put the new tile on top of the new tower
            return_list[0][1] = current_state[1] + 1 # update the travel to cost
            return_list[0][2] = h(return_list[0], goal_state, param) # calculate the hueristic
            return_list[0][3] = current_state

    # If the second tower is not empty move the top disk from it
    if current_state[0][1]:
        for i in [0,2]: # Defining the range to move to
            my_copy = copy.deepcopy(current_state)
            return_list.insert(0,my_copy) # Add a new state to the return list
            to_move = return_list[0][0][1].pop(0) # pop off the disk to move
            return_list[0][0][i].insert(0,to_move) # put the new tile on top of the new tower
            return_list[0][1] = current_state[1] + 1 # update the travel to cost
            return_list[0][2] = h(return_list[0], goal_state, param) # calculate the hueristic
            return_list[0][3] = current_state

    # If the third tower is not empty move the top disk from it
    if current_state[0][2]:
        for i in range(0,2): # Defining the range to move to
            my_copy = copy.deepcopy(current_state)
            return_list.insert(0,my_copy) # Add a new state to the return list
            to_move = return_list[0][0][2].pop(0) # pop off the disk to move
            return_list[0][0][i].insert(0,to_move) # put the new tile on top of the new tower
            return_list[0][1] = current_state[1] + 1 # update the travel to cost
            return_list[0][2] = h(return_list[0], goal_state, param) # calculate the hueristic
            return_list[0][3] = current_state

    return return_list

# Computes the hueristic for the given state, uses a different hueristic based
#   on what value is given to param
def h(current_state, goal_state, param):
    est_cost = 0
    if param == 1: # Addmissible hueristic - relaxed problem of moving any disk anywhere
        est_cost = len(goal_state[0]) - len(current_state[0][0])
    elif param == 2: # Inaddmissible hueristic - finding moving cost for each tile and Adding
        for i in range(len(goal_state[0])):
            # Calculate how many would need to be moved for this to get to its place
            pos = goal_state[0].index(i)
            g_index = pos - len(goal_state[0])
            if current_state[0][0].count(i) == 0:
                # Need to find it and Calculate distance - not on goal peg
                if current_state[0][1].count(i) == 0:
                    # Tile looking for is on last peg
                    r_index = current_state[0][2].index(i)
                else:
                    # Tile looking for is on the middle peg
                    r_index = current_state[0][1].index(i)

                if len(current_state[0][0]) < abs(g_index + 1):
                    r_index += abs(g_index + 1) - len(current_state[0][0])
                else:
                    r_index += len(current_state[0][0]) - abs(g_index + 1)
                add_cost = r_index + 2
            else:
                # Need to find how many to remove / move - on goal peg
                r_index = current_state[0][0].index(i) - len(current_state[0][0])
                if g_index == r_index:
                    add_cost = 0
                elif g_index > r_index:
                    add_cost = abs(g_index - r_index) + 2
                else:
                    add_cost = current_state[0][0].index(i) + abs(g_index - r_index) + 2
            est_cost += add_cost
    else:
        est_cost = 0
    return est_cost

def print_solution(state, flag):
    if state[3]:
        if flag == 'v':
            print state[0]
        return 1 + print_solution(state[3], flag)
    else:
        if flag == 'v':
            print state[0]
        return 1

# Function to load the data for a given problem size
def load_data(size):
    data = []

    f = open(str(size)+'_size.txt','r')
    for i in range(20):
        s = f.readline()
        s = s.replace("\n","")
        to_add = []
        for j in range(len(s)):
            to_add.insert(0,int(s[j]))

        data.append(to_add)

    return data

# Main function, this is what should be called to run everything
def main():

#for i in beam_widths:
#    for j in range(num_h):
#        for k in problem_size:
#            for l in range(20):

    beam_widths = [5,10,15,20,25,50,100,'inf']
    num_h = 2
    problem_size = [4,5,6,7,8,9,10]

    for size in problem_size:
        d = load_data(size)
        print "Problem Size"
        print size
        for width in beam_widths:
            print "Width being processed"
            print width
            for i in range(1,num_h+1):
                print "hueristic being used"
                print i


                # Variables to hold results data
                num_nodes = []
                time_taken = []
                solution_length = []

                # Loops for running many times - See above
                for item in d: # Change to d for full testing
                    # Should add code to write results to a file
                    start_state = [[item,[],[]],0,0,[]]
                    start = time.clock()
                    result = search(start_state, make_goal(size),i,width)
                    end = time.clock()
                    if not(math.isnan(result[0])):
                        num_nodes.append(result[0])
                        solution_length.append(print_solution(result[1],'n'))
                        time_taken.append(end - start)

                f = open('output/'+str(size)+'/'+str(i)+'_'+str(width)+'.txt','w')

                if len(num_nodes) > 0:
                    f.write(str(sum(num_nodes, 0.0) / len(num_nodes)))
                    f.write('\n Average number of Nodes\n')
                    print sum(num_nodes, 0.0) / len(num_nodes)

                if len(time_taken) > 0:
                    f.write(str(sum(time_taken, 0.0) / len(time_taken)))
                    f.write('\n Average Wall Clock time Taken\n')
                    print sum(time_taken, 0.0) / len(time_taken)

                if len(solution_length) > 0:
                    f.write(str(sum(solution_length, 0.0) / len(solution_length)))
                    f.write('\n Average Solution length\n')
                    print sum(solution_length, 0.0) / len(solution_length)

                f.write(str(len(d) - len(solution_length)))
                f.write('\n Number of problem for which no solution was found\n')
                print len(d) - len(solution_length)


    print "**********************************************"

NMAX = 1000000
print "Starting"
main()
