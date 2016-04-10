# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]


#TODO najpierw wygenerowac 2x liczba slow, potem print


import sys
import time
import random

start = time.clock()

if len(sys.argv) < 3:
    sys.exit("Error: the input and output files weren't provided.\n"
             "Example: python3 dd.py input.txt output.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

aSize = 40
alphabet = '+^$aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
alphabetList = [c for c in alphabet]
capitals = '+^$AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
aDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet) + 1))}
vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
twoGramMatrix = [[0] * aSize for i in range(aSize)]
threeGramMatrix = [[[0] * aSize for i in range(aSize)] *
                   aSize for j in range(aSize)]
characters = [0]*100
sanitizeAttempts = [0]
charCounter = 0
wordCounter = 0


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
    twoGramMatrix[aDict[w[1]]][aDict[w[0]]] += 1
    twoGramMatrix[aDict[w[1]]][0] += 1
    for i in range(2, len(w)):
        twoGramMatrix[aDict[w[i]]][aDict[w[i - 1]]] += 1
        twoGramMatrix[aDict[w[i]]][0] += 1
        threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]] = True


def complete_bigram(ch):
    r = max(1, random.randrange(twoGramMatrix[aDict[ch]][0] + 1))
    s = 0
    i = 1
    while s < r:
        s += twoGramMatrix[aDict[ch]][i]
        i += 1
    return alphabet[i - 1]


def sanitize(w):
    sanitizeAttempts[0] += 1
    if w[0] != '^':
        w = '^' + w + '$'
    for i in range(2, len(w)):
        if not threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]]:
            return False
    return True


def thorough_generate_word(l):
    w = "$"
    while w[0] is not "^":
        w = complete_bigram(w[0]) + w
    if len(w)-2 != l:
        return "^^^^^^"
    return w[1:-1]


for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if len(word) > 0:
            wordCounter += 1
            characters[len(word)] += 1
            charCounter += len(word)
            analyze_n_grams(word)

wordsRemaining = wordCounter

while wordsRemaining > 0:
    r = max(1, random.randrange(wordCounter + 1))
    l = 0
    s = 0
    while s < r:
        s += characters[l]
        l += 1
    l = min(l, 21)
    w = thorough_generate_word(l-1)
    while not sanitize(w):
        w = thorough_generate_word(l-1)
    if wordsRemaining % 1000 == 0:
        print(wordsRemaining)
    outputFile.write(w + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

inputFile.close()
outputFile.close()

end = time.clock()

print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print(str(sanitizeAttempts[0]) + " razy sanitize uruchomionych")
print("Czas wykonywania: " + str(end - start) + "s")
