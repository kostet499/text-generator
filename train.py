import argparse
import os.path
import fileinput
import re
import pickle


def get_files():
    parser = argparse.ArgumentParser(description=
                                     'Input directory for '
                                     'training files and model')
    parser.add_argument('--input-dir',
                        help='choose the directory with files for training')
    parser.add_argument('--model',
                        help='choose the directory to save the model')
    parser.add_argument('--lc', action='store_true',
                        help='transform to lower case')
    namespace, _ = parser.parse_known_args()

    if namespace.model is None:
        print('File for model is not chosen')
        exit(0)

    if not os.path.isfile(str(namespace.model)):
        print('Chosen file for model is not existing')
        exit(0)

    if namespace.input_dir is not None and not os.path.isdir(
            namespace.input_dir):
        print('Chosen directory for train is not existing')
        exit(0)

    return namespace


def transform(namespace, line):
    if namespace.lc:
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


def check_start_word(dictionary, word):
    start = 'specialWord1337228'
    check_words(dictionary, start, word)


def take_words(dictionary, word1, word2):
    if word1 is None:
        check_start_word(dictionary, word2)
        return
    check_words(dictionary, word1, word2)


def is_end(word):
    end_symbol = re.sub('[^?.!]', '', word)
    if len(end_symbol) == 0:
        return word
    else:
        return None


namespace = get_files()

infiles = []
if namespace.input_dir is not None:
    infiles = os.listdir(namespace.input_dir)

if len(infiles) == 0 and namespace.input_dir is not None:
    print('Directory is empty')
    exit(0)
print("Training started")

for i in range(len(infiles)):
    infiles[i] = namespace.input_dir + '/' + infiles[i]

dictionary = dict([])
lastword = None
with fileinput.input(files=infiles,
                     openhook=fileinput.hook_encoded("utf-8")) as f:
    for line in f:
        if f.filename().find('txt') == -1 and not f.isstdin():
            f.nextfile()
        else:
            line = transform(namespace, line)
            for i in range(len(line)):
                if len(line[i]) == 0:
                    continue
                take_words(dictionary, lastword, line[i])
                lastword = is_end(line[i])

file = open(namespace.model, 'wb')
pickle.dump(dictionary, file)
file.close()
