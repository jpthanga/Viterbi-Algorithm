import nltk
from nltk.corpus import brown
import numpy as np
from collections import Counter
from collections import defaultdict
from math import log
import time

stime = time.time()
sentences = np.array(brown.tagged_sents())
words = brown.tagged_words()
tokens,taged = zip(*words)

#
# firstdict = {}
# firstSum = len(sentences)
# for i in sentences:
#     x,y = i[0]
#     if y not in firstdict.keys():
#         firstdict[y] = 1
#     else:
#         firstdict[y] += 1
#
# for i in firstdict.keys():
#     firstdict[i] = firstdict[i]/firstSum

# total word count
total = len(words)

# preping corpus data
wordcount = Counter(tokens)
tokenTags = defaultdict(Counter)
for token, tag in words:
    tokenTags[token][tag] += 1

tagcount = Counter(taged)
for i in tagcount.keys():
    tagcount[i] = tagcount[i]/total

bgram = nltk.ngrams(taged,2)
tagtags = defaultdict(Counter)
for tag1, tag2 in bgram:
    tagtags[tag1][tag2] += 1


#viterbi implementation
trans = {}
StateProbs = {}
def viterbi(prior,transition,num):
    a = []
    trans[num] = []
    StateProbs[num+1] = []
    emmision = tokenTags[test[num]]
    wn =wordcount[test[num]]
    p = {}
    for ik,ii in emmision.items():
        #hold probs
        min = 100000
        for jk,ji in prior.items():
            if transition[jk][ik] != 0:
                if num==0:
                    prob = log((ii/wn),2)  + (log((transition[jk][ik]/(total-1)), 2))
                else:
                    prob = ji + log((ii/wn), 2) + (log((transition[jk][ik]/(total-1)), 2))
                trans[num].append([(jk,ik),prob])
                if min > prob:
                    min = prob
        p[ik] = min
        StateProbs[num+1].append([ik,min])
    return p

#sentence and test
test = ['Time','flies','like','an','arrow','.']
prev = viterbi(tagcount,tagtags,0)
for i in range(1,len(test)):
    prev = viterbi(prev,tagtags,i)

del trans[0]

prevP = 0
prev = ''
order = []

#backpropogation
for i in range(len(test)-1,-1,-1):
    if i == len(test)-1:
        min = 100000000
        for j in StateProbs[i+1]:
            if min > j[1]:
                prev = j[0]
                min = j[1]
                prevP = j[1]
        order.append(prev)
    else:
        for g in trans[i+1]:
            if prevP == g[1]:
                x,y = g[0]
                prev = x
                order.append(prev)
        for k in StateProbs[i+1]:
            if k[0] == prev:
                prevP = k[1]

#solution
sol = []
for i in reversed(order):
    sol.append(i)
print(sol)
print("--- %s seconds ---" % (time.time() - stime))