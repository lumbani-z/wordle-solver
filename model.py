import numpy as np

class Model:
    def __init__(self, lines):
        self._table = {}
        self._increment = 1000
        self.actions = lines

    def get_probabilities(self, pattern):
        if pattern not in self._table:
            self._table[pattern] = np.ones(self.actions)

        return self._table[pattern] / np.sum(self._table[pattern])
    
    def update(self, path):
        action = path.get_actions()
        state = path.get_states()
        for x in range(0, len(state)):
            regular = (state[x].get_pattern())
            if regular not in self._table:
                self._table[regular] = np.ones(self.actions) 

            self._table[regular][action[x]] += self._increment
            
