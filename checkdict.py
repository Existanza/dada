# Author: Existanza

import sys
import time
from bisect import bisect_left, insort

start = time.clock()

if len(sys.argv) < 3:
    sys.exit("Error: the input and dictionary files weren't provided.\n"
             "Example: python3 dd.py input.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    dictionary = open(sys.argv[2], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźż'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
inputList = []
dictList = []


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


def find(w):
    i = bisect_left(dictList, w)
    if i != len(dictList) and dictList[i] == w:
        return True
    return False


for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if len(word) > 0:
            inputList.append(word)
inputFile.close()

for line in dictionary:
    for word in line.split():
        dictList.append(word)
dictionary.close()

wordsInDict = 0
wordsTotal = len(inputList)
inputLengthsList = [0]*21
dictLengthsList = [0]*21

for word in inputList:
    inputLengthsList[len(word)] += 1
    if find(word):
        wordsInDict += 1
        dictLengthsList[len(word)] += 1

percentageList = [0 if dictLengthsList[i] == 0 else dictLengthsList[i]/inputLengthsList[i]*100 for i in range(21)]

for i in range(len(percentageList)):
    print(str(i) + " letter(s): " + str(dictLengthsList[i]) + " / " + str(inputLengthsList[i]) + " (" + str(percentageList[i]) + "%)")

print(str(wordsInDict/wordsTotal*100) + "%")
print("of words exist in dictionary.")

end = time.clock()

print("Running time: " + str(end - start) + "s")
