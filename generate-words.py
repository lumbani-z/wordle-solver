import nltk
import os
from nltk.corpus import words
from nltk.corpus import names

class dictionary:
    def generate(self):
        # Generates the word bank for our wordle simulator

        all_words = words.words()
        all_names = names.words()

        # Filter for 5-letter words
        # Filter out 5-letter names 
        five_letter_names = [name for name in all_names if len(name) == 5]
        five_letter_words = [word for word in all_words if len(word) == 5 and word not in five_letter_names]

        self.word_list = 'word_list/'
            
        if not os.path.exists(self.word_list):
            os.makedirs(self.word_list)
        self.word_list += 'words.txt'    
        f = open(self.word_list, "w")
        f.close()
            
        f = open(self.word_list, "r")
        if f.read():
            f.close()
            f = open(self.word_list, "w")
            for word in five_letter_words:
                f.write(word)
                f.write('\n')
        else:
            f.close()
            f = open(self.word_list, "a")
            for word in five_letter_words:
                f.write(word)
                f.write('\n')
        f.close()
        
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
    dictionary().generate()
    print("wow")