# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

import random
import sys
import time
from bisect import bisect_left, insort
from collections import defaultdict

start = time.clock()


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


def analyze_n_grams(w):
    w = "^" + w + "$"
    for i in range(len(w)-1, 0, -1):
        for j in range(i, len(w)):
            fDict[w[i:j+1]].append(w[i-1])


def complete_ngram(w):
    return fDict[w][random.randrange(len(fDict[w]))]


def generate_word():
    w = "$"
    while w[0] is not "^" and len(w) <= 3:
        w = complete_ngram(w) + w
    while w[0] is not "^" and len(w) <= 100:
        w = complete_ngram(w[0:min(len(w), 3)]) + w
    return w[1:-1]

# python3 dd5.py pride.txt out.txt wordsEn.txt


def printf(w):
    print(w, end=' ')
    sys.stdout.flush()


def find(sortedList, w):
    i = bisect_left(sortedList, w)
    if i != len(sortedList) and sortedList[i] == w:
        return True
    return False


aSize = 50
maxLen = 21
alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźżäöüßšžõ'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻÄÖÜẞŠŽÕ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
aDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet) + 1))}
fDict = defaultdict(list)
inputList = []
dictList = []
inputLengthsList = [0]*maxLen
dictLengthsList = [0]*maxLen
neologismsLengthsList = [0]*maxLen
outputLengthsList = [0]*maxLen
charCounter, wordCounter, wordsInDict, neologismsInDict = (0,)*4

if len(sys.argv) < 4:
    sys.exit("Error: the input, output and dictionary files weren't provided.\n"
             "Example: python3 main.py input.txt output.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
    dictFile = open(sys.argv[3], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

print("Parsing input, gathering data")

for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if 0 < len(word) < maxLen:
            wordCounter += 1
            charCounter += len(word)
            analyze_n_grams(word)
            insort(inputList, word)
inputFile.close()

for line in dictFile:
    for word in line.split():
        if 0 < len(word) < maxLen:
            dictList.append(word)
dictFile.close()

for word in inputList:
    inputLengthsList[len(word)] += 1
    if find(dictList, word):
        wordsInDict += 1
        dictLengthsList[len(word)] += 1

wordsRemaining = wordCounter
wordsToCreate = wordCounter

print(wordsInDict)
print()
# print(fDict)
printf("Generating words, parsing output")
print()
# '''
while wordsRemaining > 0:
    w = generate_word()
    outputLengthsList[min(20, len(w))] += 1
    if find(dictList, w) and not find(inputList, w):
        neologismsInDict += 1
        neologismsLengthsList[min(20, len(w))] += 1
    if (wordCounter - wordsRemaining) % (int(wordCounter / 10)) == 0 and wordCounter != wordsRemaining:
        printf(".")
    outputFile.write(w + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

outputFile.close()

print("\nWORDS\n")
percentageList = [0 if inputLengthsList[i] == 0 else dictLengthsList[i]/inputLengthsList[i]*100 for i in range(maxLen)]
for i in range(len(percentageList)):
    print(str(i) + " letter(s): " + str(dictLengthsList[i]) + " / " + str(inputLengthsList[i]) + " (" + str(percentageList[i]) + "%)")
print(str(wordsInDict/wordCounter*100) + "%")
print("of words exist in dictionary.")

print("\nNEOLOGISMS\n")
percentageList = [0 if outputLengthsList[i] == 0 else neologismsLengthsList[i]/outputLengthsList[i]*100 for i in range(maxLen)]
for i in range(len(percentageList)):
    print(str(i) + " letter(s): " + str(neologismsLengthsList[i]) + " / " + str(outputLengthsList[i]) + " (" + str(percentageList[i]) + "%)")
print(str(neologismsInDict/wordCounter*100) + "%")
print("of neologisms exist in dictionary.")
# '''
print()
print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print("Czas wykonywania: " + str(time.clock() - start) + "s")
