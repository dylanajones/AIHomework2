#for i in beam_widths:
#    for j in range(num_h):
#        for k in problem_size:
#            for l in range(20):
                #Solve the problem using h or until NMAX is reached
                #Record solution length, num of nodes, cpu time


def search(start_state, goal_state):
    print "Not done yet"
    # Need to make queues here and pop / push from them
    # Also need to design huerisitic functions

    return

def make_goal(num_size):
    goal = [[],[],[]]
    for i in range(num_size):
        goal[0].insert(0,i)

    return goal

def expand(current_state):
    return [[],[],[]]

def h1(current_state, goal_state):
    return 0

def h2(current_state, goal_state):
    return 0


print "Starting"
beam_widths = [5,10,15,20,25,50,100,'inf']
num_h = 2
problem_size = [4,6,8,10]
NMAX = 1000000

print "This should have 5"
print make_goal(5)
