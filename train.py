import argparse
import os.path
import fileinput
import re
import pickle


def get_namespace():
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

    return namespace


def transform(is_lower_case, line):
    if is_lower_case:
        line = line.lower()
    line = re.sub('[^a-zA-Zа-яА-ЯъЁё0-9!?.,-]', ' ', line)
    line = line.split(' ')
    return line


def check_words(dictionary, word1, word2):
    if word1 not in dictionary:
        dictionary[word1] = dict([])
    if word2 not in dictionary[word1]:
        dictionary[word1][word2] = 1
    else:
        dictionary[word1][word2] += 1


def is_end(word):
    end_symbol = re.sub('[^?.!]', '', word)
    if len(end_symbol) == 0:
        return word
    else:
        return None


def count_probability(dictionary, word):
    keys = list(dictionary[word].keys())
    number = 0
    for key in keys:
        number += dictionary[word][key]
    for key in keys:
        dictionary[word][key] /= number
    return number


namespace = get_namespace()

infiles = []
if namespace.input_dir is not None:
    infiles = os.listdir(namespace.input_dir)

if len(infiles) == 0 and namespace.input_dir is not None:
    print('Directory is empty')
    exit(0)
print("Training started")

for i in range(len(infiles)):
    if not infiles[i].endswith('.txt'):
        continue
    infiles[i] = os.path.join(namespace.input_dir, infiles[i])

dictionary = dict([])
lastword = None
with fileinput.input(files=infiles,
                     openhook=fileinput.hook_encoded("utf-8")) as f:
    for line in f:
        line = transform(namespace.lc, line)
        for word in line:
            if len(word) == 0:
                continue
            check_words(dictionary, lastword, word)
            lastword = is_end(word)


keys = list(dictionary.keys())
for key in keys:
    count_probability(dictionary, key)

file = open(namespace.model, 'wb')
pickle.dump(dictionary, file)
file.close()
