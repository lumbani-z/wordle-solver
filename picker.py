import os
import copy
import heapq
import math
import numpy as np
from get_words import *


class wordleNode:
    def __init__(self, parent, game_state, action):
        self._game_state = game_state
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
    
class picker():
    def recover_path(self, wordleNode, num_guesses):
        states = []
        actions = []
        
        state = wordleNode.get_parent()
        action = wordleNode.get_action()
        if num_guesses > 1:
            while state.get_parent() is not None:
                states.append(state.get_game_state())
                actions.append(action)
                
                action = state.get_action()
                state = state.get_parent()
            
            states.append(state.get_game_state())
            actions.append(action)
        
        return Trajectory(states, actions)  
    
    def constrain_domain(self, state, grey, yellow, green, valid_words, domain):
        exploit = []
        for x in grey:
            for word in valid_words:
                if x in word:
                    n = domain.index(word)
                    if n not in state.remove:
                        (state.remove).append(n)
                    if x not in state.grey:
                        state.grey.append(x)
        
        for x in yellow: 
            for word in valid_words:
                if x in enumerate(word):
                    n = domain.index(word)
                    
                    if n not in state.remove:
                        (state.remove).append(n)
                if x not in state.yellow:
                    state.yellow.append(x)
        
        if len(green) > 0:
            for word in valid_words:
                pos = 0
                while pos < len(green):
                    if green[pos] in enumerate(word):
                        pos += 1
                        if pos == len(green):
                            break
                    if green[pos] not in enumerate(word):
                        break
                    
                if pos == len(green):
                    n = domain.index(word)
                    if n not in exploit and n not in state.remove:
                        exploit.append(n)
        dont_exploit = []
        for x in exploit:
            if x in state.remove:
                dont_exploit.append(x)
                
        e = [x for x in exploit if x not in dont_exploit]
        return e
                        
    def constraints(self, parent, state, grey, yellow, green, valid_words, num_guesses, threshold):
        domain = valid_words
        removed = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        probability_distribution = parent.get_probability_distribution_actions() 
        p = probability_distribution        
        exploit = self.constrain_domain(state, grey, yellow, green, valid_words, domain)
        
        
        if threshold == 5:
            threshold = 999999
        
        if len(exploit) > 0 and num_guesses >= threshold:
            for x in state.remove:
                removed += probability_distribution[x] 
                probability_distribution[x] = 0
                
            sum_remaining = sum(probability_distribution)
            if removed > 0:
                for x in range(len(domain)):
                    probability_distribution[x] += (probability_distribution[x] / sum_remaining) * removed
            parent.set_probability_distribution_actions(probability_distribution)
            
            p = []
            for x in exploit:
                p.append(probability_distribution[x])
            p = p / np.sum(p)
            return np.random.choice(exploit)
        else:      
            for x in state.remove:
                removed += probability_distribution[x] 
                probability_distribution[x] = 0   
            sum_remaining = sum(probability_distribution)
            if removed > 0:
                for x in range(len(domain)):
                    probability_distribution[x] += (probability_distribution[x] / sum_remaining) * removed    
            parent.set_probability_distribution_actions(probability_distribution)
            choice = np.random.choice(len(domain), p = probability_distribution)
            return choice

    def search(self, state, model, valid_words, list_of_words, threshold):
        dictionary = WORDBANK()
        dictionary.word_list = list_of_words
        grey = []
        yellow = []
        green = []
        open = []
        closed = {}
        tries = 0
        root = wordleNode(None, state, -1)
        action_distribution = model.get_probabilities(state.get_pattern())
        root.set_probability_distribution_actions(action_distribution)
        closed[root.__hash__()] = root
        num_guesses = 1
        correct_guess = state.answer
        attempt = ''
        while attempt != state.answer:
            attempt = ''
            heapq.heappush(open, root)
            parent = heapq.heappop(open)            
            state = parent.get_game_state()
            a = self.constraints(parent, state, grey, yellow, green, valid_words, num_guesses, threshold)
            guess = copy.deepcopy(state)
            guess.guess = valid_words[a].strip()
            guess_node = wordleNode(parent, guess, a)
            action_distribution = model.get_probabilities(guess.get_pattern())
            guess_node.set_probability_distribution_actions(action_distribution)
            attempt = valid_words[a].strip()
            heapq.heappush(open, guess_node)

            if dictionary.valid(attempt):
                root = heapq.heappop(open)    
                if num_guesses > 0:
                    guess.update_states(green, yellow, grey, num_guesses, (guess.get_guess()))                        
                    hash_guess = guess_node.__hash__()
                    closed[hash_guess] = hash_guess
                    guess_node = guess_node.get_parent()
                else:
                    guess.update_states(green, yellow, grey, num_guesses, (guess.get_guess()))                        
                    hash_guess = guess_node.__hash__()
                    closed[hash_guess] = hash_guess
                    guess_node = guess_node.get_parent()

                if attempt == state.answer:  
                    path = self.recover_path(guess_node, num_guesses)
                    return path, True, num_guesses
                
                correct = [(index, x) for index, x in enumerate(correct_guess)]
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
                yellow.sort()
                green.sort()
                num_guesses += 1
                guess.guess = ['']
                
            else:
                guess.invalid()
                heapq.heappop(open)  
                tries += 1

        return path, True, num_guesses
