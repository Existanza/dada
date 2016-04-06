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


alphabet = 'aąbcćdeęfghijklłmnńopóqrsśtuvwxyzźż'
alphabetDict = {ch: i for ch, i in zip(alphabet, range(1, len(alphabet)+1))}
nGramMatrix = [[0]*50 for i in range(50)]
syllables = [0]*20
syllableCounter = 0
words = [0]*50
wordCounter = 0


def analyze_n_grams(w):
    alphabetDict[w[len(w)-1]][0] += 1
    for i in range(len(w), 1, -1):
        print(w[i])


def analyze_syllables(w):
    print(w)


def generate_word():
    w = 'hehe'
    return w


def generate_sentence(n):
    w = "hehehe"
    return w


for line in inputFile:
    wordsInSentenceCounter = 0
    for word in line.split():
        wordsInSentenceCounter += 1
        wordCounter += 1
        analyze_n_grams(word)
        analyze_syllables(word[::-1])
    words[wordsInSentenceCounter] += 1


wordsRemaining = wordCounter
while wordsRemaining > 0:
    n = 1
    outputFile.write(generate_sentence(n)+'\n')

inputFile.close()
outputFile.close()
