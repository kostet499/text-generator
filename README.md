train.py
Functions

get_files():
    Parses console for arguments
    Asserts ways to model file, input directory

transform(namespace, line):
    Cleans line from file of stuff
    Splits it to words

check_words(dictionary, word1, word2):
    Creates bigram if it does not exist
    Else increases its frequency

check_start_word(dictionary, word):
    Creates special bigram of two words:
        "start word" and 'word'
    *"start word" is a specificator for marking text beginning, end of sentence
     ("start word" goes after words with "?.!")

take_words(dictionary, word1, word2):
    Considers two cases:
    1. Word1 is "start word"
    2. Word1 is usual word

is_end(word):
    Checks 'word' for being previous to "start word"
    (whether word is end of sentence or not)


count_number(dictionary, word):
    counts probability for every bigram related to 'word'

Code:
    Reads files by line
    For every pair of words calls function 'take_words'
    If variable 'lastword' is end of sentence, bigram is created not with a
    'lastword' but with "first word", which we actually won't see in generated text

    Counts probabilities for all words and bigrams in 'dictionary'

    Writes 'dictionary' to file

generate.py
Functions

is_end(word):
    The same implementation as in 'train.py'

generate(dictionary, word):
    1. Generates a word after 'word'

gen_word(dictionary, lastword):
    Two cases:
    1. Lastword is end of sentence(text beginning)
    2. Lastword is usual word

parse_cmd():
    Parses command line
    Asserts directory for output(if specified), length of word sequence, model file

Code:
    Opens model and loads 'dictionary'
    Generates word sequence and puts it to specified file or standard output stream
    Closes file if it is not std out