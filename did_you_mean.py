import os
import re
import sys
import timeit
from typing import Set 

from utils import clear

#####################################
# Edit/Levenshtein distance functions
#####################################
def call_counter(func):
    # Decorator used for debugging how many times a function was called.
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    helper.__name__= func.__name__
    return helper

def memoize(func):
    mem = {}
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in mem:
            mem[key] = func(*args, **kwargs)
        return mem[key]
    return memoizer

@call_counter
@memoize    
def levenshtein(s: str, t: str) -> int:
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    
    res = min([levenshtein(s[:-1], t) + 1,
               levenshtein(s, t[:-1]) + 1,
               levenshtein(s[:-1], t[:-1]) + cost ])
    return res

#####################################
# End of Edit/Levenshtien functions
#####################################

clear()  # clear the terminal screen.
input_word = input("\n\nPlease enter a word.\n")

if os.path.exists('/usr/dict/words'):
    path_to_words = '/usr/dict/words' 
elif os.path.exists('/usr/share/dict/words'):
    path_to_words = '/usr/share/dict/words'
else:
    sys.exit("Words file not found. Exiting...")

print(f"\nChecking {input_word} against words in {path_to_words}")

# Open and grab the words in the file.
with open(path_to_words) as f:
    all_words_set = {line.strip().lower() for line in f}

def real_word(word):
    """Check if word is in word set. I.e. it's not a mispelled word. """
    if word in all_words_set:
        sys.exit("{} is a real word!".format(sys.argv[1]))

def closest_match(input_word: str, words: Set) -> str:
    real_word(input_word) 

    print("Calculating edit distance...")   

    # Compute the edit distance between the input word and all words.
    ld_values_list = [levenshtein(input_word, w) for w in words]
    
    # Merge the computed edit values list with the words list.
    ld_dict = dict(zip(ld_values_list, words))
   
    # Get the min value of the edit values list.
    min_key = min(ld_dict.keys())

    return ld_dict.get(min_key)

if __name__ == "__main__":
    start = timeit.default_timer() 
    print(f"\nDid you mean {closest_match(input_word, all_words_set)}?\n")
    end = timeit.default_timer()
    
    print(f'The function was called {levenshtein.calls} times.')
    print(f'Time taken: {end-start:.2f} seconds\n')

