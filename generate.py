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
                               list(dictionary[word].values()))[0]


def gen_word(dictionary, length, lastword):
    if is_end(lastword) is None:
        return generate(dictionary, 'specialWord1337228')
    return generate(dictionary, lastword)


def count_number(dictionary, word):
    keys = list(dictionary[word].keys())
    number = 0
    for i in range(len(keys)):
        number += dictionary[word][keys[i]]
    for i in range(len(keys)):
        dictionary[word][keys[i]] /= number;
    return number


parser = argparse.ArgumentParser(description=
                                 'Output directory for text')
parser.add_argument('--output', help=
                    'choose the file where text will be generated')
parser.add_argument('--model', help=
                    'choose the model file')
parser.add_argument('--seed', help=
                    'choose the first word')
parser.add_argument('--length', type=int, help=
                    'the number of words in the generated sequence')
namespace, _ = parser.parse_known_args()

if not os.path.isfile(namespace.model):
    print('Model file doesn\'t exist')
    exit(0)

if namespace.length is None:
    print('Length is not defined')
    exit(0)

if namespace.output is not None and not os.path.isfile(namespace.output):
    print('Output file doesn\' not existing')
    exit(0)

file = None
if namespace.output is None:
    file = os.sys.stdout
else:
    file = open(namespace.output, 'w', encoding='windows-1251')

model = open(namespace.model, 'rb')
dictionary = pickle.load(model)
model.close()

keys = list(dictionary.keys())
length = dict([])

for i in range(len(keys)):
    number = count_number(dictionary, keys[i])
    length[keys[i]] = number

lastword = '.'
leni = 0;
for _ in range(namespace.length):
    word = gen_word(dictionary, length, lastword)
    file.write(word + ' ')
    leni += len(word) + 1;
    if leni > 80:
        file.write('\n')
        leni = 0
    lastword = word

if namespace.output is not None:
    file.close()
