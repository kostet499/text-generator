import argparse
import pickle
import os.path
import numpy
import re
import collections


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


def generate(bigrams, word):
    """Generate bigram related to word"""
    return numpy.random.choice(list(bigrams[word].keys()), 1,
                               p=list(bigrams[word].values()))[0]


def parse_cmd():
    """Parse cmd for arguments, check them and return namespace"""
    parser = argparse.ArgumentParser(description=
                                     'Output directory for text')
    parser.add_argument('--output',
                        help='choose the file where text will be generated')
    parser.add_argument('--model',
                        help='choose the model file')
    parser.add_argument('--seed',
                        help='choose the first word')
    parser.add_argument('--length', type=int,
                        help='the number of words in the generated sequence')
    namespace = parser.parse_args()

    if namespace.model is None:
        print('Model file is not chosen')
        exit(0)

    if not os.path.isfile(namespace.model) \
            or not namespace.model.endswith('.txt'):
        print('Model file doesn\'t exist or is not a .txt file')
        exit(0)

    if namespace.length is None:
        print('Length is not defined')
        exit(0)

    return namespace


namespace = parse_cmd()

file = None
if namespace.output is None:
    file = os.sys.stdout
else:
    file = open(namespace.output, 'w', encoding="utf-8")

model = open(namespace.model, 'rb')
bigrams = pickle.load(model)
model.close()

lastword = None
length_string = 0
for _ in range(namespace.length):
    word = generate(bigrams, lastword)
    file.write(word + ' ')
    length_string += len(word) + 1
    if length_string > 80:
        file.write('\n')
        length_string = 0
    lastword = is_end(word)

if namespace.output is not None:
    file.close()
