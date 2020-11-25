import copy
from _collections import deque
from util import Agent, Policy
from queue import PriorityQueue
from collections import deque
import sys
import numpy as np

DFS = 'dfs'
BFS = 'bfs'
ASTAR = 'astar'
MDP = 'mdp'

ALL_AGENTS = [DFS, BFS, ASTAR]
ITERATIONS = 10000
WALL_REWARD = -150.0
GOAL_REWARD = 100.0
DISCOUNT_FACTOR = 0.5

class DfsAgent(Agent):
  def getPlan(self, problem):
      # TODO: implement DFS w/ this problem
      start = problem.getStartState()
      stack = deque([start])
      visited = {start[0]}
      while len(stack) > 0:
          state = stack.pop()
          if state[0] in visited:
              continue
          if problem.isGoalState(state):
             return state[1]
          visited.add(state)
          for child in problem.getSuccessors(state):
              if child not in visited:
                  stack.append(child)
      return []
    #print('not defined')
    #sys.exit(1)

class BfsAgent(Agent):
  def getPlan(self, problem):

    start = problem.getStartState()
    
    visited = {start[0]}
    q = []

    def push(item):
        if item[0] not in visited:
            visited.add(item[0])
            q.append(item)


    for state in problem.getSuccessors(start): 
        push(state)

    while len(q) > 0:
        state = q.pop(0)

        if problem.isGoalState(state):
            return state[1]

        for child in problem.getSuccessors(state):
            push(child)

    return []

class PriorityItem:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
    
    def __lt__(self, other):
        return self.priority < other.priority

def nullHeuristic(state, problem=None):
    return 0

class AstarAgent(Agent):
  def getPlan(self, problem, heuristic=nullHeuristic):
    # the shape of our queue items is: {position, weight, path, pathCost}

    start = problem.getStartState()
    
    # visited is a dict with the key being the position, and the value being cost to potentially get there
    visited = {start:0}
    q = PriorityQueue()

    def push(item, parent):
        if item not in visited or visited[item] > parent[4]+item[2]:
            item = item + (parent[3] + [item[1]],parent[4]+item[2])
            h = heuristic(item[0],problem)+item[4]
            visited[item[0]] = parent[4] + item[2]
            q.put(PriorityItem(h, item))


    for state in problem.getSuccessors(start): 
        push(state, (0,0,0,[], 0))

    while not q.empty():
        state = q.get().item

        if problem.isGoalState(state[0]):
            return state[3]

        for child in problem.getSuccessors(state):
            push(child, state)

    return []
  
# Generates the maximum utility value of a state from all the possible
# utility values allowed based on possible legal moves
# returns value and the direction
def Q_max(moves, R, V_copy, i, j, problem):
    A = {a: 0 for a in moves}
    for m in moves:
        if m == 'North':
            x = i
            for p in problem.move_probs:
                x = x - 1
                if x >= 0:
                    A[m] += p * (R[x][j] + (DISCOUNT_FACTOR * V_copy[x][j]))
                else:
                    z = x + 1 if x + 1 >= 0 else x + 2
                    A[m] += p * (R[z][j] + (DISCOUNT_FACTOR * V_copy[z][j]))
        elif m == 'South':
            x = i
            for p in problem.move_probs:
                x = x + 1
                if x < len(problem.maze):
                    A[m] += p * (R[x][j] + (DISCOUNT_FACTOR * V_copy[x][j]))
                else:
                    z = x - 1 if x - 1 < len(problem.maze) else x - 2
                    A[m] += p * (R[z][j] + (DISCOUNT_FACTOR * V_copy[z][j]))
        elif m == 'East':
            y = j
            for p in problem.move_probs:
                y = y + 1
                if y < len(problem.maze[0]):
                    A[m] += p * (R[i][y] + (DISCOUNT_FACTOR * V_copy[i][y]))
                else:
                    z = y - 1 if y - 1 < len(problem.maze[0]) else y - 2
                    A[m] += p * (R[i][z] + (DISCOUNT_FACTOR * V_copy[i][z]))
        elif m == 'West':
            y = j
            for p in problem.move_probs:
                y = y - 1
                if y >= 0:
                    A[m] += p * (R[i][y] + (DISCOUNT_FACTOR * V_copy[i][y]))
                else:
                    z = y + 1 if y + 1 >= 0 else y + 2
                    A[m] += p * (R[i][z] + (DISCOUNT_FACTOR * V_copy[i][z]))
    max_key = max(A, key=A.get)
    return max_key, A[max_key]


class MdpAgent(Agent):

    def getPlan(self, problem, iterations=1000):
        # make a copy of the maze
        grid = copy.deepcopy(problem.maze)

        # get the start state
        start = problem.getStartState()

        # Initial Utility Matrix
        V = [[0 for j in range(len(problem.maze[0]))] for i in range(len(problem.maze))]

        # Reward Matrix
        R = [[0 if problem.maze[i][j] == '-' else GOAL_REWARD if
        problem.maze == problem.isGoalState([0]) else WALL_REWARD
              for j in range(len(problem.maze[0]))] for i in range(len(problem.maze))]
        while iterations > 0:

            # Creates a copy of utility matrix for every new iteration
            V_copy = copy.deepcopy(V)
            for i in range(len(problem.maze)):
                for j in range(len(problem.maze[0])):
                    # if the goal is met skip the state and go onto the next state
                    if problem.maze[i][j] == problem.isGoalState([0]):
                        continue

                    # compute the maximum possible utility value for that state along with the direction
                    key, value = Q_max(problem.legalMoves(i, j), R, V_copy, i, j, problem)
                    # remove legal moves
                    # update the utility matrix
                    V[i][j] = value

                    # update the maze with direction
                    problem.maze[i][j] = key
            iterations -= 1
        # Generate the Policy based on above computation
        policy = Policy(problem)

        # TODO: store moves made by agent using the policy and return path
        # reset the maze to original value
        problem.maze = grid
        return policy


def get_agent(agent_type):
  if agent_type == DFS:
    return DfsAgent()
  elif agent_type == BFS:
    return BfsAgent()
  elif agent_type == ASTAR:
    return AstarAgent()
  elif agent_type == MDP:
    return MdpAgent()
    
  print('Invalid agent type.')
  sys.exit(1)
