#!/usr/bin/python3

# Skeleton code for the assignment on part-of-speech tagging
# Marco Kuhlmann <marco.kuhlmann@liu.se>

import tagger

# Python class implementing a part-of-speech tagger for Swedish

class MyTagger(tagger.PerceptronTagger):

    def accuracy(self, matrix):
        """Computes accuracy based on the specified confusion matrix."""
        return super().accuracy(matrix)

    def precision(self, matrix, tag):
        """Computes precision for tag `tag` based on the specified confusion matrix."""
        return super().precision(matrix, tag)

    def recall(self, matrix, tag):
        """Computes recall for tag `tag` based on the specified confusion matrix."""
        return super().recall(matrix, tag)

    def confusion_matrix(self, data):
        """Returns a confusion matrix based on the specified data."""
        return super().confusion_matrix(data)

    def tag(self, tokens):
        """Tags the specified tokens."""
        return super().tag(tokens)

    def make_tagdict(self, data):
        """Creates a tag dictionary based on the specified data."""
        super().make_tagdict(data)

    def get_features(self, tokens, i, pred_tags):
        """Extract features from the specified configuration."""
        return super().get_features(tokens, i, pred_tags)

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
                    result.append(list(line.split()))

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
        
    # Load a trained model from a file and use it to tag new data (in CoNLL format).
    # Usage: python3 lab2.py tag MODEL_FILE IN_DATA_FILE OUT_DATA_FILE
    if sys.argv[1] == "tag":
        tagger = MyTagger(TAGS)
        LOG("Loading the model from %s ..." % sys.argv[2])
        tagger.load(sys.argv[2])
        LOG(" done\n")
        with open(sys.argv[4], 'w') as fp:
            for sentence in load_data(sys.argv[3]):
                tagged_tokens = tagger.tag([token[1] for token in sentence])
                for token, tagged_token in zip(sentence, tagged_tokens):
                    for i in range(len(token), 6):
                        token.append("_")
                    token[3] = tagged_token[1]
                    token[4] = tagged_token[1]
                    fp.write("\t".join(token))
                    fp.write("\n")
                fp.write("\n")
    
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
