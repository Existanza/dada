# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

# TODO - threegrams?

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

aSize = 50
alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźżäöüßšžõ'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻÄÖÜẞŠŽÕ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
aDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet) + 1))}
twoGramMatrix = [[0] * aSize for i in range(aSize)]
threeGramMatrix = [[[0] * aSize for i in range(aSize)] for j in range(aSize)]
characters = [0] * 21
characters2 = [0] * 21
singletons = [0] * aSize
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
        threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]] += 1


def complete_bigram(ch):
    r = max(1, random.randrange(twoGramMatrix[aDict[ch]][0] + 1))
    s = 0
    i = 1
    while s < r:
        s += twoGramMatrix[aDict[ch]][i]
        i += 1
    return alphabet[i - 1]


def sanitize(w):
    w = '^' + w + '$'
    for i in range(2, len(w)):
        if threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]] == 0:
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
        if 0 < len(word) <= 20:
            wordCounter += 1
            characters[len(word)] += 1
            charCounter += len(word)
            analyze_n_grams(word)
            if len(word) == 1:
                singletons[0] += 1
                singletons[aDict[word]] += 1

wordsRemaining = wordCounter
wordsToCreate = 2*wordCounter

popularDict = {}
for i in range(3, len(twoGramMatrix)):
    for j in range(3, len(twoGramMatrix[i])):
        if twoGramMatrix[i][j] > charCounter/100:
            popularDict[alphabet[j] + alphabet[i]] = twoGramMatrix[i][j]/charCounter*100

for el in reversed(sorted(popularDict.items(), key=lambda x: x[1])):
    print(el)

popularDict3 = {}
for i in range(1, len(threeGramMatrix)):
    for j in range(1, len(threeGramMatrix[i])):
        for k in range(1, len(threeGramMatrix[j])):
            if threeGramMatrix[i][j][k] > charCounter/200:
                popularDict3[alphabet[k] + alphabet[j] + alphabet[i]] = threeGramMatrix[i][j][k]/charCounter*100

for el in reversed(sorted(popularDict3.items(), key=lambda x: x[1])):
    print(el)


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
    if l == 1:
        i = 3
        while r >= 0:
            r -= singletons[i]
            i += 1
        w = alphabet[i-1]
    else:
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
# print(characters)
# print(characters2)
print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print("Czas wykonywania: " + str(end - start) + "s")
