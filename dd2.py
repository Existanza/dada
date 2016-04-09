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

alphabetSize = 40
alphabet = '+^$aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
alphabetList = [c for c in alphabet]
capitals = '+^$AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
alphabetDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet)+1))}
vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
diphthongs = {'au', 'eu', 'ia', 'ią', 'ie', 'ię', 'io', 'iu'}
twoGramMatrix = [[0] * alphabetSize for i in range(alphabetSize)]
threeGramMatrix = [[[0]*alphabetSize for i in range(alphabetSize)] * alphabetSize for j in range(alphabetSize)]
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
    # print(nw)
    return nw


def analyze_n_grams(w):
    w = "^" + w + "$"
    twoGramMatrix[alphabetDict[w[1]]][alphabetDict[w[0]]] += 1
    twoGramMatrix[alphabetDict[w[1]]][0] += 1
    for i in range(2, len(w)):
        twoGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i - 1]]] += 1
        twoGramMatrix[alphabetDict[w[i]]][0] += 1
        threeGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i - 1]]][alphabetDict[w[i - 2]]] = True


def generate_letter():
    r = max(1, random.randrange(wordCounter+1))
    s = 0
    i = 3
    while s < r:
        s += twoGramMatrix[2][i]
        i += 1
    # print(str(r) + alphabet[i-1])
    return alphabet[i - 1]


def complete_bigram(ch):
    r = max(1, random.randrange(twoGramMatrix[alphabetDict[ch]][0] + 1))
    s = 0
    i = 1
    while s < r:
        s += twoGramMatrix[alphabetDict[ch]][i]
        i += 1
    # print(ch + ' -> ' + alphabet[i-1])
    return alphabet[i - 1]


def sanitize(w):
    sanitizeAttempts[0] += 1
    if w[0] != '^':
        w = '^' + w + '$'
    for i in range(2, len(w)):
        if not threeGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i - 1]]][alphabetDict[w[i - 2]]]:
            return False
    # print(w)
    return True


def generate_word_by_characters(l):
    w = generate_letter()
    for i in range(1, l):
        c = '^'
        while c == '^':
            c = complete_bigram(w[0])
        w = c + w
    # print(w)
    return w


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
    w = generate_word_by_characters(l-1)
    while not sanitize(w):
        w = generate_word_by_characters(l - 1)
    outputFile.write(w + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

inputFile.close()
outputFile.close()

end = time.clock()

print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print(str(sanitizeAttempts) + " razy sanitize uruchomionych")
print("Czas wykonywania: " + str(end - start) + "s")
