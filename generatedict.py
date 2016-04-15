# Author: Existanza

import sys
import time
from bisect import bisect_left, insort

start = time.clock()

if len(sys.argv) < 3:
    sys.exit("Error: the input and output files weren't provided.\n"
             "Example: python3 generatedict.py input.txt newdict.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    dictionary = open(sys.argv[2], 'w')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźżäöüßšžõ'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻÄÖÜẞŠŽÕ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
inputList = []


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


def find(w):
    i = bisect_left(inputList, w)
    if i != len(inputList) and inputList[i] == w:
        return True
    return False


for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if 20 >= len(word) > 0 and not find(word):
            insort(inputList, word)
inputFile.close()


for el in inputList:
    dictionary.write(el + '\n')
end = time.clock()

print("Running time: " + str(end - start) + "s")
