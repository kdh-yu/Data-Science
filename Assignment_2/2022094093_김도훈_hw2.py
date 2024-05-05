import sys
from math import log2
             
def Info(D: list):
    if D:
        class_cnt = {}
        entropy = 0
        l = len(D)
        for data in D:
            if data[-1] not in class_cnt:
                class_cnt[data[-1]] = 0
            class_cnt[data[-1]] += 1
        for cnt in class_cnt.values():
            if not cnt:
                continue
            entropy -= (cnt/l) * log2(cnt/l)
        return entropy
    
def InfoA(D: dict, dlen: int):
    if D:
        entropy = 0
        for j in D.keys():
            entropy += (len(D[j]) / dlen) * Info(D[j])
        return entropy

def SplitInfo(D: list, Ds: dict):
    sinfo = 0
    for v in Ds.values():
        if v != 0:
            sinfo -= (len(v)/len(D)) * log2(len(v)/len(D))
    return sinfo
    
def selectFeature(feature: list, data: list, flagidx=0):
    InfoGain = []
    TreeTemp = []
    for f in range(len(feature)):
        # Divide
        temp = {}
        for d in data:
            if d[f] not in temp:
                temp[d[f]] = []
            temp[d[f]].append(d)
        sinfo = SplitInfo(data, temp)
        if sinfo == 0:
            gain = 0
        else:
            gain = (Info(data) - InfoA(temp, len(data))) / SplitInfo(data, temp)
        InfoGain.append(gain)
        TreeTemp.append(temp)
    feature_index = InfoGain.index(max(InfoGain))
    flag = (max(InfoGain) == 0)
    if flagidx:
        return InfoGain, TreeTemp
    return feature_index, TreeTemp[feature_index], flag
    
def build_tree(T: dict, feature: list, data: list):
    feature_idx, tree, flag = selectFeature(feature, data)
    if flag:
        return data[0][-1]
    T['feature'] = feature[feature_idx]
    t = {}
    for k, v in tree.items():
        t[k] = build_tree({}, feature, v)
    T['split'] = t
    return T

def predict(T: dict, feature: list, data: list):
    if type(T) == str:
        return T
    idx = feature.index(T['feature'])
    try:
        return predict(T['split'][data[idx]], feature, data)
    except:
        f = list(T['split'].keys())[-1]
        return predict(T['split'][f], feature, data)

if __name__ == '__main__':
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    result_path = sys.argv[3]
    train = []
    flag = False
    with open(train_path, 'r') as f:
        for data in f.readlines():
            data = data.strip('\n').split('\t')
            if not flag:
                features = data
                flag = True
                continue
            train.append(data)
    T = build_tree({}, features[:-1], train)
    with open(result_path, 'w') as fr:
        fr.write('\t'.join(features))
        fr.write('\n')
        with open(test_path, 'r') as f:
            for data in f.readlines()[1:]:
                data = data.strip('\n').split('\t')
                prediction = predict(T, features, data)
                data.append(prediction)
                fr.write('\t'.join(data))
                fr.write('\n')
