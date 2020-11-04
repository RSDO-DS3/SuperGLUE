import jsonlines
import pandas as pd
import os
from collections import defaultdict
import numpy as np


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def jsonl2csv(json_eng, csv_eng):
    # todo you can rewrite this function with pandas (check pandas.json_normalize)
    nested_datasets = ['MultiRC', 'WSC', 'ReCoRD']

    for file in os.listdir(json_eng):
        file_json = os.path.join(json_eng, file)
        os.makedirs(os.path.join(csv_eng), exist_ok=True)

        with jsonlines.open(file_json) as reader:
            D = defaultdict(list)
            l = []
            for idx, dic in enumerate(reader):
                if idx % 10000 == 0 and idx != 0:  # monitor large datasets
                    print(idx, file_json)
                if file_json.split('/')[-2] in nested_datasets:
                    dic = flatten_json(dic)
                l.append((dic, idx))

            # build all keys
            for idx, d in enumerate(l):
                for key in d[0].keys():
                    D[key] = []

            # populate keys
            for idx, d in enumerate(l):
                d = d[0]
                for key in D.keys():
                    if key in d:
                        D[key].append(d[key])
                    else:
                        D[key].append(np.nan)

            df = pd.DataFrame(D, index=list(range(idx+1)))
            df.to_csv(os.path.join(csv_eng, file.split('.')[0] + '.csv'), index=False)


for dataset in os.listdir('combined-json-eng'):
    print(dataset)
    json_eng = os.path.join('combined-json-eng', dataset)
    csv_eng = os.path.join('combined-csv-eng', dataset)
    jsonl2csv(json_eng, csv_eng)