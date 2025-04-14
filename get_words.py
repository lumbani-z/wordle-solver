import nltk
import os
import numpy as np
from nltk.corpus import words
from nltk.corpus import names

class WORDBANK:
    def generate(self):
        all_words = words.words()
        all_names = names.words()

        five_letter_names = [name for name in all_names if len(name) == 5]
        five_letter_words = [word for word in all_words if len(word) == 5 and word not in five_letter_names]

        self.word_list = 'word_list/'
        np.random.shuffle(five_letter_words)
        if not os.path.exists(self.word_list):
            os.makedirs(self.word_list)
        self.word_list += 'words.txt'    
        f = open(self.word_list, "w")
        f.close()
        seen = []
        f = open(self.word_list, "r")
        if f.read():
            f.close()
            f = open(self.word_list, "w")
            for word in five_letter_words:
                f.write(word.lower() + '\n')
                if word.lower() not in seen:
                    if len(seen) < 1000:
                        seen.append(word.lower())
        else:
            f.close()
            f = open(self.word_list, "a")
            for word in five_letter_words:
                f.write(word.lower() + '\n')
                if word.lower() not in seen:
                    if len(seen) < 1000:
                        seen.append(word.lower())
        f.close()
        np.random.shuffle(seen)
        self.lines = len(seen)
        f = open(self.word_list, "w")
        while len(seen) > 0:
            word = seen.pop()
            if word.lower() not in seen:
                f.write(word.lower() + '\n')
        f.close()
        
    
    def valid(self, guess):
        f = open(self.word_list, "r")
        words = f.readlines()
        for word in words:
            if guess == word.strip():
                f.close()  
                return True
        f.close()  
        return False

if __name__ == "__main__":
    # Ensures both the names and common english words corpora are downloaded
    try:
        nltk.data.find('corpora/names.zip')
    except LookupError:
        nltk.download('names')
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')
    
    dictionary = WORDBANK()
    dictionary.generate()
    word = dictionary.answer()
    
    if dictionary.valid("hoped"):
        print('yerrr')
    else:
        print('Not in word list')
    print(word)
    if dictionary.is_sol("hopes"):
        print('yea')
    else:
        print("nooooo")