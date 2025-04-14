class WordleState():
    def __init__(self, answer, grey=[], yellow=[], green=[], row=0, guess=[]):
        self.green = green
        self.yellow = yellow
        self.grey = grey
        self.row = row
        self.guess = guess
        self.answer = answer
        self.remove = []
        self.exploit = []
        
    def get_pattern(self):
        return str((self.green, self.yellow))

    def get_guess(self):
        return (self.guess)
    
    def invalid(self):
        self.guess = []
    
    def answer(self):
        return(self.answer)
    
    def update_states(self, green, yellow, grey, row, guesses):
        yellow.sort()
        green.sort()
        self.green = green
        self.yellow = yellow
        self.grey = grey
        self.row = row
        self.guess = guesses