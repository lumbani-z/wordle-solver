import os
import copy
import heapq
import math
import numpy as np
from get_words import *


class wordleNode:
    def __init__(self, parent, game_state, p, action):
        self._game_state = game_state
        self._p = p
        self._action = action
        self._parent = parent
        self._probabilitiy_distribution_a = None
    
    def __hash__(self):
        """
        Hash function used in the closed list
        """
        return self._game_state.__hash__()
    
    def set_probability_distribution_actions(self, d):
        self._probabilitiy_distribution_a = d
        
    def get_probability_distribution_actions(self):
        return self._probabilitiy_distribution_a
    
    def get_p(self):
        """
        Returns the pi cost of a node
        """
        return self._p
    
    def get_game_state(self):
        """
        Returns the game state represented by the node
        """
        return self._game_state
    
    def get_parent(self):
        """
        Returns the parent of the node
        """
        return self._parent
    
    def get_action(self):
        """
        Returns the action taken to reach node stored in the node
        """
        return self._action

class Trajectory():
    def __init__(self, states, actions):
        self._states = states
        self._actions = actions
        
    def get_states(self):
        return self._states
    
    def get_actions(self):
        return self._actions
    
    def length(self):
        return len(self._states)
    
class picker():
            
    def recover_path(self, wordleNode):
        states = []
        actions = []
        
        state = wordleNode.get_parent()
        action = wordleNode.get_action()
        
        while not state.get_parent() is None:
            states.append(state.get_game_state())
            actions.append(action)
            
            action = state.get_action()
            state = state.get_parent()
            
        states.append(state.get_game_state())
        actions.append(action)
        
        return Trajectory(states, actions)  
    
    def constraints(self, parent, letters, state, col, grey, yellow, green, last):
        domain = letters
        remove = []
        exploit = []
        j = []
        removed = 0
        #print("yellow",yellow)
        #print("green",green)
        if last == -1:
            last = -1
        
        
        probability_distribution = parent.get_probability_distribution_actions() 
        p = probability_distribution
        
        for x in grey:
            index = domain.index(x)
            remove.append(index)
            j.append(index)
        
        for x in yellow:
            if x[0] == col:
                remove.append(x[0])
        for x in green:
            if x[0] == col:
                exploit.append(x[1])               
        
        if len(exploit) > 0:
            return domain.index(exploit[0]), last
        else:
            for x in yellow:
                if x[0] != col and x[1] not in remove and x[1] not in state.get_guess() and last != col:
                    if np.random.random(1) > 0.10:
                        for y in j:
                            removed += probability_distribution[y] 
                            probability_distribution[y] = 0
                        #print(j, col)
                            
                            
                        sum_remaining = sum(probability_distribution)
                        for l in range(len(domain)):
                            probability_distribution[l] += (probability_distribution[l] / sum_remaining) * removed
                        parent.set_probability_distribution_actions(probability_distribution)
                        
                        return domain.index(x[1]), col
            for y in j:
                removed += probability_distribution[y] 
                probability_distribution[y] = 0
            #print(j, col)
                
                
            sum_remaining = sum(probability_distribution)
            for x in range(len(domain)):
                probability_distribution[x] += (probability_distribution[x] / sum_remaining) * removed
            parent.set_probability_distribution_actions(probability_distribution)
            
            removed = 0
            for y in remove:
                removed += p[y] 
                p[y] = 0
            sum_remaining = sum(p)
            for x in range(len(domain)):
                p[x] += (p[x] / sum_remaining) * removed
            return np.random.choice(len(domain), p = p), last
            
        
        

    def search(self, state, model, budget):
        #os.system('cls')
        letters = 'abcdefghijklmnopqrstuvwxyz'
        dictionary = WORDBANK()
        dictionary.generate()
        grey = []
        yellow = []
        green = []
        open = []
        closed = {}
        tries = 0
        root = wordleNode(None, state, 0, -1)
        action_distribution = model.get_probabilities(state.get_pattern())
        root.set_probability_distribution_actions(action_distribution)
        closed[root.__hash__()] = root
        num_guesses = 0
        last = -1
        correct_guess = state.answer
        while num_guesses < 6:
            col = -1
            attempt = ''
            heapq.heappush(open, root)
            
            while len(attempt) < 5:
                col += 1
                if tries > budget:
                    return tries, None, False
                parent = heapq.heappop(open)            
                state = parent.get_game_state()
                a, last = self.constraints(parent, letters, state, col, grey, yellow, green, last)
                #print(state.green)
                #actions = state.constraints(parent.get_action())
                #if num_guesses == 0:
                #    actions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
                probability_distribution = parent.get_probability_distribution_actions() 
               # a = np.random.choice(26, p = probability_distribution)

                guess = copy.deepcopy(state)
                guess.add_letter(a)
                guess_node = wordleNode(parent, guess, 0, a)
                action_distribution = model.get_probabilities(guess.get_pattern())
                guess_node.set_probability_distribution_actions(action_distribution)
                prob = parent.get_p() + probability_distribution[a]
                guess_node._p = prob
                attempt += (letters[a])
                heapq.heappush(open, guess_node)

            if dictionary.valid(attempt):
               # print(attempt)
                x = 5
                root = heapq.heappop(open)    
                if num_guesses > 0:
                    while x > 0:
                        #print("ha")
                        guess.update_states(green, yellow, grey, num_guesses, x-1, (guess.get_guess())[:x])                        
                        hash_guess = guess_node.__hash__()
                        closed[hash_guess] = hash_guess
                        guess_node = guess_node.get_parent()
                   #     print(guess.get_guess()[:x])
                  #      print(guess.get_pattern())
                        x -= 1
                else:
                    
                    while x > 0:
                        guess.update_states(green, yellow, grey, num_guesses, x-1, (guess.get_guess())[:x])                        
                        hash_guess = guess_node.__hash__()
                        closed[hash_guess] = hash_guess
                        guess_node = guess_node.get_parent()
                       # print(guess.get_guess()[:x])
                       # print(guess.get_pattern())
                        x -= 1
                if attempt == guess.answer:
                    path = self.recover_path(guess_node)
                    return tries, path, True
                correct = [(index, x) for index, x in enumerate(correct_guess)]
               # print(correct)
                    
                grey2 = [x for x in attempt if x not in guess.answer]
                yellow2 = [(index, x) for index, x in enumerate(attempt) if x in guess.answer if (index, x) not in correct]
                green2 = [(index, x) for index, x in enumerate(attempt) if x in guess.answer if (index, x) in correct]
                
                for x in grey2:
                    if x not in grey:
                        grey.append(x)
                for x in yellow2:
                    if x not in yellow:
                        yellow.append(x)
                for x in green2:
                    if x not in green:
                        green.append(x)
                    
                #print(grey)
                #print(yellow)
                #print(green)
                
                num_guesses += 1
                tries += 1
                guess.guess = ['']
                
            else:
               # print(attempt)
               # print(grey)
                guess.invalid()
                heapq.heappop(open)  
                tries += 1

               

        return tries, None, False
