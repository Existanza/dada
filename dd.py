# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

# TODO - naprawic generate_by_syllables

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
    # inputFile = open("pride.txt", 'r')
    # outputFile = open("prideout.txt", 'w')
    # inputFile = open("padeusz.txt", 'r')
    # outputFile = open("pad5.txt", 'w')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

generate_by_default = False
generate_by_characters = False
generate_by_syllables = False
thorough_generate = True
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
wordOccurrences = {}
charOccurrences = {l: 0 for l in alphabet}
originalBeginningsOccurrences = {l: 0 for l in alphabet}
processedBeginningsOccurrences = {l: 0 for l in alphabet}
startingConsonants = [0]*20
syllables = [0]*25
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


def analyze_syllables(w):
    s = 0
    c = 0
    for i in range(len(w)):
        if (w[i] in vowels) and (i == len(w)-1 or (not w[i:i+2] in diphthongs)):
            s += 1
        elif s == 0:
            c += 1
    syllables[s] += 1
    startingConsonants[c] += 1
    # print(str(s) + ' ' + w)


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


def generate_word():
    w = "$"
    while w[0] is not "^":
        w = complete_bigram(w[0]) + w
    for i in range(1, len(w)-3):
        if not threeGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i+1]]][alphabetDict[w[i+2]]]:
            return generate_word()
    return w[1:-1]


def generate_word_by_syllables(s):
    w = generate_letter()
    i = 0
    while i < s:
        if w[0] in vowels and (len(w) < 2 or not w[0:2] in diphthongs):
            i += 1
        w = complete_bigram(w[0]) + w
    r = max(1, random.randrange(wordCounter+1))
    s = 0
    i = 0
    while s < r:
        s += startingConsonants[i]
        i += 1
    i -= 1
    for j in range(i):
        cb = complete_bigram(w[0])
        if cb in vowels:
            j -= 1
        else:
            w = cb + w
    # print(w)
    return w


def sanitize(w):
    sanitizeAttempts[0] += 1
    if w[0] != '^':
        w = '^' + w + '$'
    for i in range(2, len(w)):
        if not threeGramMatrix[alphabetDict[w[i]]][alphabetDict[w[i - 1]]][alphabetDict[w[i - 2]]]:
            return False
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
            originalBeginningsOccurrences[word[0]] += 1
            for i in range(len(word)):
                charOccurrences[word[i]] += 1
            if word in wordOccurrences:
                wordOccurrences[word] += 1
            else:
                wordOccurrences[word] = 1
            wordCounter += 1
            characters[len(word)] += 1
            charCounter += len(word)
            analyze_n_grams(word)
            analyze_syllables(word)

'''
wordList = sorted(wordOccurrences.items(), key=lambda x: x[1])
charList = sorted(charOccurrences.items())
for i in charList:
    if i[1] is not 0:
        print(str(i[0]) + ": " + str(i[1]/charCounter*100) + "%")
print()
'''
# print(wordList[:-50:-1])

wordsRemaining = wordCounter

# print(startingConsonants)
# print(syllables)
# for r in twoGramMatrix:
#     print(r)

# print(characters)

while wordsRemaining > 0:
    if generate_by_default:
        outputFile.write(generate_word() + ' ')
    else:
        r = max(1, random.randrange(wordCounter + 1))
        l = 0
        s = 0
        while s < r:
            s = s + syllables[l] if generate_by_syllables else s + characters[l]
            l += 1
        if generate_by_characters:
            l = min(l, 21)
            w = generate_word_by_characters(l-1)
            while not sanitize(w):
                w = generate_word_by_characters(l - 1)
            processedBeginningsOccurrences[w[0]] += 1
            # if len(w) >= 15:
            #     print(str(len(w)) + ' ' + w)
            outputFile.write(w + ' ')
        elif thorough_generate:
            l = min(l, 21)
            w = thorough_generate_word(l-1)
            while not sanitize(w):
                w = thorough_generate_word(l-1)
            processedBeginningsOccurrences[w[0]] += 1
            # if len(w) >= 15:
            #     print(str(len(w)) + ' ' + w)
            if wordsRemaining % 1000 == 0:
                print(wordsRemaining)
            # print(str(wordsRemaining) + '  ' + str(l) + '  ' + w)
            outputFile.write(w + ' ')
        elif generate_by_syllables:
            outputFile.write(generate_word_by_syllables(l - 1) + ' ')
    if (wordCounter - wordsRemaining) % 10 == 9:
        outputFile.write('\n')
    wordsRemaining -= 1

print()
charList2 = sorted(originalBeginningsOccurrences.items())
charList3 = sorted(processedBeginningsOccurrences.items())
for i, j in zip(charList2, charList3):
    if i[1] or j[1] is not 0:
        print(str(i[0]) + ": " + str(i[1]/wordCounter*100) + "%" + "   " + str(j[1]/wordCounter*100) + "%")

inputFile.close()
outputFile.close()

end = time.clock()

print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print(str(sanitizeAttempts[0]) + " razy sanitize uruchomionych")
print("Czas wykonywania: " + str(end - start) + "s")
