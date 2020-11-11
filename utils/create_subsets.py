"""Create subsets of datasets based on word count"""

import os
import shutil


def make_dirs(source, tasks, sub_folders):
    for task in tasks:
        for sf in sub_folders:
            os.makedirs(os.path.join(source, task, sf), exist_ok=True)


def copy_files(source_eng, target_eng, spt, file):
    original_eng = os.path.join(source_eng, spt, str(file) + '.txt')
    target_eng = os.path.join(target_eng, spt, str(file) + '.txt')
    shutil.copyfile(original_eng, target_eng)


def boolq_count_words(source, spt, file):
    columns = ['question', 'passage']
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        keyword, text = line.split(':', 1)
        if keyword in columns:
            file_text.append(text)
    text = " ".join(file_text)
    return len(text.split())


def create_boolq(source_eng, target_eng, size):
    words = 0
    ratios = (3, 1, 1)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += boolq_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += boolq_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += boolq_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('BoolQ:', words)
            print(tvt)
            break


def cb_count_words(source, spt, file):
    columns = ['premise', 'hypothesis']
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        keyword, text = line.split(':', 1)
        if keyword in columns:
            file_text.append(text)
    text = " ".join(file_text)
    return len(text.split())


def create_cb(source_eng, target_eng, size):
    words = 0
    ratios = (5, 1, 5)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += cb_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += cb_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += cb_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('CB:', words)
            print(tvt)
            break


def rte_count_words(source, spt, file):
    columns = ['premise', 'hypothesis']
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        keyword, text = line.split(':', 1)
        if keyword in columns:
            file_text.append(text)
    text = " ".join(file_text)
    return len(text.split())


def create_rte(source_eng, target_eng, size):
    words = 0
    ratios = (8, 1, 1)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += rte_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += rte_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += rte_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('RTE:', words)
            print(tvt)
            break


def wic_count_words(source, spt, file):
    columns = ['word', 'sentence1', 'sentence2']
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        keyword, text = line.split(':', 1)
        if keyword in columns:
            file_text.append(text)
    text = " ".join(file_text)
    return len(text.split())


def create_wic(source_eng, target_eng, size):
    words = 0
    ratios = (10, 1, 2)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += wic_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += wic_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += wic_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('WiC:', words)
            print(tvt)
            break


def multirc_count_words(source, spt, file):
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        file_text.append(line.split(':', 1)[1].rstrip())
    text = " ".join(file_text)
    return len(text.split())


def create_multirc(source_eng, target_eng, size):
    words = 0
    ratios = (5, 1, 2)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += multirc_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += multirc_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += multirc_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('MultiRC:', words)
            print(tvt)
            break


def record_count_words(source, spt, file):
    file_path = os.path.join(source, spt, str(file) + '.txt')
    file_text = []
    for line in open(file_path).readlines():
        entry = line.split(':', 1)[0].rstrip()
        if entry.endswith('text') or entry.endswith('query'):
            file_text.append(line.split(':', 1)[1].rstrip())
    text = " ".join(file_text)
    return len(text.split())


def create_record(source_eng, target_eng, size):
    words = 0
    ratios = (10, 1, 1)  # train:val:test ratios
    tvt = (0, 0, 0)
    while True:
        for file in range(tvt[0], tvt[0] + ratios[0]):  # train
            words += record_count_words(source_eng, 'train', file)
            copy_files(source_eng, target_eng, 'train', file)
        for file in range(tvt[1], tvt[1] + ratios[1]):  # val
            words += record_count_words(source_eng, 'val', file)
            copy_files(source_eng, target_eng, 'val', file)
        for file in range(tvt[2], tvt[2] + ratios[2]):  # test
            words += record_count_words(source_eng, 'test', file)
            copy_files(source_eng, target_eng, 'test', file)

        # update files
        tvt = tvt[0] + ratios[0], tvt[1] + ratios[1], tvt[2] + ratios[2]

        if words > size:
            print('ReCoRD:', words)
            print(tvt)
            break


source = 'combined-txt-eng'
target = 'combined-txt-eng-subsets'
sub_folders = ['test', 'train', 'val']
dataset_size = {'BoolQ': 20000,
                'CB': 14000,
                'MultiRC': 14000,
                'ReCoRD': 14000,
                'RTE': 14000,
                'WiC': 14000}

# create dirs
tasks = dataset_size.keys()
make_dirs(target, tasks, sub_folders)

# create subsets
create_boolq(f'{source}/BoolQ', f'{target}/BoolQ', size=dataset_size['BoolQ'])
create_multirc(f'{source}/MultiRC', f'{target}/MultiRC', size=dataset_size['MultiRC'])
create_record(f'{source}/ReCoRD', f'{target}/ReCoRD', size=dataset_size['ReCoRD'])
create_cb(f'{source}/CB', f'{target}/CB', size=dataset_size['CB'])
create_rte(f'{source}/RTE', f'{target}/RTE', size=dataset_size['RTE'])
create_wic(f'{source}/WiC', f'{target}/WiC', size=dataset_size['WiC'])

# # create full COPA and WSC
# shutil.copytree(f'{source}/COPA', f'{target}/COPA')
# shutil.copytree(f'{source}/WSC', f'{target}/WSC')
