import sys
from collections import deque

def dist(p1, p2):
    d = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    return d**0.5

def RangeQuery(DB, point, eps):
    neighbors = deque()
    for pts, ploc in DB:
        if dist(point, ploc) < eps:
            neighbors.append(pts)
    return neighbors

def DBSCAN(DB, eps, minPts):
    c = 0
    label = [None]*len(DB)
    for p, pc in DB:
        if label[p] is not None:
            continue
        neighbors = RangeQuery(DB, pc, eps)
        neighbors.remove(p)
        if len(neighbors) < minPts:
            label[p] = 'Noise'
            continue
        label[p] = c
        S = neighbors.copy()
        t = 0
        while t < len(S):
            q = S[t]
            if label[q] == 'Noise':
                label[q] = c
            if label[q] is None:
                label[q] = c
                N = RangeQuery(DB, DB[q][1], eps)
                N.remove(DB[q][0])
                if len(N) >= minPts:
                    for ngb in N:
                        if ngb not in S:
                            S.append(ngb)
            t += 1
        c += 1
    return label

if __name__ == '__main__':
    file = sys.argv[1]
    n = int(sys.argv[2])
    eps = int(sys.argv[3])
    minpts = int(sys.argv[4])
    DB = []
    with open(file, 'r') as f:
        for data_ in f.readlines():
            data = data_.strip('\n').split('\t')
            pid, px, py = int(data[0]), float(data[1]), float(data[2])
            DB.append([pid, [px, py]])
    clusters = {i : deque() for i in range(n)}
    cluster = DBSCAN(DB, eps, minpts)
    groups = {}
    for idx, group in enumerate(cluster):
        if not groups.get(group):
            groups[group] = deque()
        groups[group].append(idx)
    for k in groups.keys():
        if k == 'Noise': continue
        with open(f"{file.strip('.txt')}_cluster_{k}.txt", 'w') as f:
            for item in groups[k]:
                f.write(f"{item}\n")