#!/usr/bin/python3

# Skeleton code for the assignment on syntactic parsing
# Marco Kuhlmann <marco.kuhlmann@liu.se>

import secret

def las(gold_file, pred_file):
    # TODO: Replace with your own code.
    return secret.las(gold_file, pred_file)

def uas(gold_file, pred_file):
    # TODO: Replace with your own code.
    return secret.uas(gold_file, pred_file)

def lem(gold_file, pred_file):
    # TODO: Replace with your own code.
    return secret.lem(gold_file, pred_file)

def uem(gold_file, pred_file):
    # TODO: Replace with your own code.
    return secret.uem(gold_file, pred_file)

def extract(file):
    # TODO: Replace with your own code.
    return secret.extract(file)

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
