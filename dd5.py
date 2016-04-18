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
    while w[0] is not "^":
        w = complete_ngram(w[0:min(len(w), depth)]) + w
    return w[1:-1]


def printf(w):
    print(w, end=' ')
    sys.stdout.flush()


def find(sortedList, w):
    i = bisect_left(sortedList, w)
    if i != len(sortedList) and sortedList[i] == w:
        return True
    return False


def results(wordList):
    inDictCounter = 0
    for w in wordList:
        if find(dictList, w):
            inDictCounter += 1
    print(str(inDictCounter / len(wordList) * 100) + "%", end='')
    return str(inDictCounter)

# 1 - 10% - 10143
# 2 - 17% - 12631
# 3 - 13% - 5167
# 4 - 16% - 2387
# 5 - 30% - 1162
# 6 - 46% - 441
depth = 1
aSize = 50
maxLen = 101
alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźżäöüßšžõ'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻÄÖÜẞŠŽÕ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
aDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet) + 1))}
fDict = defaultdict(list)
inputList, dictList, outputList, neologismsList = ([] for i in range(4))
charCounter, wordCounter = (0, )*2

if len(sys.argv) < 4:
    sys.exit("Error: the input, output and dictionary files weren't provided.\n"
             "Example: python3 main.py input.txt output.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
    dictFile = open(sys.argv[3], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

printf("Parsing input, gathering data")

for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if 0 < len(word) < maxLen:
            if (wordCounter + 1) % 10000 == 0:
                printf(".")
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

wordsRemaining = wordCounter

printf("\nGenerating words, parsing output")

while wordsRemaining > 0:
    w = generate_word()
    outputList.append(w)
    if not find(inputList, w):
        neologismsList.append(w)
    if (wordCounter - wordsRemaining) % (int(wordCounter / 10)) == 0 and wordCounter != wordsRemaining:
        printf(".")
    outputFile.write(w + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

outputFile.close()

print()
results(inputList)
print(" of the input words are correct.")
results(outputList)
print(" of the generated words are correct.")
print(" of the created words are correct." + '\n' + results(neologismsList) + " correct words have been created." + '\n')
print(str(wordCounter) + " words parsed")
print(str(charCounter) + " characters parsed")
print("Running time: " + str(time.clock() - start) + "s")
