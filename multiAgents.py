# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from math import inf
from functools import partial

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # return successorGameState.getScore()

        agent = self.index

        """
        Set distance of ghost to pacman
        """
        ghostPacmanDist = partial(manhattanDistance, newPos)

        """
        get timer value
        """
        # def ghostActions(ghost):
        #     distance = ghostPacmanDist(ghost.getPosition())
        #
        #     if(ghost.scaredTimer > distance):
        #         return inf
        #     if(distance <= 1):
        #         return -inf
        #     return 0
        #     # print("GHOST ACTIONS", ghostActions)

        def getNewScaredTime(agent):
            for i in range(len(newScaredTimes)):
                return newScaredTimes[i]

        """
        map timer to new ghost states
        """
        # print("GHOST ACTIONS", ghostActions)
        ghostPoints = min(map(getNewScaredTime, newGhostStates))
        # print("GHOST ACTIONS", ghostPoints)
        # print("NewScaredTimes", newScaredTimes)
        # print("NewGhostStates", newGhostStates)
        # print("TIMER", ghostPoints)

        """
        Set distance of ghost to food
        """
        ghostFoodDist = min(map(ghostPacmanDist, newFood.asList()), default=inf)

        nearestFood = 1.0 / (1.0 + ghostFoodDist)

        # return successorGameState.getScore()
        return successorGameState.getScore() + ghostPoints + nearestFood

def scoreEvaluationFunction(currentGameState: GameState):
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
s
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Recursion function
        """
        def miniMaxFunction(state, depth, agent):

            """
            get depth
            if it cycles back to player move down the tree
            """
            if(agent == 0):
                nextDepth = depth - 1
            else:
                nextDepth = depth

            """
            If state is end of game
            """
            if (nextDepth == 0) or (state.isWin()) or (state.isLose()):
                return self.evaluationFunction(state), None

            """
            max = player
            min = ghosts
            """
            if(agent == 0):
                agentType = max
                bestValue = -inf

            else:
                agentType = min
                bestValue = inf
            # print("BEST OF", bestOf)
            # print("BEST VAL", bestVal)

            """
            modulo to keep reverting back and forth between pacman and ghosts
            """
            nextAgent = (agent + 1) % state.getNumAgents()
            bestAction = None

            """
            Loop - get all successor states and legal actions
            """
            for legalAction in state.getLegalActions(agent):
                successorState = state.generateSuccessor(agent, legalAction)
                actionValue, direction = miniMaxFunction(successorState, nextDepth, nextAgent)

                # print(actionValue, direction)

                """
                Decide on the best course of action by getting best value
                """
                if(agentType(bestValue, actionValue) == actionValue):
                    bestValue = actionValue
                    bestAction = legalAction
                    # print(agent, bestValue, bestAction)

            # if(agent == 0):
            #     print(agent, bestValue, bestAction)

            return bestValue, bestAction

        value, legalAction = miniMaxFunction(gameState, self.depth + 1, self.index)
        return legalAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Recursion function
        """
        def alphaBetaFunction(state, depth, alpha, beta, agent):
            """
            Check for Player
            """
            isMax = agent == 0

            """
            get depth
            if it cycles back to player move down the tree
            """
            if (isMax):
                nextDepth = depth - 1
            else:
                nextDepth = depth

            """
            If state is end of game
            """
            if (nextDepth == 0) or (state.isWin()) or (state.isLose()):
                return self.evaluationFunction(state), None

            """
            modulo to keep reverting back and forth between pacman and ghosts
            """
            nextAgent = (agent + 1) % state.getNumAgents()

            """
            max = player
            min = ghosts
            """
            if (isMax):
                agentType = max
                bestValue = -inf
            else:
                agentType = min
                bestValue = inf
            # print("BEST OF", bestOf)
            # print("BEST VAL", bestVal)

            bestAction = None

            """
            Loop - get all successor states and legal actions
            """
            for legalAction in state.getLegalActions(agent):
                successorState = state.generateSuccessor(agent, legalAction)
                actionValue, direction = alphaBetaFunction(successorState, nextDepth, alpha, beta, nextAgent)

                # print(actionValue, direction)

                """
                Decide on the best course of action by getting bestValue
                """
                if (agentType(bestValue, actionValue) == actionValue):
                    bestValue = actionValue
                    bestAction = legalAction
                    # print(agent, bestValue, bestAction)

                """
                set alpha and beta
                """
                if(isMax):
                    """
                    Pruning
                    """
                    if(bestValue > beta):
                        return bestValue, bestAction
                    alpha = max(alpha, bestValue)
                else:
                    """
                    Pruning
                    """
                    if (bestValue < alpha):
                        return bestValue, bestAction
                    beta = min(beta, bestValue)

            return bestValue, bestAction

        value, legalAction = alphaBetaFunction(gameState, self.depth + 1, -inf, inf, self.index)
        return legalAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Recursion function
        """
        def expectimaxFunction(state, depth, agent):
            """
            get depth
            if it cycles back to player move down the tree
            """
            if (agent == 0):
                nextDepth = depth - 1
            else:
                nextDepth = depth

            """
            If state is end of game
            """
            if (nextDepth == 0) or (state.isWin()) or (state.isLose()):
                return self.evaluationFunction(state), None

            """
            max = player
            min = ghosts
            """
            if (agent == 0):
                agentType = max
                bestValue = -inf

            else:
                agentType = min
                bestValue = inf
            # print("BEST OF", bestOf)
            # print("BEST VAL", bestVal)

            """
            modulo to keep reverting back and forth between pacman and ghosts
            """
            nextAgent = (agent + 1) % state.getNumAgents()

            """
            legal actions list available for an agent
            """
            legalActionsList = state.getLegalActions(agent)

            """
            If agents are not pacman
            """
            if(agent != 0):
                """
                Probability = branches of the node of possible agent moves
                """
                probability = 1.0 / len(legalActionsList)
                averageValue = 0

                """
                Loop - get all successor states and legal actions for ghosts
                """
                for legalAction in legalActionsList:
                    successorState = state.generateSuccessor(agent, legalAction)
                    nodeValue, direction = expectimaxFunction(successorState, nextDepth, nextAgent)
                    """
                    calculate for the average of all available nodes
                    """
                    averageValue += probability * nodeValue

                # print(agent, averageValue, legalAction)
                return averageValue, legalAction


            """
            Loop - get all successor states and legal actions for pacman
            """
            for legalAction in legalActionsList:
                successorState = state.generateSuccessor(agent, legalAction)
                actionValue, direction = expectimaxFunction(successorState, nextDepth, nextAgent)

                # print(actionValue, direction)

                """
                Decide on the best course of action by getting best value
                """
                if (agentType(bestValue, actionValue) == actionValue):
                    bestValue = actionValue
                    bestAction = legalAction
                    # print(agent, bestValue, bestAction)

            # if(agent == 0):
            #     print(agent, bestValue, bestAction)

            return bestValue, bestAction

        value, legalAction = expectimaxFunction(gameState, self.depth + 1, self.index)
        return legalAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    """
    Variables
    """
    foodDistance = []
    ghostDistance = 0
    scaredGhosts = 0
    scaredGhostMultiplier = 20
    capsuleMultiplier = 100

    newPos = list(currentGameState.getPacmanPosition())
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()

    """
    Get amount of capsules
    More capsules = more points
    """
    newCapsule = currentGameState.getCapsules()

    # """
    # Set distance of ghost to pacman
    # """
    # ghostPacmanDist = partial(manhattanDistance, newPos)

    """
    get closest food distance
    """
    for food in newFood:
        x = abs(food[0] - newPos[0])
        y = abs(food[1] - newPos[1])
        foodDistance.append(1*(x+y))

    if not foodDistance:
        foodDistance.append(0)

    """
    get ghost distance
    """
    for ghostState in newGhostStates:
        """
        Get scared ghosts number
        """
        if ghostState.scaredTimer == 0:
            scaredGhosts += 1
            ghostDistance = 0
            continue

        ghostPosition = ghostState.getPosition()
        x = abs(ghostPosition[0] - newPos[0])
        y = abs(ghostPosition[1] - newPos[1])

        if(x + y) == 0:
            ghostDistance = 0
        else:
            ghostDistance = (1.0/(x + y))


    # print(currentGameState.getScore())
    # if(len(newGhostStates) - scaredGhosts != 0):
    #     print(currentGameState.getScore(), min(foodDistance), max(ghostDistance),
    #         100 * len(newCapsule), 20 * (len(newGhostStates) - scaredGhosts))
    # print(len(newGhostStates), scaredGhosts)
    # print(ghostDistance, ghostState)
    # print(newCapsule)
    # print(foodDistance, food)

    """
    Score in relation to food and ghost are the main drivers.
    The capsules and scared ghosts are just extras
    """
    return (currentGameState.getScore()
            - min(foodDistance)
            - ghostDistance
            - len(newCapsule) * capsuleMultiplier
            - (len(newGhostStates) - scaredGhosts)) * scaredGhostMultiplier


# Abbreviation
better = betterEvaluationFunction
