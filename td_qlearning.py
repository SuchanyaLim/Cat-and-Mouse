# Contains class implementation of reinforcement learning, specifically passive temporal difference Q-learning, to learn the optimal policy for the mouse movement

import numpy
import sys
import csv

class td_qlearning:

    alpha = 0.05
    gamma = 0.95

    Qvalues = {}    #stores q-values for all state-trial pairs

    def __init__(self, trial_filepath):
      '''
        Parameters:
            trial_filepath is the path to a .csv file containing a trial through state space
            formatting of the csv   -> 2 col, left = string representation of state, right = string representation of action in state
                                    -> ith row = state-action pair at time i
                                    -> assume only valid actions
      '''

      helper_array = []
      
      with open(trial_filepath, newline='') as csvfile:
          reader = csv.reader(csvfile, delimiter=',', quotechar='|')
          for row in reader:
              pair = (row[0], row[1])
              self.Qvalues[pair] = self.qvalue(row[0], row[1])  # set all initial Q values to 0
              helper_array.append(pair)

      for i in range(len(helper_array)):    #for updating the qvalues of each state-action pair, currently uses 1 iteration
          if i == len(helper_array)-1: break
          self.updateQ(helper_array[i], helper_array[i+1])

      return

    def qvalue(self, state, action):
      '''
        Parameters:
            state: a string representation of a state
            action: a string representation of an action
        Returns: 
            the q-value for the state-action pair if the pair is valid, 
            otherwise return 0
      '''

      if (state, action) in self.Qvalues:
          return self.Qvalues[(state, action)]
      return 0    # if not already in values, then it is 0 (the initial Q value for every state-action pair)

    def policy(self, state):
      '''
        Parameters:
            state: a string representation of a state
        Returns: 
            the policy (the 'best' action out of all possible actions)
            using argmax Q(s,a)
      '''
      all_actions = ["N", "L", "R", "U", "D"]
      # this removes impossible actions
      match state[0][0]:
        case "A":
            all_actions.remove("U")
            all_actions.remove("L")
        case "B":
            all_actions.remove("U")
        case "C":
            all_actions.remove("U")
            all_actions.remove("R")
        case "D":
            all_actions.remove("D")
            all_actions.remove("L")
        case "E":
            all_actions.remove("D")
        case "F":
            all_actions.remove("D")
            all_actions.remove("R")

      values = []
      for action in all_actions:
          values.append(self.qvalue(state, action))

      return all_actions[numpy.argmax(values)]

    def reward(self, state):
      '''
        Parameters:
            state: a string representation of a state
        Returns: 
            the reward value of the given state -- the mouse does not want to be caught by the cat, but does not want to stay at 'home'
      '''
      if (state[0][0] == state[0][1]): return -10       # if cat and mouse on same space
      if (state[0][0] != state[0][1] and state[0][0] != "B"): return 1      # if cat and mouse on different space
      if (state[0][0] == "B"): return -1        # lose points if mouse on space B as cat cannot be on space B
  
    def updateQ(self, curState, nextState):
      '''
      Updates the q value based on the following equation
      Q(s,a) <- Q(s,a) + alpha*(reward(state) + gamma*(argmax(Q(next_s, next_a))) - Q(s,a))
        Parameters:
            curState: a string representation of the current state
            nextState: a string representation of the next state
        Returns: 
            None
      '''
      actionQs = []
      all_actions = ["N", "L", "R", "U", "D"]
      # Q value could still be negative
      # This step removes illegal actions
      match nextState[0][0]:
        case "A":
            all_actions.remove("U")
            all_actions.remove("L")
        case "B":
            all_actions.remove("U")
        case "C":
            all_actions.remove("U")
            all_actions.remove("R")
        case "D":
            all_actions.remove("D")
            all_actions.remove("L")
        case "E":
            all_actions.remove("D")
        case "F":
            all_actions.remove("D")
            all_actions.remove("R")

      # adds qvalue of all possible actions to list to find the max
      for action in all_actions:
          actionQs.append(self.qvalue(nextState[0], action))

      #the equation Q(s,a) <- Q(s,a) + alpha*(reward(state) + gamma*(argmax(Q(next_s, next_a))) - Q(s,a))
      self.Qvalues[curState] += self.alpha*(self.reward(curState) + self.gamma*(max(actionQs)) - self.qvalue(curState[0], curState[1]))
      return

