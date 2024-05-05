from itertools import combinations
import sys

def C_k(length, L_kminus1, minVal=0, maxVal=19):
    if(length == 1):
        candidateList = []

        for candidate in list(range(minVal, maxVal+1)):
            candidateList.append({candidate})
        return candidateList
    
    else:
        preCandidateList = []
        frozenL_kminus1 = []
        for _ in L_kminus1:
            frozenL_kminus1.append(frozenset(_))
        for c0 in L_kminus1:
            for c1 in L_kminus1:
                candidate = set(sorted(list(c0 | c1))) 
                # if(len(candidate) != length):
                #     continue
                # else:
                #     preCandidateList.append(candidate)
                
                if(len(candidate) != length):
                    continue
                
                subList = list(combinations(candidate, length-1))
                
                subset = []
                for i in range(len(subList)):
                    subset.append(set(subList[i]))
                # if(length == 6):
                #     print(candidate, length, subset)
                # for i in range(len(subset)):
                #     if(subset[i] not in L_kminus1):
                #         check = False
                #         break
                frozenSubSet = []
                for _ in subset:
                    frozenSubSet.append(frozenset(_))
                
                if(set(frozenSubSet) - set(frozenL_kminus1) == set() and candidate not in preCandidateList):
                    preCandidateList.append(candidate)

        return preCandidateList

def L_k(C_k, itemSetList, minimumSupport=0.05):
    frequentPatternList = []

    for candidiate in C_k:
        cnt = 0
        for itemSet in itemSetList:
            # print(candidiate, itemSet)
            if(candidiate & itemSet == candidiate):
                cnt = cnt+1
        # print(candidiate, cnt, len(itemSetList)*minimumSupport)
        if(cnt >= len(itemSetList)*minimumSupport):
            frequentPatternList.append(candidiate)
    
    return frequentPatternList

if __name__ == '__main__':

    minimum = float(sys.argv[1])/100
    inputFile = sys.argv[2]
    outputFile = sys.argv[3]

    r = open(inputFile, 'r')
    w = open(outputFile, 'w')

    itemSetList = []

    while True:
        line = r.readline()

        if not line: break

        splittedLine = line.split('\t')

        itemSet = []
        for i in range(len(splittedLine)):
            itemSet.append(int(splittedLine[i].replace('\n', '')))
        
        itemSetList.append(set(itemSet))

    # for i in range(len(itemSetSet)):
    #     print(itemSetSet[i])

    maxVal = max(map(max, itemSetList))
    minVal = min(map(min, itemSetList))

    print(minVal, maxVal)

    Lkminus1 = []
    # lKCount = 0
    for k in range(1, maxVal-minVal+2):
        Ck = C_k(k, Lkminus1, minVal, maxVal)
        # print(Ck)

        Lk = L_k(Ck, itemSetList, minimum)
        # print(Lk)
        
        for itemSet in Lk:
            assoRuleList = []

            for i in range(1, len(itemSet)):
                assoRuleList = assoRuleList+list(combinations(itemSet,i))

            for i in range(len(assoRuleList)):
                assoRuleList[i] = set(assoRuleList[i])

            for i in range(len(assoRuleList)):
                support = 0
                for rawItemSet in itemSetList:
                    # print(candidiate, itemSet)
                    if(itemSet & rawItemSet == itemSet):
                        support = support+1
                # support = support/len(itemSetList)*100

                confidence = 0
                for rawItemSet in itemSetList:
                    # print(candidiate, itemSet)
                    if(assoRuleList[i] & rawItemSet == assoRuleList[i]):
                        confidence = confidence+1
                # confidence = confidence/support*100

                # print(str(assoRuleList[i]) + '\t' + str(itemSet-assoRuleList[i]) + '\t' + str(format(support/len(itemSetList)*100, ".2f") + '\t' + str(format(support/confidence*100, ".2f"))))
                w.write(str(assoRuleList[i]).replace(' ', '') + '\t' + str(itemSet-assoRuleList[i]).replace(' ', '') + '\t' + str(format(support/len(itemSetList)*100, ".2f")) + '\t' + str(format(support/confidence*100, ".2f")) + '\n')
                # w.write('%s\t%s\t%0.2f\t%0.2f\n' % (str(assoRuleList[i]) , str(itemSet-assoRuleList[i]), support/len(itemSetList)*100, support/confidence*100))
        # lKCount = lKCount+len(Lk)
        # print(Lk)
        # print(k, len(Lk))
        print(k, "len(Lk)", len(Lk))
        if(len(Lk) <= 1):
            break
        Lkminus1 = Ck

    # Ck = C_k(1, Lkminus1)
    # print(Ck)

    # Lk = L_k(Ck, itemSetList)
    # lKCount = lKCount+len(Lk)
    # print(Lk)

    # Ckminus1 = Ck

    # Ck = C_k(2, Lk)
    # print(Ck)

    # Lk = L_k(Ck, itemSetList)
    # lKCount = lKCount+len(Lk)
    # print(Lk)
    # print(lKCount)
    r.close()
    w.close()