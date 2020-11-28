import sys
import copy

class Directions:
  NORTH = 'North'
  SOUTH = 'South'
  EAST = 'East'
  WEST = 'West'

  LIST = [NORTH, SOUTH, EAST, WEST]

  LEFT = {
    NORTH: WEST,
    SOUTH: EAST,
    EAST:  NORTH,
    WEST:  SOUTH
  }

  RIGHT = dict([(y,x) for x, y in LEFT.items()])

  REVERSE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
  }

  TO_VECTOR = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
  }


               
class Agent:
  def getPlan(self, problem):
    print('not defined') 
    sys.exit(1)

class Problem:
    def __init__(self, startState, goalState, maze, width, height, transition_probs=None):
        self.start = startState
        self.maze = maze
        self.width = width
        self.height = height
        self.goal = goalState
        
        if transition_probs is None:
          self.move_probs = [0.25]*4
        else: 
          self.move_probs = transition_probs
        

    def getStartState(self):
        return (self.start, [], 0)

    def isGoalState(self, state):
        return state[0] == self.goal

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and the cumulative cost."
        successors = []
        for direction in Directions.LIST:
            x,y = state[0]
            dx, dy = Directions.TO_VECTOR[direction]
            nextx, nexty = int(x + dx), int(y + dy)
            if nextx >= 0 and nextx < self.width and nexty >= 0 and nexty < self.height and self.maze[nexty][nextx] == 0:
                successors.append(((nextx, nexty), state[1]  + [direction], state[2] + 1))
        return successors
      
    # Generates legal moves available for the agent to move from a state
    def legalMoves(problem, row, column):
        moves = []
        if column - 1 >= 0:
            moves.append('West')
        if row + 1 < len(problem.maze):
            moves.append('South')
        if row - 1 >= 0:
            moves.append('North')
        if column + 1 < len(problem.maze[0]):
            moves.append('East')

        return moves


class Policy:
    def __init__(self, problem):  # problem is a Problem
        # Signal 'no policy' by just displaying the maze there
        self.best_actions = copy.deepcopy(problem.maze)

  
    def __str__(self):
        return '\n'.join([' '.join(
            [str(element) for element in row]
        ) for row in self.best_actions])
