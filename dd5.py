# -*- coding: utf-8 -*-
# Author: Existanza

import random
import sys
import time
from bisect import bisect_left, insort
from collections import defaultdict
from tqdm import tqdm, trange

start = time.clock()


def normalize_word(w):
    nw = ''
    if not "—" in w:
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
    return str(inDictCounter / len(wordList) * 100) + "%"

# 1 - 10% - 10143
# 2 - 17% - 12547
# 3 - 14% - 5254
# 4 - 17% - 2431
# 5 - 31% - 1149
# 6 - 41% - 389
# 7 - 56% - 201
# 8 - 64% - 88
# 9 - 67% - 32
depth = 5
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
charCounter, wordCounter, wordsToCreate, actualNeologisms = (0, )*4

if len(sys.argv) < 5:
    sys.exit("Error: the source, input, output, neologisms output and dictionary files weren't provided.\n"
             "Example: python3 main.py input.txt output.txt neologisms.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
    neoFile = open(sys.argv[3], 'w')
    dictFile = open(sys.argv[4], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

lineCount = sum(1 for l in inputFile)
inputFile.seek(0)
for line in tqdm(inputFile, total=lineCount, desc="Parsing input, gathering data"):
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

for wordsToCreate in trange(wordCounter, desc="Generating words, parsing output"):
    w = generate_word()
    outputList.append(w)
    if not find(inputList, w):
        neologismsList.append(w)
    outputFile.write(w + ' ')
    if not find(inputList, w) and not find(dictList, w):
        actualNeologisms += 1
        neoFile.write(w + ' ')
        if actualNeologisms % 10 == 9:
            neoFile.write('\n')
    if wordsToCreate % 10 == 9:
        outputFile.write('\n')
    wordsToCreate += 1
neoFile.close()
outputFile.close()

print(results(inputList) + " of the input words are correct.\n" +
results(outputList) + " of the generated words are correct.\n" +
results(neologismsList) + " of the created words are correct.\n" +
str(actualNeologisms) + " actual neologisms have been created.\n" +
str(wordCounter) + " words parsed.\n" +
str(charCounter) + " characters parsed.\n" +
"Running time: " + str(time.clock() - start) + "s")
