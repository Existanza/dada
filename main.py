# -*- coding: utf-8 -*-
# Author: Existanza
# sys.version
# 3.4.3 (default, Oct 14 2015, 20:28:29)
# [GCC 4.8.4]

# TODO: n-grams

from methods import *
from memory import *

start = time.clock()

if len(sys.argv) < 4:
    sys.exit("Error: the input, output and dictionary files weren't provided.\n"
             "Example: python3 main.py input.txt output.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], 'w')
    dictFile = open(sys.argv[3], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

print("Parsing input...")

for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if 0 < len(word) <= 20:
            wordCounter += 1
            characters[len(word)] += 1
            charCounter += len(word)
            analyze_n_grams(word)
            if not find(inputList, word):
                insort(inputList, word)
            if len(word) == 1:
                singletons[0] += 1
                singletons[aDict[word]] += 1
inputFile.close()

for line in dictFile:
    for word in line.split():
        if 20 >= len(word) > 0:
            dictList.append(word)
dictFile.close()

wordsRemaining = wordCounter
wordsToCreate = 2*wordCounter

printf("Creating words")

while wordsToCreate > 0:
    if wordsToCreate % int(wordCounter/5) == 0 and wordCounter != wordsToCreate:
        printf(".")
    w = generate_word()
    while not sanitized(w):
        w = generate_word()
    outputList.append(w)
    words[len(w)].append(w)
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

outputFile.close()

wordsInDict = 0
neologismsInDict = 0
inputLengthsList = [0]*21
dictLengthsList = [0]*21
neologismsLengthsList = [0]*21

for word in inputList:
    inputLengthsList[len(word)] += 1
    if find(dictList, word):
        wordsInDict += 1
        dictLengthsList[len(word)] += 1

dictLengthsList = [0]*21

for word in outputList:
    neologismsLengthsList[len(word)] += 1
    if find(dictList, word):
        neologismsInDict += 1
        neologismsLengthsList[len(word)] += 1

print("\nWORDS\n")

percentageList = [0 if dictLengthsList[i] == 0 else dictLengthsList[i]/inputLengthsList[i]*100 for i in range(21)]

for i in range(len(percentageList)):
    print(str(i) + " letter(s): " + str(dictLengthsList[i]) + " / " + str(inputLengthsList[i]) + " (" + str(percentageList[i]) + "%)")

print(str(wordsInDict/wordCounter*100) + "%")
print("of words exist in dictionary.")

print("\nNEOLOGISMS\n")

percentageList = [0 if neologismsLengthsList[i] == 0 else dictLengthsList[i]/neologismsLengthsList[i]*100 for i in range(21)]

for i in range(len(percentageList)):
    print(str(i) + " letter(s): " + str(dictLengthsList[i]) + " / " + str(neologismsLengthsList[i]) + " (" + str(percentageList[i]) + "%)")

print(str(neologismsInDict/wordCounter*100) + "%")
print("of neologisms exist in dictionary.")

end = time.clock()

print()
print(str(wordCounter) + " slow przetworzonych")
print(str(charCounter) + " znakow przetworzonych")
print("Czas wykonywania: " + str(end - start) + "s")
