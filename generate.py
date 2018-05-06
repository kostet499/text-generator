import argparse
import pickle
import os.path
import numpy
import re


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
                        help='choose the model file', required=True)
    parser.add_argument('--seed',
                        help='choose the first word')
    parser.add_argument('--length', type=int,
                        help='the number of words in the generated sequence',
                        required=True)
    namespace = parser.parse_args()

    if not os.path.isfile(namespace.model):
        print('Model file doesn\'t exist')
        exit(0)

    return namespace


def main():
    namespace = parse_cmd()

    file = None
    if namespace.output is None:
        file = os.sys.stdout
    else:
        file = open(namespace.output, 'w', encoding="utf-8")

    model = open(namespace.model, 'rb')
    bigrams = pickle.load(model)
    model.close()

    length_string = 0
    lastword = namespace.seed
    if lastword is not None:
        print(lastword, end=' ')
        length_string = len(lastword)

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


if __name__ == "__main__":
    main()
