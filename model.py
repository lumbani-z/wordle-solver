import numpy as np

class UniformModel:
    def get_probabilities(self, _):
        return np.ones(26) / 26

class Model:
    def __init__(self):
        self._table = {}
        self._increment = 5

    def get_probabilities(self, pattern):
        if pattern not in self._table:
            self._table[pattern] = np.ones(26)

        return self._table[pattern] / np.sum(self._table[pattern])
    
    def update(self, path):
        action = path.get_actions()
        state = path.get_states()
        for x in range(0, len(state)):
            regular = (state[x].get_pattern())
            if regular not in self._table:
                self._table[regular] = np.ones(26) 

            self._table[regular][action[x]] += self._increment
