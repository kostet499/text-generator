import argparse
import os.path
import fileinput
import re
import pickle
import collections


def get_namespace():
    """"Operate with console arguments and return namespace"""
    parser = argparse.ArgumentParser(description=
                                     'Input directory for '
                                     'training files and model')
    parser.add_argument('--input-dir',
                        help='choose the directory with files for training')
    parser.add_argument('--model',
                        help='choose the directory to save the model')
    parser.add_argument('--lc', action='store_true',
                        help='transform to lower case')
    namespace = parser.parse_args()

    if namespace.model is None:
        print('File for model is not chosen')
        exit(0)

    if namespace.input_dir is not None and not os.path.isdir(
            namespace.input_dir):
        print('Chosen directory for train is not existing')
        exit(0)

    if not namespace.model.endswith('.txt'):
        namespace.model = namespace.model + '.txt';

    return namespace


def transform(is_lower_case, line):
    """
    Clean string from rubbish
    :param is_lower_case: change to lower case if true
    :param line: string to operate with
    :return: list of words
    """

    if is_lower_case:
        line = line.lower()
    line = re.sub('[^a-zA-Zа-яА-ЯъЁё0-9!?.,-]', ' ', line)
    line = line.split(' ')
    return line


def insert_bigram(bigrams, word1, word2):
    """Check word1, word2 in dictionary and update them"""
    if word2 not in bigrams[word1]:
        bigrams[word1][word2] = 1
    else:
        bigrams[word1][word2] += 1


def is_end(word):
    """
    Check word for being the end of the sentence
    :param word: word to be checked
    :return: None or String type 
    """

    end_symbol = re.sub('[^?.!]', '', word)
    if len(end_symbol) == 0:
        return word
    else:
        return None


def count_probability(bigrams, word):
    """Calculate chances for every bigram related to word to be generated"""
    keys = list(bigrams[word].keys())
    frequency_word = 0
    for key in keys:
        frequency_word += bigrams[word][key]
    for key in keys:
        bigrams[word][key] /= frequency_word
    return frequency_word


namespace = get_namespace()

infiles = []
if namespace.input_dir is not None:
    infiles = os.listdir(namespace.input_dir)

if len(infiles) == 0 and namespace.input_dir is not None:
    print('Directory is empty')
    exit(0)
print("Training started")

infiles = [os.path.join(namespace.input_dir, file)
           for file in infiles if(file.endswith('.txt'))]

bigrams = collections.defaultdict(dict)
lastword = None
with fileinput.input(files=infiles,
                     openhook=fileinput.hook_encoded("utf-8")) as f:
    for line in f:
        line = transform(namespace.lc, line)
        for word in line:
            if len(word) == 0:
                continue
            insert_bigram(bigrams, lastword, word)
            lastword = is_end(word)


keys = list(bigrams.keys())
for key in keys:
    count_probability(bigrams, key)

file = open(namespace.model, 'wb')
pickle.dump(bigrams, file)
file.close()
