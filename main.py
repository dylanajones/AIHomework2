# Code to implement Towers of Corvallis

# TODO:
#   - Finish first run implementation of Code
#   - Write Hueristic funnctions
#   - Implement data loading Code
#   - Second pass modularization for beam search
#   - Implement method to store path to goal node / print it out - just have each node store its parent

import Queue as Q
import copy
import time

# State: [[[],[],[]],to_cost,hueristic_cost,parent]

#for i in beam_widths:
#    for j in range(num_h):
#        for k in problem_size:
#            for l in range(20):
                #Solve the problem using h or until NMAX is reached
                #Record solution length, num of nodes, cpu time

# Function to perform the search NOTE: currently will only work for A* and not beam search
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

            searched[str(current_state[0])] = cost(current_state) # Adding in expanded nodes
            if current_state[0] == goal_state:
                at_goal = True
            else:
                to_add = expand(current_state, goal_state, param)
                num_expand += 1
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


    return [num_expand, current_state]

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
    num_cor = len(goal_state[0])
    if param == 1:
        num_cor = len(goal_state[0]) - len(current_state[0][0])
    elif param == 2:
        cur_state = copy.deepcopy(current_state)
        goal = copy.deepcopy(current_state)
        while cur_state[0][0] and goal:
            if cur_state[0][0].pop() == goal.pop():
                num_cor -= 1
    else:
        num_cor = 0
    return num_cor

def print_solution(state):
    if state[3]:
        print state[0]
        print_solution(state[3])
    else:
        print state[0]
        return

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

    p_size = 4

    d = load_data(p_size)
    print d

    b = [d[0]] # Code for testing purposes to shorten the amount printed

    beam_widths = [5,10,15,20,25,50,100,'inf']
    num_h = 2
    problem_size = [4,6,8,10]

    # Variables to hold results data
    num_nodes = []
    time_taken = []

    # Loops for running many times - See above
    for item in d: # Change to d for full testing
        # Should add code to write results to a file
        start_state = [[item,[],[]],0,0,[]]
#        print "This is the goal"
#        print make_goal(p_size)
        start = time.clock()
        result = search(start_state, make_goal(p_size),1,5)
        end = time.clock()
#        print "Number of nodes expanded to get to goal"
#        print result[0]
        num_nodes.append(result[0])
#        print "Solution to get to the goal"
        print_solution(result[1])
#        print "Time to get solution"
#        print end - start
        time_taken.append(end - start)

    print sum(num_nodes) / len(num_nodes)
    print sum(time_taken) / len(time_taken)

NMAX = 1000000
print "Starting"
main()

#q = Q.PriorityQueue(2)

#while q.full() != True:
#    print "Adding to queue"
#    q.put(5)

#while not q.empty():
#    print q.get()
