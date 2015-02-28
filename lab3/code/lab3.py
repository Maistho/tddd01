#!/usr/bin/python3

# Skeleton code for the assignment on syntactic parsing
# Marco Kuhlmann <marco.kuhlmann@liu.se>

import secret
from pprint import pprint

def las(gold_file, pred_file):

    gold = secret.read_data(gold_file)
    pred = secret.read_data(pred_file)

    all = 0
    correct = 0

    for _g, _p in zip(gold,pred):
        for g, p in zip(_g, _p):
            if g[6] == p[6] and g[7] == p[7]:
                correct +=1

            all +=1

    return correct/all

#return secret.las(gold_file, pred_file)

def uas(gold_file, pred_file):
    gold = secret.read_data(gold_file)
    pred = secret.read_data(pred_file)

    all = 0
    correct = 0

    for _g, _p in zip(gold,pred):
        for g, p in zip(_g, _p):
            if g[6] == p[6]:
                correct +=1

            all +=1

    return correct/all
# TODO: Replace with your own code.
    #return secret.uas(gold_file, pred_file)

def lem(gold_file, pred_file):
    gold = secret.read_data(gold_file)
    pred = secret.read_data(pred_file)

    all = 0
    fail = 0

    for _g, _p in zip(gold,pred):
        for g, p in zip(_g, _p):
            if not g[6] == p[6] or not g[7] == p[7]:
                fail += 1
                break

        all += 1

    return (all-fail)/all
# TODO: Replace with your own code.
    #return secret.lem(gold_file, pred_file)

def uem(gold_file, pred_file):
    gold = secret.read_data(gold_file)
    pred = secret.read_data(pred_file)

    all = 0
    fail = 0

    for _g, _p in zip(gold,pred):
        for g, p in zip(_g, _p):
            if not g[6] == p[6]:
                fail += 1
                break

        all += 1

    return (all-fail)/all
# TODO: Replace with your own code.
    return secret.uem(gold_file, pred_file)

class TripleGen():
    def __init__(self,verb):
        self.verb = verb
        self.obj = []
        self.subj = []

    def setObject(self, obj):
        self.obj.append(obj)

    def setSubject(self, subject):
        self.subj.append(subject)

    def getTuple(self):
        if self.subj and self.obj and self.verb:
            retval = []
            for obj in self.obj:
                for subj in self.subj:
                    retval.append((subj, self.verb, obj))
            return retval
        else:
            return None

def extract(file):
    triples = []

    read = secret.read_data(file)

    for _r in read:
        verbs = {}
        for r in _r:
            if r[3] == 'VB':
                verbs[r[0]] = TripleGen(r[1])
        for r in _r:
            if r[6] in verbs.keys(): #might not be needed
                if r[3] in ['NN', 'PM']:
                    if r[7] in ['SS', 'ES']:
                        verbs[r[6]].setSubject(r[1])
                    elif r[7] in ['OO', 'EO']:
                        verbs[r[6]].setObject(r[1])

        for key in verbs.keys():
            triple = verbs[key].getTuple()
            if triple:
                triples += triple

    return triples

if __name__ == "__main__":
    import sys

    if sys.argv[1] == "evaluate":
        gold_file = sys.argv[2]
        pred_file = sys.argv[3]
        print("LAS: %.4f" % las(gold_file, pred_file))
        print("UAS: %.4f" % uas(gold_file, pred_file))
        print("LEM: %.4f" % lem(gold_file, pred_file))
        print("UEM: %.4f" % uem(gold_file, pred_file))

    if sys.argv[1] == "tag":
        tag(sys.argv[2], sys.argv[3])

    if sys.argv[1] == "extract":
        for triple in extract(sys.argv[2]):
            print(triple)
