# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    x,y = newPos
    curFood = currentGameState.getFood()
    score = 10000000
    for i in range(0, len(list(curFood))):
      for j in range(0, len(list(curFood[i]))):
        if curFood[i][j] == True:
          tmpScore = abs(x-i) + abs(y-j)
          if tmpScore < score:
            score = tmpScore
    

    for gh in newGhostStates:
      gx, gy = gh.getPosition()
      dis = abs(gx-x) + abs(gy-y)
      if dis <= 2 and gh.scaredTimer==0 :
        score = 10000000


    return -1*score


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    action = self.value(gameState, 0, 0).keys()[0]
    return action

  def value(self, gameState, agentIndex, depthNum):
    if agentIndex == 0 and depthNum ==0:
      return self.max_value(gameState, agentIndex, depthNum+1)
    
    if depthNum == self.depth and agentIndex == gameState.getNumAgents()-1:
      return self.evaluationFunction(gameState)
    
    agentIndex += 1
    if agentIndex == gameState.getNumAgents():
      agentIndex = 0
    if agentIndex != 0:
      return self.min_value(gameState, agentIndex, depthNum)
    else :
      return self.max_value(gameState, agentIndex, depthNum+1)

  def max_value( self, gameState, agentIndex, depthNum):
    v = -10000000
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum)
      if type(varList) is int:
        if v < varList:
          v = varList
          vdict = {action : v}
      else:
        #print(varList)
        if v < varList.values()[0]:
          v = varList.values()[0]
          vdict = {action : v}
    return vdict

  def min_value( self, gameState, agentIndex, depthNum):
    v = 10000000
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum)
      if type(varList) is int:
        if v > varList:
          v = varList
          vdict = {action : v}
      else:
        #print(varList)
        if v > varList.values()[0]:
          v = varList.values()[0]
          vdict = {action : v}
    return vdict



class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    action = self.value(gameState, 0, 0, -10000000, 10000000).keys()[0]
    return action

  def value(self, gameState, agentIndex, depthNum, a, b):
    if agentIndex == 0 and depthNum ==0:
      return self.max_value(gameState, agentIndex, depthNum+1, a, b)
    
    if depthNum == self.depth and agentIndex == gameState.getNumAgents()-1:
      return self.evaluationFunction(gameState)
    
    agentIndex += 1
    if agentIndex == gameState.getNumAgents():
      agentIndex = 0
    if agentIndex != 0:
      return self.min_value(gameState, agentIndex, depthNum, a, b)
    else :
      return self.max_value(gameState, agentIndex, depthNum+1, a, b)

  def max_value( self, gameState, agentIndex, depthNum, a, b):
    v = -10000000
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum, a, b)
      if type(varList) is int:
        if v < varList:
          v = varList
          vdict = {action : v}
      else:
        #print(varList)
        if v < varList.values()[0]:
          v = varList.values()[0]
          vdict = {action : v}
    return vdict

  def min_value( self, gameState, agentIndex, depthNum, a, b):
    v = 10000000
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum, a, b)
      if type(varList) is int:
        if v > varList:
          v = varList
          vdict = {action: v}
      else:
        #print(varList)
        if v > varList.values()[0]:
          v = varList.values()[0]
          vdict = {action: v}
      if v >= b :
        return vdict
      a = max(a, v)
    return vdict
    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    action = self.value(gameState, 0, 0).keys()[0]
    return action

  def value(self, gameState, agentIndex, depthNum):
    if agentIndex == 0 and depthNum ==0:
      return self.max_value(gameState, agentIndex, depthNum+1)
    
    if depthNum == self.depth and agentIndex == gameState.getNumAgents()-1:
      return self.evaluationFunction(gameState)
    
    agentIndex += 1
    if agentIndex == gameState.getNumAgents():
      agentIndex = 0
    if agentIndex != 0:
      return self.exp_value(gameState, agentIndex, depthNum)
    else :
      return self.max_value(gameState, agentIndex, depthNum+1)

  def max_value( self, gameState, agentIndex, depthNum):
    v = -float('inf')
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum)
      if type(varList) is int or type(varList) is float:
        if v < varList:
          v = varList
          vdict = {action: v}
      else:
        #print(varList)
        if v < varList.values()[0]:
          v = varList.values()[0]
          vdict = {action : v}
    return vdict

  def exp_value( self, gameState, agentIndex, depthNum):
    v = 0
    vdict = {}
    allActions = gameState.getLegalActions(agentIndex)
    if Directions.STOP in allActions:
      allActions.remove(Directions.STOP)
    if not allActions:
      return self.evaluationFunction(gameState)
    p = 1.0/len(allActions)
    for action in allActions:
      varList = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, depthNum)
      #print(varList)
      #print(depthNum, agentIndex)
      if type(varList) is int or type(varList) is float:
        v = v+ p*varList
        vdict = {action: v}
      else:
        #print(varList)
        v = v+ p*varList.values()[0]
        vdict = {action: v}
    return vdict
    

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"

  if currentGameState.isWin():
    return 10000000
  if currentGameState.isLose():
    return -10000000
  curFood = currentGameState.getFood().asList()  
  ghostStates = currentGameState.getGhostStates() 
  capPos = currentGameState.getCapsules()  
  curPos = list(currentGameState.getPacmanPosition())
  score=[]
  capScore=[]

  for food in curFood:
    dis = manhattanDistance(food, curPos)
    score.append(dis)
  score.sort()
  for cap in capPos:
    dis = manhattanDistance(cap, curPos)
    capScore.append(dis)
  capScore.sort()
  #print(capScore)
  if len(capScore)>1:
    #print("yes")
    return currentGameState.getScore() - capScore[0]*200
  return currentGameState.getScore() - score[0]

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

