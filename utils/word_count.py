"""How many words in a dataset"""

import pandas as pd
import os


def count(text):
    return len(str(text).split())


def sum_col(col):
    return col.dropna().apply(count).sum()


def count_dataset(folder, columns):
    words = 0
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        df = pd.read_csv(file)
        for col in columns:
            words += sum_col(df[col])
    return words


def boolq(folder):
    columns = ['question', 'passage']
    return count_dataset(folder, columns)


def cb(folder):
    columns = ['premise', 'hypothesis']
    return count_dataset(folder, columns)


def copa(folder):
    columns = ['premise', 'choice1', 'choice2']
    return count_dataset(folder, columns)


def rte(folder):
    columns = ['premise', 'hypothesis']
    return count_dataset(folder, columns)


def wic(folder):
    columns = ['word', 'sentence1', 'sentence2']
    return count_dataset(folder, columns)


def wsc(folder):
    columns = ['text']
    return count_dataset(folder, columns)


def multirc(folder):
    words = 0
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        df = pd.read_csv(file)
        df_filtered = df.filter(regex='text|passage.questions.[0-9]*.question')
        columns = list(df_filtered)
        for col in columns:
            words += sum_col(df[col])
    return words


def record(folder):
    words = 0
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        df = pd.read_csv(file, low_memory=False)
        df_filtered = df.filter(regex='text|query')
        columns = list(df_filtered)
        for col in columns:
            words += sum_col(df[col])
    return words


source = 'combined-csv-eng'
print('BoolQ:', boolq(f'{source}/BoolQ'))
print('CB:', cb(f'{source}/CB'))
print('COPA:', copa(f'{source}/COPA'))
print('RTE:', rte(f'{source}/RTE'))
print('WiC:', wic(f'{source}/WiC'))
print('WSC:', wsc(f'{source}/WSC'))
print('MultiRC:', multirc(f'{source}/MultiRC'))
print('ReCoRD:', record(f'{source}/ReCoRD'))
