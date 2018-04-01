import argparse
import pickle
import os.path
import numpy
import re


def is_end(word):
    end_symbol = re.sub('[^?.!]', '', word)
    if len(end_symbol) == 0:
        return word
    else:
        return None


def generate(dictionary, word):
    return numpy.random.choice(list(dictionary[word].keys()), 1,
                               p=list(dictionary[word].values()))[0]


def parse_cmd():
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

    if not os.path.isfile(namespace.model):
        print('Model file doesn\'t exist')
        exit(0)

    if namespace.length is None:
        print('Length is not defined')
        exit(0)

    if namespace.output is not None and not os.path.isfile(namespace.output):
        print('Output file doesn\'t exist')
        exit(0)
    return namespace


namespace = parse_cmd()

file = None
if namespace.output is None:
    file = os.sys.stdout
else:
    file = open(namespace.output, 'w', encoding="utf-8")

model = open(namespace.model, 'rb')
dictionary = pickle.load(model)
model.close()

lastword = '.'
length_string = 0
for _ in range(namespace.length):
    word = generate(dictionary, lastword)
    file.write(word + ' ')
    length_string += len(word) + 1
    if length_string > 80:
        file.write('\n')
        length_string = 0
    lastword = word

if namespace.output is not None:
    file.close()
