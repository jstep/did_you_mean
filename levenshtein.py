import os
import re
import sys


#####################################
# Edit/Levenshtein distance functions
#####################################
def call_counter(func):
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
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    
    res = min([levenshtein(s[:-1], t)+1,
               levenshtein(s, t[:-1])+1, 
               levenshtein(s[:-1], t[:-1]) + cost])
    return res

#####################################
# End of Edit/Levenshtien functions
#####################################

try:
    input_word = sys.argv[1].lower()
except IndexError:
    sys.exit("Please provide a word as an argument")

if os.path.exists('/usr/dict/words'):
    path_to_words = '/usr/dict/words' 
elif os.path.exists('/usr/share/dict/words'):
    path_to_words = '/usr/share/dict/words'
else:
    sys.exit("Words file not found. Exiting...")

print("Checking {arg} against words in {file}".format(arg=input_word, file=path_to_words))

# Open and grab the words in the file.
with open(path_to_words) as f:
    all_words_set = {line.strip().lower() for line in f}

def member_word(word):
    """Check if word is in word set. I.e. it's not a mispelled word. """
    if word in all_words_set:
        sys.exit("{} is a real word!".format(sys.argv[1]))

def closest_match(input_word, words):
    member_word(input_word) 
    
    print("Calculating edit distance...")   
    
    # Compute the edit distance between the input word and all words.
    ld_values_list = [levenshtein(input_word, w) for w in words]
    
    print("dotting i's...")   

    # Merge the computed edit values list with the words list.
    ld_dict = dict(zip(ld_values_list, words))
   
   
    print("crossing t's...\n")   
   
    # Get the min value of the edit values list.
    min_key = min(ld_dict.keys())

    return ld_dict.get(min_key)

print("Did you mean {}?".format(closest_match(input_word, all_words_set)))