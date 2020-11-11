"""Create empty slo files"""

import os


def create_boolq(eng_root, slo_root, splits, task):
    translate = ['question', 'passage']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_cb(eng_root, slo_root, splits, task):
    translate = ['premise', 'hypothesis']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_copa(eng_root, slo_root, splits, task):
    translate = ['premise', 'choice1', 'choice2']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_rte(eng_root, slo_root, splits, task):
    translate = ['premise', 'hypothesis']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_wsc(eng_root, slo_root, splits, task):
    translate = ['text']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] in translate:
                        # slo.write(lines[0] + ':' +
                        #           '<w1></w1> ' +
                        #           '<w2></w2> ' +
                        #           '\n')
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_record(eng_root, slo_root, splits, task):
    translate = ['query', 'text']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0] == 'passage.text':
                        # slo.write(lines[0] + ':' + ' '.join(re.findall('<.*?>', lines[1])) + '\n')
                        slo.write(lines[0] + ':' + '\n')
                    elif lines[0].split('.')[-1] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def create_multirc(eng_root, slo_root, splits, task):
    translate = ['question', 'text']
    for s in splits:
        for file in os.listdir(os.path.join(eng_root, task, s)):
            eng_file = os.path.join(eng_root, task, s, file)
            slo_file = os.path.join(slo_root, task, s, file)
            with open(eng_file, 'r') as eng, open(slo_file, 'w') as slo:
                for line in eng.readlines():
                    lines = line.split(':', 1)
                    if lines[0].split('.')[-1] in translate:
                        slo.write(lines[0] + ':' + '\n')
                    else:
                        slo.write(line)


def make_dirs(source, tasks, sub_folders):
    for task in tasks:
        for sf in sub_folders:
            os.makedirs(os.path.join(source, task, sf), exist_ok=True)


if __name__ == '__main__':
    # variables
    SOURCE = 'combined-txt-eng-subsets'
    TARGET = 'combined-txt-slo'
    SUB_FOLDERS = ['test', 'train', 'val']
    TASKS = ['WiC', 'CB', 'ReCoRD', 'BoolQ', 'MultiRC', 'COPA', 'RTE', 'WSC']

    # create dirs
    make_dirs(TARGET, TASKS, SUB_FOLDERS)

    # create slo files without english text and copy constants
    create_boolq(SOURCE, TARGET, SUB_FOLDERS, task='BoolQ')
    create_cb(SOURCE, TARGET, SUB_FOLDERS, task='CB')
    create_copa(SOURCE, TARGET, SUB_FOLDERS, task='COPA')
    create_rte(SOURCE, TARGET, SUB_FOLDERS, task='RTE')
    create_wsc(SOURCE, TARGET, SUB_FOLDERS, task='WSC')
    create_multirc(SOURCE, TARGET, SUB_FOLDERS, task='MultiRC')
    create_record(SOURCE, TARGET, SUB_FOLDERS, task='ReCoRD')