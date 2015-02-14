#!/usr/bin/python3

# Skeleton code for the assignment on part-of-speech tagging
# Marco Kuhlmann <marco.kuhlmann@liu.se>

import tagger
from pprint import pprint
import operator
from collections import defaultdict, Counter
import re

# Python class implementing a part-of-speech tagger for Swedish

class MyTagger(tagger.PerceptronTagger):

    def accuracy(self, matrix):
        """Computes accuracy based on the specified confusion matrix."""
        correct = 0
        total = 0
        for key in matrix:
            total += sum(matrix[key].values())
            correct += matrix[key][key]

        #TODO: oneliner
        if(total != 0):
            return correct/total
        else:
            return float('NaN')

    def precision(self, matrix, tag):
        """Computes precision for tag `tag` based on the specified confusion matrix."""
        try:
            return matrix[tag][tag]/sum(matrix[tag].values())
        except:
            return float('NaN')

    def recall(self, matrix, tag):
        """Computes recall for tag `tag` based on the specified confusion matrix."""
        a = 0
        for key in matrix:
            a += matrix[key][tag]

        return matrix[tag][tag]/a

    def confusion_matrix(self, data):
        """Returns a confusion matrix based on the specified data."""
        matrix = {key:{el:0 for el in self.tags} for key in self.tags}

        for sentence in data:
            tagged = list(self.tag(list(zip(*sentence))[0]))
            for i,x in enumerate(sentence):
                matrix[tagged[i][1]][x[1]] += 1

        return matrix

    def tag(self, tokens):
        """Tags the specified tokens."""

        """ baseline
        list = []
        for a in tokens:
            if a in self.tagdict.keys():
                list.append((a,self.tagdict[a]))
            else:
                #most frequent class
                list.append((a,'NN'))
        return list
        """
        return super().tag(tokens)

    def test(self):
        return {el:0 for el in self.tags}

    def make_tagdict(self, data):
        """Creates a tag dictionary based on the specified data."""
        words = defaultdict(self.test)
        for sentence in data:
            for word in sentence:
                words[word[0]][word[1]] +=1

        ret = {}
        for word in words:
            ret[word] = max(words[word].items(), key=operator.itemgetter(1))[0]

        self.tagdict = ret
        return ret;

    def get_features(self, tokens, i, pred_tags):
        """Extract features from the specified configuration."""
        def extract(name, *args):
            features.append((name,) + tuple(args))
        features = []

        extract("current_word", tokens[i])

        extract("end_of_word_2", tokens[i][-2:])
        extract("end_of_word_3", tokens[i][-3:])
        extract("end_of_word_4", tokens[i][-4:])

        extract("start_of_word3", tokens[i][0:3])

        extract("Capitalised", "__isCaps__" if re.match('^[A-Z]',tokens[i]) else "__isNotCaps__")

        if len(tokens) > i+1:
            extract("current_next", tokens[i], tokens[i+1])
            extract("next_word", tokens[i+1])
            if re.match("""[!?,".']""", tokens[i+1]):
                extract("separators", "__separator__")
            if re.match("dje$", tokens[i]):
                extract("forsta", "__COUNT__")

        if len(tokens) > i+2:
            extract("current_next_next", tokens[i], tokens[i+1], tokens[i+2])
            extract("next_next_word", tokens[i+2])

        if i == 0:
            extract("current_word_first", "__isFirst__")

        if i == len(tokens)-1:
            extract("current_word_last", "__isLast__")

        if i != 0:
            extract("pred_before_current", pred_tags[i-1], tokens[i])
            extract('pred_before', pred_tags[i-1])
            extract('word_before', tokens[i-1])

        if i > 1:
            extract("pred_before_before", pred_tags[i-1], pred_tags[i-2])
            extract("word_before_before", tokens[i-1], tokens[i-2])






        return features

# The following code will be run when you call this script from the
# command line.

if __name__ == "__main__":
    import sys

    def LOG(msg):
        sys.stderr.write(msg)
        sys.stderr.flush()

    def load_data(file):
        with open(file) as fp:
            result = []
            for line in fp:
                line = line.rstrip()
                if len(line) == 0:
                    yield result
                    result = []
                else:
                    result.append(tuple(line.split()))

    # List of part-of-speech tags in SUC
    TAGS = 'AB DT HA HD HP HS IE IN JJ KN NN PC PL PM PN PP PS RG RO SN UO VB MAD MID PAD'.split()

    # Train a model on training data and save it to a file.
    # Usage: python3 lab2.py train TRAINING_DATA_FILE MODEL_FILE
    if sys.argv[1] == "train":
        tagger = MyTagger(TAGS)
        LOG("Loading the training data ...")
        training_data = list(load_data(sys.argv[2]))
        LOG(" done\n")
        tagger.make_tagdict(training_data)
        LOG("Training ...")
        tagger.train(training_data)
        LOG(" done\n")
        LOG("Saving model to %s ..." % sys.argv[3])
        tagger.save(sys.argv[3])
        LOG(" done\n")

    # Load a trained model from a file and evaluate it on test data.
    # This will print precision, recall and accuracy.
    # Usage: python3 lab2.py evaluate MODEL_FILE TEST_DATA_FILE
    if sys.argv[1] == "evaluate":
        tagger = MyTagger(TAGS)
        LOG("Loading the model from %s ..." % sys.argv[2])
        tagger.load(sys.argv[2])
        LOG(" done\n")
        matrix = tagger.confusion_matrix(load_data(sys.argv[3]))
        for tag in tagger.tags:
            p = tagger.precision(matrix, tag)
            r = tagger.recall(matrix, tag)
            LOG("tag %s: precision = %.4f, recall = %.4f\n" % (tag, p, r))
        LOG("accuracy = %.4f\n" % tagger.accuracy(matrix))

    # Load a trained model from a file and evaluate it on test data.
    # This will print the confusion matrix.
    # Usage: python3 lab2.py matrix MODEL_FILE TEST_DATA_FILE
    if sys.argv[1] == "matrix":
        tagger = MyTagger(TAGS)
        LOG("Loading the model from %s ..." % sys.argv[2])
        tagger.load(sys.argv[2])
        LOG(" done\n")
        matrix = tagger.confusion_matrix(load_data(sys.argv[3]))
        separator = ","
        for gold in tagger.tags:
            sys.stdout.write("%s" % separator)
            sys.stdout.write("%s" % gold)
        sys.stdout.write("\n")
        for pred in tagger.tags:
            sys.stdout.write("%s" % pred)
            for gold in tagger.tags:
                sys.stdout.write("%s" % separator)
                sys.stdout.write("%d" % matrix[pred][gold])
            sys.stdout.write("\n")
