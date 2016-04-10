# Author: Existanza

#TODO: wypisac proporcje slow istniejacych zaleznie od ich dlugosci

import sys
import time

start = time.clock()

if len(sys.argv) < 3:
    sys.exit("Error: the input and dictionary files weren't provided.\n"
             "Example: python3 dd.py input.txt dictionary.txt")
try:
    inputFile = open(sys.argv[1], 'r')
    dictionary = open(sys.argv[2], 'r')
except OSError as err:
    sys.exit("OS error: {0}".format(err))

alphabet = '+^$aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
alphabetList = [c for c in alphabet]
capitals = '+^$AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
inputList = []
dictList = []


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


for line in inputFile:
    for word in line.split():
        word = normalize_word(word)
        if len(word) > 0:
            inputList.append(word)
inputFile.close()

for line in dictionary:
    for word in line.split():
        dictList.append(word)
dictionary.close()

wordsInDict = 0
wordsTotal = len(inputList)

counter = 0

for word in inputList:
    counter += 1
    if word in dictList:
        # print(word)
        wordsInDict += 1
    if counter % 1000 == 0:
        print(str(counter) + " / " + str(wordsTotal))

print(str(wordsInDict/wordsTotal*100) + "%")

end = time.clock()

print("Czas wykonywania: " + str(end - start) + "s")
