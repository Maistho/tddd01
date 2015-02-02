#!/usr/bin/python3

# Skeleton code for the assignment on text classification
# Marco Kuhlmann <marco.kuhlmann@liu.se>

import nb
from pprint import pprint
import operator
from collections import defaultdict, Counter
import math

# List of stop words

STOP_WORDS = set("och det att i en jag hon som han på den med var sig för så till är men ett om hade de av icke mig du henne då sin nu har inte hans honom skulle hennes där min man ej vid kunde något från ut när efter upp vi dem vara vad över än dig kan sina här ha mot alla under någon eller allt mycket sedan ju denna själv detta åt utan varit hur ingen mitt ni bli blev oss din dessa några deras blir mina samma vilken er sådan vår blivit dess inom mellan sådant varför varje vilka ditt vem vilket sitta sådana vart dina vars vårt våra ert era vilkas".split())

# Python class implementing a Naive Bayes classifier.  Initially, the
# methods of this class only call the corresponding methods from the
# superclass (NaiveBayesClassifier).  Your task in the assignment is
# to replace these calls with your own code.

class MyNaiveBayesClassifier(nb.NaiveBayesClassifier):

    def get_tokens(self, speech):
        """Returns the token list for the specified speech."""
        return [word for word in speech['tokenlista'] if word not in STOP_WORDS]

    def get_class(self, speech):
        """Returns the class of the specified speech."""
        return "L" if speech['parti'] in ["MP", "S", "V"] else "R"

    def accuracy(self, speeches):
        """Computes accuracy on the specified test data."""

        correct = 0
        for speech in speeches:
            if(self.predict(speech) == self.get_class(speech)):
                correct+=1
        return correct/len(speeches)

        #return super().accuracy(speeches)

    def precision(self, c, speeches):
        """Computes precision for class `c` on the specified test data."""

        tp = 0
        fp = 0
        for speech in speeches:
            if(self.predict(speech) == c):

                if(self.predict(speech) == self.get_class(speech)):
                    tp+=1
                else:
                    fp+=1

        if(tp+fp == 0):
            return float('nan')
        else:
            return tp/(tp+fp)

        #return super().precision(c, speeches)

    def recall(self, c, speeches):
        """Computes recall for class `c` on the specified test data."""

        tp = 0
        fn = 0
        for speech in speeches:
            if(self.get_class(speech) == c):

                if(self.predict(speech) == self.get_class(speech)):
                    tp+=1
                else:
                    fn+=1

        return tp/(tp+fn)

        #return super().recall(c, speeches)

    def predict(self, speech):
        """Predicts the class of the specified speech."""
        # Uppg3
        #return 'R'

        #return super().predict(speech)

        classes = {'R': 0, 'L': 0}
        for c in classes:
            classes[c] = self.pc[c]
            for word in self.get_tokens(speech):
                if word in self.pw[c]:
                    classes[c] += self.pw[c][word]

        return max(classes.items(), key=operator.itemgetter(1))[0]

    def train(self, speeches):
        """Trains using the specified training data."""

        """ get baseline
        l = 0
        r = 0
        for speech in speeches:
            if(self.get_class(speech) == 'L'):
                l+=1
            else:
                r+=1
        if(l > r):
            print('L is bigger')
        elif(r > l):
            print('R is bigger')
        else:
            print('L is the same size as R')
        """


        vocabulary = set()

        classes = defaultdict(int)
        tokens_by_class = defaultdict(list)

        for speech in speeches:

            #P(c)
            c = self.get_class(speech)
            classes[c] +=1

            #P(w|c)
            tokens_by_class[c] += self.get_tokens(speech)

        for c in tokens_by_class:

            #Add to set of all words
            vocabulary.update(tokens_by_class[c])

        self.pc = {}
        for c in classes:
            self.pc[c] = math.log(classes[c]/len(speeches))

        self.pw = {}
        for c in tokens_by_class:
            self.pw[c] = dict.fromkeys(vocabulary,0)
            self.pw[c].update(Counter(tokens_by_class[c]))
            for word in self.pw[c]:
                times = self.pw[c][word]

                self.pw[c][word] = math.log((times+1)/(len(tokens_by_class[c])+len(vocabulary)))






# The following code will be run when you call this script from the
# command line.

if __name__ == "__main__":
    import json
    import sys

    def LOG(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    # Train a model on training data and save it to a file.
    # Usage: python lab1.py train TRAINING_DATA_FILE MODEL_FILE
    if sys.argv[1] == "train":
        classifier = MyNaiveBayesClassifier()
        with open(sys.argv[2]) as fp:
            LOG("Loading training data from %s ..." % sys.argv[2])
            training_data = json.load(fp)
            LOG(" done\n")
        LOG("Training ...")
        classifier.train(training_data)
        LOG(" done\n")
        LOG("Saving model to %s ..." % sys.argv[3])
        classifier.save(sys.argv[3])
        LOG(" done\n")

    # Load a trained model from a file and evaluate it on test data.
    # Usage: python lab1.py evaluate MODEL_FILE TEST_DATA_FILE
    if sys.argv[1] == "evaluate":
        classifier = MyNaiveBayesClassifier()
        LOG("Loading the model from %s ..." % sys.argv[2])
        classifier.load(sys.argv[2])
        LOG(" done\n")
        with open(sys.argv[3]) as fp:
            LOG("Loading test data from %s ..." % sys.argv[3])
            test_data = json.load(fp)
            LOG(" done\n")
        LOG("accuracy = %.4f\n" % classifier.accuracy(test_data))
        for c in sorted(classifier.pc):
            p = classifier.precision(c, test_data)
            r = classifier.recall(c, test_data)
            LOG("class %s: precision = %.4f, recall = %.4f\n" % (c, p, r))
