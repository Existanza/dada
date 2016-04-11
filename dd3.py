# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

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
characters = [0]*21
characters2 = [0]*21
words = [[""] for i in range(21)]
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
    for i in range(2, len(w)):
        if not threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]]:
            return False
    return True


def generate_word():
    w = "$"
    while w[0] is not "^":
        w = complete_bigram(w[0]) + w
    return w[1:-1]


def printf(w):
    print(w, end=' ')
    sys.stdout.flush()


print("Parsing input...")

for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if len(word) > 0:
            wordCounter += 1
            characters[min(20, len(word))] += 1
            charCounter += len(word)
            analyze_n_grams(word)

wordsRemaining = wordCounter
wordsToCreate = 2*wordCounter

printf("Creating words")

while wordsToCreate > 0:
    if wordsToCreate % int(wordCounter/5) == 0 and wordCounter != wordsToCreate:
        printf(".")
    w = generate_word()
    while not sanitize(w):
        w = generate_word()
    words[min(len(w), 20)].append(w)
    wordsToCreate -= 1

print()
printf("Parsing output")

while wordsRemaining > 0:
    r = max(1, random.randrange(wordCounter + 1))
    l = 0
    while r >= 0 and l <= 20:
        r -= characters[l]
        l += 1
    l -= 1
    while r < 0:
        r += characters[l]
    characters2[l] += 1
    w = words[l][r % len(words[l])]
    if (wordCounter - wordsRemaining) % (int(wordCounter / 10)) == 0 and wordCounter != wordsRemaining:
        printf(".")
    outputFile.write(w + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

inputFile.close()
outputFile.close()

end = time.clock()

print()
print(characters)
print(characters2)
print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print("Czas wykonywania: " + str(end - start) + "s")
