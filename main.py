import nltk
import os
import numpy as np
import time
from nltk.corpus import words
from nltk.corpus import names
from get_words import *
from model import *
from picker import *
from wordle import *
from bootstrap import *

def main():
    # Ensures both the names and common english words corpora are downloaded
    try:
        nltk.data.find('corpora/names.zip')
    except LookupError:
        nltk.download('names')
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')
    
    
    states = {}
    dictionary = WORDBANK()
    wordlist = open(dictionary.generate(), 'r')
    #correct_word = dictionary.answer()
    correct_word = 'audio'
    easy_instance = 'word_list/easy.txt'

   
    j = 0
    limit = 50
    for word in wordlist.readlines():
        s = WordleState(word.lower().strip())
        if word.strip() == 'audio':
            easy = s
        states['Word_' + str(j)] = s
        j += 1   
        if j == limit:
            break

    #print(len(states))
    wordlist.close()

    print('Loaded ', len(states), ' instances.')

    start = time.time()
    bootstrap = Bootstrap(states)

    pick_logic = picker()
    bootstrap.train_model(pick_logic, Model())

if __name__ == "__main__":
    main()