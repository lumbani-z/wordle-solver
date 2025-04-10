class WordleState():
    def __init__(self, answer, grey=[], yellow=[], green=[], row=0, col=0, guess=[]):
        self.green = green
        self.yellow = yellow
        self.grey = grey
        self.row = row
        self.col = col
        self.guess = guess
        self.answer = answer
        
    def get_pattern(self):
        return str((self.green, self.yellow, self.row, self.col, self.guess))
    
    def add_letter(self, a):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        self.guess.append(letters[a])

    def get_guess(self):
        return (self.guess)
    
    def invalid(self):
        self.guess = []
    
    def answer(self):
        return(self.answer)
    
    def update_states(self, green, yellow, grey, row, col, guesses):
        self.green = green
        self.yellow = yellow
        self.grey = grey
        self.row = row
        self.col = col
        self.guess = guesses
    
    def update_constraints(self, green, yellow, grey, row, col, guess):
        self.green = green
        self.yellow = yellow
        self.grey = grey
        self.row = row
        self.col = col
        self.guess = guess
        