# Data Science Assignment#1
# 2022094093 Kim Dohoon, Dept. of Data Science
# Apriori Algorithm to find association rules
import sys, itertools

# Candidate Generating Function
def candidate(I: list, k: int):
    lst = set()
    for i in range(len(I)):
        for j in range(i+1, len(I)):
            if len(set(I[i]+I[j])) == k:
                cand = tuple(sorted(set(I[i]+I[j])))
                lst.add(cand)
    return lst

# Apriori
def apriori(DB, min_sup):
    min_sup = min_sup * len(DB) / 100
    L = {}
    C = {}
    L[1] = {}
    for transaction in DB:
        item = {i : transaction.count(i) for i in transaction}
        for i in item.keys():
            if not L[1].get((i,)):
                L[1][(i,)] = 0
            L[1][(i,)] += 1
    ref = [i for i in L[1].keys()]

    k = 1
    while L[k]:
        Candidate = candidate(ref, k+1)
        C[k+1] = {}
        for transaction in DB:
            for c in Candidate:
                intersect = tuple(sorted(set(c).intersection(transaction)))
                if intersect == c:
                    if not C[k+1].get(intersect):
                        C[k+1][intersect] = 0
                    C[k+1][intersect] += 1
        L[k+1] = {i[0] : i[1] for i in C[k+1].items() if i[1]>=min_sup}
        ref = list(L[k+1].keys())
        k += 1
    l = {}
    for i in L.keys():
        l.update(L[i])
    return l

# Union operation from L_1 to L_k
def union(D):
    res = {}
    for key, value in D.items():
        flag = True
        for k in D.keys():
            if key!=k and set(key).issubset(k):
                flag = False
                break
        if flag:
            res[key] = value
    return res
        
# Calculate support and confidence
def supconf(D, ref, n):
    output = {}
    for key, cnt in D.items():
        for i in range(1, len(key)):
            for x in itertools.combinations(key, i):
                y = tuple(i for i in key if i not in x)
                if not output.get(x):
                    output[x] = {}
                if not output[x].get(y):
                    output[x][y] = 0
                output[x][y] += cnt
    for key in output.keys():
        for k in output[key].keys():
            output[key][k] *= 100
            output[key][k] = [output[key][k]/n, output[key][k]/ref[key]]
    return output

if __name__ == '__main__':
    min_support = int(sys.argv[1])  # Minimum support, %
    inputfile = sys.argv[2]  # Input file, .txt format
    outputfile = sys.argv[3]  # Output file, .txt format

    with open(inputfile, 'r') as f:
        DB = []
        for item in f.readlines():
            t = item.split('\t')
            for i in range(len(t)):
                t[i] = int(t[i])
            DB.append(t)

    result = apriori(DB, min_support)
    res = union(result)
    sc_table = supconf(res, result, len(DB))

    with open(outputfile, 'w') as f:
        for item_set in sc_table.keys():
            itemset = [str(i) for i in item_set]
            for associative_item_set, values in sc_table[item_set].items():
                associative_itemset = [str(i) for i in associative_item_set]
                string = "{" + ",".join(itemset) + "}\t{" + ",".join(associative_itemset) + "}\t" + f"{values[0]:.2f}\t{values[1]:.2f}\n"
                f.write(string)
