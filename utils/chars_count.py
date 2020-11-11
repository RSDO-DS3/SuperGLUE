"""Calculate number of characters and estimate translation price for each dataset."""

import pandas as pd
import os


def count(text):
    return len(str(text))


def sum_col(col):
    return col.dropna().apply(count).sum()  # 83106


def count_dataset(folder, columns):
    chars = 0
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        df = pd.read_csv(file)
        for col in columns:
            chars += sum_col(df[col])
    return chars


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

bq_out = boolq(f'{source}/BoolQ')
print(f'BoolQ:{bq_out}', f'{round(bq_out*0.00002, 2)}$')

cb_out = cb(f'{source}/CB')
print(f'CB:{cb_out}', f'{round(cb_out*0.00002, 2)}$')

copa_out = copa(f'{source}/COPA')
print(f'COPA:{copa_out}', f'{round(copa_out*0.00002, 2)}$')

rte_out = rte(f'{source}/RTE')
print(f'RTE:{rte_out}', f'{round(rte_out*0.00002, 2)}$')

# print(f'WiC:', wic(f'{source}/WiC'))

wsc_out = wsc(f'{source}/WSC')
print(f'WSC:{wsc_out}', f'{round(wsc_out*0.00002, 2)}$')

multirc_out = multirc(f'{source}/MultiRC')
print(f'MultiRC:{multirc_out}', f'{round(multirc_out*0.00002, 2)}$')

record_out = record(f'{source}/ReCoRD')
print(f'ReCoRD:{record_out}', f'{round(record_out*0.00002, 2)}$')
