from memory import *


def normalize_word(w):
    nw = ''
    for i in range(len(w)):
        if w[i] in alphabetList and w[i] is not ("+" or "^" or "$"):
            nw += w[i]
        elif w[i] in capitalsList and w[i] is not ("+" or "^" or "$"):
            nw += toSmallDict[w[i]]
    return nw


def analyze_n_grams(w): #fDict
    w = "^" + w + "$"
    twoGramMatrix[aDict[w[1]]][aDict[w[0]]] += 1
    twoGramMatrix[aDict[w[1]]][0] += 1
    for i in range(2, len(w)):
        twoGramMatrix[aDict[w[i]]][aDict[w[i - 1]]] += 1
        twoGramMatrix[aDict[w[i]]][0] += 1
        threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][aDict[w[i - 2]]] += 1
        threeGramMatrix[aDict[w[i]]][aDict[w[i - 1]]][0] += 1


def complete_ngram(w):  #fDict
    r = max(1, random.randrange(twoGramMatrix[aDict[ch]][0] + 1))
    s = 0
    i = 1
    while s < r:
        s += twoGramMatrix[aDict[ch]][i]
        i += 1
    return alphabet[i - 1]


def sanitized(w):
    w = '^' + w + '$'
    if len(w) == 2 and threeGramMatrix[aDict[w[2]]][aDict[w[1]]][aDict[w[0]]] == 0:
        return True
    for i in range(2, len(w)):
        if threeGramMatrix[aDict[w[i]]][aDict[w[i-1]]][aDict[w[i-2]]] == 0:
            return False
    return True


def generate_word():
    w = "$"
    while w[0] is not "^":
        w = complete_ngram(w) + w
    return w[1:-1]


def printf(w):
    print(w, end=' ')
    sys.stdout.flush()


def find(sortedList, w):
    i = bisect_left(sortedList, w)
    if i != len(sortedList) and sortedList[i] == w:
        return True
    return False
