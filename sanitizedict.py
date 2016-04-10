# -*- coding: utf-8 -*-
# Author: Existanza

import sys
import time

start = time.clock()

if len(sys.argv) < 3:
    sys.exit("Error: the input and output files weren't provided.\n"
             "Example: python3 dd.py input.txt output.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

alphabetSize = 40
alphabet = '+^$aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
alphabetList = [c for c in alphabet]
capitals = '+^$AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
alphabetDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet)+1))}


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if len(word) > 0:
            outputFile.write(word + '\n')

inputFile.close()
outputFile.close()

end = time.clock()

print("Czas wykonywania: " + str(end - start) + "s")
