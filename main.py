# Code to implement Towers of Corvallis

# TODO:
#   - Finish first run implementation of Code
#   - Write Hueristic funnctions
#   - Implement data loading Code
#   - Second pass modularization for beam search
#   - Implement metghod to store path to goal node / print it out

import Queue as Q

# State: [[[],[],[]],to_cost,hueristic_cost]

#for i in beam_widths:
#    for j in range(num_h):
#        for k in problem_size:
#            for l in range(20):
                #Solve the problem using h or until NMAX is reached
                #Record solution length, num of nodes, cpu time


def search(start_state, goal_state):
    print "Not done yet"
    num_expand = 0
    searched = {}
    q = Q.PriorityQueue()
    q.put((cost(start_state),start_state))

    while at_goal != goal_state or num_expand < NMAX:
        current_state = q.get()
        current_state = current_state[1]
        if current_state[0] == goal_state:
            at_goal = True
        else:
            to_add = expand(current_state)
            num_expand += 1
            for item in to_add:
                if not(searched.has_key(str(item(0)))):
                    q.put((cost(item),item))
        # Pop from the priority queue - need to limit the size in some way
        # Check if that node is the goal node
        # Expand that node
        # Check if any sucessors in the hash table - if not add them to the hash table
        # Now evaluate each of the sucessor states

    return
# Returns the cost of a state -> travel to cost + hueristic cost
def cost(state):
    return 0

# Makes the goal state based on the number given representing the number of blocks
def make_goal(num_size):
    goal = [[],[],[]]
    for i in range(num_size):
        goal[0].insert(0,i)

    return goal

# Expands a given state and returns the children states that can be reached
def expand(current_state):
    return [[[],[],[]],0,0]

# Computes the hueristic for the given state
def h1(current_state, goal_state):
    return 0

# Computes the hueristic for the given state
def h2(current_state, goal_state):
    return 0


print "Starting"
beam_widths = [5,10,15,20,25,50,100,'inf']
num_h = 2
problem_size = [4,6,8,10]
NMAX = 1000000

print "This should have 5"
print make_goal(5)

D = {}

D['make_goal(2)'] = 1

print D.has_key('a')
print D.has_key('make_goal(2)')

q = Q.PriorityQueue()
q.put(-10)
q.put(-5)

while not q.empty():
    print q.get()

print str(make_goal(2))
print '[[1, 0], [], []]'
print str(make_goal(2)) == '[[1, 0], [], []]'
