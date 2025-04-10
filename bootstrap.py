import os
import time
from os.path import join

class Bootstrap:
    def __init__(self, states, initial_budget=5000):
        self._states = states
        self._number_problems = len(states)
        
        self._initial_budget = initial_budget
        
        self._log_folder = 'training_logs/'
            
        if not os.path.exists(self._log_folder):
            os.makedirs(self._log_folder)
    
    def train_model(self, planner, model):
        iteration = 1
        number_solved = 0
        total_expanded = 0
        
        budget = self._initial_budget
        start = time.time()
        
        current_solved_puzzles = set()
                
        while len(current_solved_puzzles) < self._number_problems:
            number_solved = 0
            
            for name, state in self._states.items():
                if name in current_solved_puzzles:
                    continue
                print('Attempting ', name, end=": ")
                print(state.answer, end=" result: ")
                #print()

                tries, path, passed = planner.search(state, model, budget)
                total_expanded += tries
                     
                if passed and name not in current_solved_puzzles:
                    number_solved += 1
                    current_solved_puzzles.add(name)    
                    model.update(path)
                    print('solved.', tries)
                else:
                    print('failed.', tries)
            
            end = time.time()
            with open(join(self._log_folder + 'training_bootstrap'), 'a') as results_file:
                results_file.write(("{:d}, {:d}, {:d}, {:d}, {:d}, {:f} ".format(iteration, 
                                                                                 number_solved, 
                                                                                 self._number_problems - len(current_solved_puzzles), 
                                                                                 budget,
                                                                                 total_expanded,
                                                                                 end-start)))
                results_file.write('\n')
            
            print('Number solved: ', number_solved)
            if number_solved == 0:
                #budget *= 2
                print('Budget: ', budget)
                continue
                                    
            iteration += 1
    