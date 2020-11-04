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


source = 'combined-txt-eng-subsets'
target = 'combined-txt-slo'
sub_folders = ['test', 'train', 'val']
tasks = ['WiC', 'CB', 'ReCoRD', 'BoolQ', 'MultiRC', 'COPA', 'RTE', 'WSC']

# create dirs
make_dirs(target, tasks, sub_folders)

# create slo files without english text and copy constants
create_boolq(source, target, sub_folders, task='BoolQ')
create_cb(source, target, sub_folders, task='CB')
create_copa(source, target, sub_folders, task='COPA')
create_rte(source, target, sub_folders, task='RTE')
create_wsc(source, target, sub_folders, task='WSC')
create_multirc(source, target, sub_folders, task='MultiRC')
create_record(source, target, sub_folders, task='ReCoRD')