import os
import time


class Bootstrap:
    def __init__(self, states):
        self._states = states
        self._number_problems = len(states)
    
    def train_model(self, planner, model, valid_words, wordlist, threshold):
        number_solved = 0          
        current_solved_puzzles = set()
        attempts = []
        
        while len(current_solved_puzzles) < self._number_problems:
            number_solved = 0

            for name, state in self._states.items():
                if name in current_solved_puzzles:
                    continue
                print('Attempting ', name, end=": ")
                print(state.answer, end=" result: ")

                path, passed, num_guesses = planner.search(state, model, valid_words, wordlist, threshold)
                if passed and name not in current_solved_puzzles:
                    number_solved += 1
                    current_solved_puzzles.add(name)    
                    model.update(path)
                    print('solved.', num_guesses, "Guesses")
                    attempts.append(num_guesses)
            if threshold+1 < 5:
                print('Number solved: ', number_solved)
                print()
                print("Exploiting after", threshold+2, "guesses.")
            else:
                print('Number solved: ', number_solved)
                print()
                if threshold+1 == 5:
                    print("No exploiting")
        return attempts
    