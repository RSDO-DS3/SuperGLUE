import argparse

import pandas as pd
import os
from collections import defaultdict
import re
import numpy as np


def make_dirs(root, tasks):
    for task in tasks:
        os.makedirs(os.path.join(root, task), exist_ok=True)


def test_all(org_folder, rev_folder):
    for task in os.listdir(rev_folder):
        for file in os.listdir(os.path.join(rev_folder, task)):
            org_file = pd.read_csv(os.path.join(org_folder, task, file), low_memory=False)
            org_file = org_file.reindex(sorted(org_file.columns), axis=1)
            rev_file = pd.read_csv(os.path.join(rev_folder, task, file), low_memory=False)
            rev_file = rev_file.reindex(sorted(rev_file.columns), axis=1)

            # if org_file.equals(rev_file):
            #     print(f'{task:10}{file:15}OK')
            # else:
            #     print(f'{task:10}{file:15}FAIL')

            if org_file.equals(rev_file):  # equals fails if two entries are of a different dtype
                print(f'{task:10}{file:15}OK')
            else:
                # important: inspect failed files manually and report
                # COPA (no real difference)
                # MUltirc (no real difference)
                # Record (no difference)
                # WSC (some mistakes, mainly with upper-lower letters)
                df_diff = pd.concat([org_file, rev_file]).drop_duplicates(keep=False)
                df_diff.sort_values('idx', inplace=True)
                print(f'{task:10}{file:15}{"FAIL": <10}{str(len(df_diff) // 2): <10}{"files"}')


def txt2csv_group(task_path, save_path):
    for task in os.listdir(task_path):
        files = []

        for file in os.listdir(os.path.join(task_path, task)):
            # print(file, task)
            with open(os.path.join(task_path, task, file), 'r', encoding='utf-8') as f:  # todo check encoding
                d = {}
                for line in f.readlines():
                    key, value = line.split(':', 1)
                    d[key.lower().strip()] = value.strip()

            files.append(d)

        D = defaultdict(list)
        for d in files:
            for key, value in d.items():
                D[key].append(value)

        print(task)
        df = pd.DataFrame(D, index=list(range(len(files))))
        df['idx'] = df['idx'].astype(int)
        df.sort_values('idx', inplace=True)
        df.to_csv(os.path.join(save_path, task + '.csv'), index=False)


def txt2csv_wsc(task_path, save_path):
    for task in os.listdir(task_path):
        files = []

        for file in os.listdir(os.path.join(task_path, task)):
            with open(os.path.join(task_path, task, file), 'r', encoding='utf-8-sig') as f:
                d = {}
                for line in f.readlines():
                    key, value = line.split(':', 1)

                    try:
                        if key == 'text' and file == '95.txt':  # Sample with mistakes (in english dataset), check it
                            d['target.span1_text'] = False
                            d['target.span2_text'] = False
                            d['target.span1_index'] = False
                            d['target.span2_index'] = False
                            d['text'] = False

                        elif key == 'text' and file == '392.txt':  # Sample with mistakes (in english dataset), check it
                            d['target.span1_text'] = False
                            d['target.span2_text'] = False
                            d['target.span1_index'] = False
                            d['target.span2_index'] = False
                            d['text'] = False

                        if key == 'text':
                            d['target.span1_text'] = re.findall('<w1> (.+?) <\/w1>', value)[0]
                            d['target.span2_text'] = re.findall('<w2> (.+?) <\/w2>', value)[0]
                            d['target.span1_index'] = value.split().index('<w1>')
                            d['target.span2_index'] = value.split().index('<w2>') - 2
                            text = re.sub('<.+?>', '', value).strip().replace('  ', ' ')
                            d['text'] = text
                            # d['text'] = re.sub('<.+?>', '', value.strip())

                        else:
                            d[key] = value.strip()

                    except IndexError:
                        print(f'{task},{file}')
            files.append(d)

        D = defaultdict(list)
        for d in files:
            for key, value in d.items():
                D[key].append(value)

        df = pd.DataFrame(D, index=list(range(len(files))))
        df['idx'] = df['idx'].astype(int)
        df.sort_values('idx', inplace=True)
        df.to_csv(os.path.join(save_path, task + '.csv'), index=False)


def txt2csv_multirc(task_path, save_path):
    for task in os.listdir(task_path):
        files = []

        for file in os.listdir(os.path.join(task_path, task)):
            with open(os.path.join(task_path, task, file), 'r') as f:
                d = {}
                for line in f.readlines():
                    key, value = line.split(':', 1)
                    d[key] = value.strip()
            files.append(d)

        D = defaultdict(list)

        # build all the keys
        for idx, d in enumerate(files):
            for key in d.keys():
                D[key] = []

        # populate keys
        for d in files:
            for key in D.keys():
                if key in d.keys():
                    D[key].append(d[key])
                else:
                    D[key].append(np.nan)


        df = pd.DataFrame(D, index=list(range(len(files))))
        df['idx'] = df['idx'].astype(int)
        df.sort_values('idx', inplace=True)
        df.to_csv(os.path.join(save_path, task + '.csv'), index=False)


def simplify_record_key_reverse(key):
    key = key[1:-1].split('.')  # remove brackets
    if '/q' in key[0]:
        return f'qas.{key[1]}.answers.{key[3]}.end'
    elif 'q' in key[0]:
        return f'qas.{key[1]}.answers.{key[3]}.start'
    elif '/e' in key[0]:
        return f'passage.entities.{key[1]}.end'
    else:
        return f'passage.entities.{key[1]}.start'


def txt2csv_record(task_path, save_path):
    for task in os.listdir(task_path):
        files = []

        for file in os.listdir(os.path.join(task_path, task)):
            with open(os.path.join(task_path, task, file), 'r') as f:
                d = {}
                for line in f.readlines():
                    key, value = line.split(':', 1)
                    if key in ['source', 'idx']:
                        d[key] = value.strip()
                    elif key == 'passage.text':
                        text = value
                        tags = re.findall('<.+?>', text)
                        tag_idx = {}
                        for tag in tags:
                            try:
                                idx = text.index(tag)
                            except ValueError:  # files 479 and 19 (validation set) were manually repaired
                                print(f'{task:10}{file:15} --> wrong indices!')
                            if '/' in tag:
                                tag_idx[tag] = idx - 1
                            else:
                                tag_idx[tag] = idx
                            text = text.replace(tag, '')

                        for tag, value in tag_idx.items():
                            tag_reversed = simplify_record_key_reverse(tag)
                            d[tag_reversed] = value

                        d['passage.text'] = text.strip().replace(' @highlight ', '\n@highlight\n')
                    else:
                        d[key] = value.strip()
            files.append(d)

        D = defaultdict(list)

        # build all the keys
        for idx, d in enumerate(files):
            for key in d.keys():
                D[key] = []

        # populate keys
        for d in files:
            for key in D.keys():
                if key in d.keys():
                    D[key].append(d[key])
                else:
                    D[key].append(np.nan)

        df = pd.DataFrame(D, index=list(range(len(files))))
        df['idx'] = df['idx'].astype(int)
        df.sort_values('idx', inplace=True)
        df.to_csv(os.path.join(save_path, task + '.csv'), index=False)


if __name__ == '__main__':
    # important WSC and ReCoRD datasets contain mistakes as ORIGINAL datasets:

    parser = argparse.ArgumentParser(
        description='Format conversion tool'
    )

    parser.add_argument('--txt', required=True)
    parser.add_argument('--csv', required=True)

    args = parser.parse_args()

    # variables
    TXT = args.txt
    CSV = args.csv

    # create empty directories
    TASKS = ['CB', 'COPA', 'MultiRC', 'ReCoRD', 'RTE', 'WSC']
    make_dirs(CSV, TASKS)

    # Group: no nesting, no indices, no NA values
    group = ['CB', 'COPA', 'RTE', 'BoolQ']
    for dataset in group:
        print(dataset)
        txt_eng = os.path.join(TXT, dataset)
        csv_eng = os.path.join(CSV, dataset)
        txt2csv_group(txt_eng, csv_eng)

    # each file has a specific format
    txt2csv_wsc(f'{TXT}/WSC', f'{CSV}/WSC')
    txt2csv_multirc(f'{TXT}/MultiRC', f'{CSV}/MultiRC')
    txt2csv_record(f'{TXT}/ReCoRD', f'{CSV}/ReCoRD')

    # only if you have preexisting csv files
    # test_all('combined-csv-eng', 'combined-csv-eng-reverse')
