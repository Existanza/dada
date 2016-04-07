# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

import sys
import random

if len(sys.argv) < 3:
    sys.exit("Error: the input and output files weren't provided.\n"
             "Example: python3 dd.py input.txt output.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'a')
except OSError as err:
    sys.exit("OS error: {0}".format(err))


alphabetSize = 50
alphabet = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
alphabetList = [c for c in alphabet]
capitals = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
alphabetDict = {ch: i for ch, i in zip(alphabet, range(1, len(alphabet)+1))}
vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
diphthongs = {'au', 'eu', 'ia', 'ią', 'ie', 'ię', 'io', 'iu'}
nGramMatrix = [[0]*alphabetSize for i in range(alphabetSize)]
nGramList = [0]*alphabetSize
endings = [0]*alphabetSize
syllables = [0]*20
syllableCounter = 0
characters = [0]*25
charCounter = 0
wordCounter = 0


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList:
            nw += w[i]
        elif w[i] in capitalsList:
            nw += toSmallDict[w[i]]
    # print(nw)
    return nw


def analyze_n_grams(w):
    endings[alphabetDict[w[len(w)-1]]] += 1
    for i in range(1, len(w)):
        nGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i-1]]] += 1
        # print(w[i] + ' ' + w[i-1])


def analyze_syllables(w):
    s = 0
    for i in range(len(w)):
        if (w[i] in vowels) and (i == len(w)-1 or (not w[i:i+2] in diphthongs)):
            s += 1
    syllables[s] += 1
    # print(str(s) + ' ' + w)
    return s


def generate_word(l):
    r = random.randrange(1, charCounter)
    s = 0
    i = 0
    while s < r:
        s += endings[i]
        i += 1
    w = alphabet[i-1]
    for i in range(1, len(l)):
        #TODO
        print(' ')
    return w


normalize_word('Sroka.')
normalize_word('ChuJ!!111')
normalize_word('GŻEGżółKA!@@@!111')
analyze_n_grams('pokiereszowany')
analyze_syllables('pokiereszowany')
analyze_syllables('kier')
analyze_syllables('ciało')
analyze_syllables('ogień')
analyze_syllables('gar')
analyze_syllables('naiwny')
analyze_syllables('korci')

# '''
for line in inputFile:
    for word in line.split():
        wordCounter += 1
        word = normalize_word(word)
        characters[len(word)] += 1
        charCounter += len(word)
        analyze_n_grams(word)
        syllableCounter += analyze_syllables(word[::-1])


for i in range(alphabetSize):
    for j in range(alphabetSize):
        print(' ')


wordsRemaining = wordCounter

while wordsRemaining > 0:
    r = random.randrange(1, wordCounter)
    l = 0
    s = 0
    while s < r:
        s += characters[l]
        l += 1
    outputFile.write(generate_word(l-1) + ' ')
    wordsRemaining -= 1
# '''
inputFile.close()
outputFile.close()
