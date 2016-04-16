import random
import sys
import time
from bisect import bisect_left, insort

aSize = 50
alphabet = '+^$aeiouybcdfghjklmnpqrstvwxząćęłńóśźżäöüßšžõ'
alphabetList = [c for c in alphabet]
capitals = '+^$AEIOUYBCDFGHJKLMNPQRSTVWXZĄĆĘŁŃÓŚŹŻÄÖÜẞŠŽÕ'
capitalsList = [c for c in capitals]
toSmallDict = {c: s for c, s in zip(capitals, alphabet)}
aDict = {ch: i for ch, i in zip(alphabet, range(len(alphabet) + 1))}
twoGramMatrix = [[0] * aSize for i in range(aSize)]
threeGramMatrix = [[[0] * aSize for i in range(aSize)] for j in range(aSize)]
fDict = {}
characters = [0] * 21
characters2 = [0] * 21
singletons = [0] * aSize
words = [[""] for i in range(21)]
sanitizeAttempts = [0]
charCounter = 0
wordCounter = 0
inputList = []
outputList = []
dictList = []
