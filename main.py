import nltk
import numpy as np
import matplotlib.pyplot as plt

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
    
    np.random.seed(0)
    states = {}
    dictionary = WORDBANK()
    dictionary.generate()
    wordlist = (dictionary.word_list)

    thousand_words = open(wordlist, 'r')
    valid_words = (thousand_words.readlines())
    thousand_words.close()
    thousand_words = open(wordlist, 'r')
    
    j = 0
    limit = 1000
    for word in thousand_words.readlines():
        s = WordleState(word.lower().strip())
        if word not in valid_words:
            valid_words.append(word)
        states['Word_' + str(j)] = s
        j += 1   
        if j == limit:
            break
    thousand_words.close()
    thousand_words = open(wordlist, 'r')
    
    lines = len(valid_words)
    print(lines)
    print('Loaded ', len(states), ' instances.')
    print("Exploiting after 1 guess.")

    bootstrap = Bootstrap(states)
    model = Model(lines)
    for threshold in range(0, 6):
        n = threshold
        pick_logic = picker()
        
        attempts = bootstrap.train_model(pick_logic, model, valid_words, wordlist, threshold)
        word_num = []
        bar = [0, 0]
        for x in range(1,len(attempts)+1):
            word_num.append(x)
        for x in attempts:
            if x > 6:
                bar[1] += 1
            else:
                bar[0] += 1
        avg = sum(attempts) / len(attempts)
        if n+1 < 6:
            plt.scatter(word_num, attempts, s=30, alpha=0.2, marker='o', linestyle='-', color='g')
            plt.title('Attempts per word. Exploit after ' + str(n+1) + ' guesses. ' + str(limit) + ' words. Average: ' + str(avg))
            plt.xlabel('Word #')
            plt.ylabel('Guesses')
            plt.savefig('exploit_after' + str(n+1) + '_scatter.png')
            plt.close()
            
            categories = ["Solved in 6: " + str([bar[0]]), "Failed: " + str([bar[1]])]
            plt.bar(categories, bar)
            plt.title("Exploitation after " + str(n+1) + " guesses. " + str(limit) + " words. 6 guess limit")
            plt.ylabel("Number")
            plt.savefig('exploit_after' + str(n+1) + '_bar.png')
            plt.close()
        else:
            plt.scatter(word_num, attempts, s=30, alpha=0.2, marker='o', linestyle='-', color='g')
            plt.title('Attempts per word. No exploiting. ' + str(limit) + ' words. Average: ' + str(avg))
            plt.xlabel('Word #')
            plt.ylabel('Guesses')
            plt.savefig('no_exploit_scatter.png')
            plt.close()
            
            categories = ["Solved in 6: "+ str([bar[0]]), "Failed: " + str([bar[1]])]
            plt.bar(categories, bar)
            plt.title("No exploiting. " + str(limit) + " words. 6 guess limit")
            plt.ylabel("Number")
            plt.savefig('no_exploit_bar.png')
            plt.close()
    print('Done!')
if __name__ == "__main__":
    main()