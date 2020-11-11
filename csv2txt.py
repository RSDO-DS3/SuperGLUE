import argparse
import os
import pandas as pd


def csv2txt_group(csv_eng, txt_eng):
    for file in os.listdir(csv_eng):
        csv_file = os.path.join(csv_eng, file)
        os.makedirs(os.path.join(txt_eng, file.split('.')[0]), exist_ok=True)

        df = pd.read_csv(csv_file)
        df = df.reindex(sorted(df.columns), axis=1)
        for sample in df.iterrows():
            file_txt_eng = os.path.join(txt_eng, file.split('.')[0], str(sample[1]['idx']) + '.txt')
            with open(file_txt_eng, 'w') as eng:
                for key, value in sample[1].items():
                    eng.write(str(key) + ":" + str(value) + '\n')


def csv2txt_wsc(csv_eng, txt_eng):
    """Note: Text is segmented by spaces"""
    for file in os.listdir(csv_eng):
        csv_file = os.path.join(csv_eng, file)
        os.makedirs(os.path.join(txt_eng, file.split('.')[0]), exist_ok=True)

        df = pd.read_csv(csv_file)
        df = df.reindex(sorted(df.columns), axis=1)
        for sample in df.iterrows():
            # if sample[1]['idx'] == 129:
            #     print()
            file_txt_eng = os.path.join(txt_eng, file.split('.')[0], str(sample[1]['idx']) + '.txt')
            with open(file_txt_eng, 'w') as eng:
                data = sample[1]

                text = data['text'].split()
                wrapped_text = []

                # Text is segmented by spaces, indices point only to the start of a word.
                # This causes problems because some answers are word phrases.
                # The code below solves this problem.
                w1 = data['target.span1_text'].split()
                w1_idx_start = data['target.span1_index']
                w1_idx_end = w1_idx_start + len(w1)
                w2 = data['target.span2_text'].split()
                w2_idx_start = data['target.span2_index']
                w2_idx_end = w2_idx_start + len(w2)

                if w1_idx_end == w2_idx_start:  # they cancel each other if they are the same
                    w2_idx_start += 1
                    w2_idx_end += 1


                for idx, word in enumerate(text):
                    if idx == w1_idx_start:
                        wrapped_text.append('<w1>')  # '<target.span1_text>'
                        wrapped_text.append(word)
                    elif idx == w1_idx_end:
                        wrapped_text.append('</w1>')
                        wrapped_text.append(word)
                    elif idx == w2_idx_start:
                        wrapped_text.append('<w2>')  # '<target.span2_text>'
                        wrapped_text.append(word)
                    elif idx == w2_idx_end:
                        wrapped_text.append('</w2>')
                        wrapped_text.append(word)
                    else:
                        wrapped_text.append(word)

                eng.write('text:' + str(' '.join(wrapped_text)) + '\n')
                eng.write('idx:' + str(data['idx']) + '\n')

                if 'test' not in file:
                    eng.write('label:' + str(data['label']) + '\n')


def csv2txt_wic(csv_eng, txt_eng):
    """Note: Text is segmented by characters"""
    for file in os.listdir(csv_eng):
        csv_file = os.path.join(csv_eng, file)
        os.makedirs(os.path.join(txt_eng, file.split('.')[0]), exist_ok=True)

        df = pd.read_csv(csv_file)
        df = df.reindex(sorted(df.columns), axis=1)
        for sample in df.iterrows():
            file_txt_eng = os.path.join(txt_eng, file.split('.')[0], str(sample[1]['idx']) + '.txt')
            with open(file_txt_eng, 'w') as eng:
                data = sample[1]
                sent1 = data['sentence1']
                sent2 = data['sentence2']
                start1 = data['start1']
                start2 = data['start2']
                end1 = data['end1']
                end2 = data['end2']

                wrapped_sent1 = sent1[:start1] + '<start1>' + sent1[start1:end1] + '</start1>' + sent1[end1:]
                wrapped_sent2 = sent2[:start2] + '<start2>' + sent2[start2:end2] + '</start2>' + sent2[end2:]

                eng.write('word:' + str(data['word']) + '\n')
                eng.write('sentence1:' + wrapped_sent1 + '\n')
                eng.write('sentence2:' + wrapped_sent2 + '\n')
                eng.write('idx:' + str(data['idx']) + '\n')

                if 'test' not in file:
                    eng.write('label:' + str(data['label']) + '\n')


def csv2txt_multirc(csv_eng, txt_eng):
    for file in os.listdir(csv_eng):
        csv_file = os.path.join(csv_eng, file)
        os.makedirs(os.path.join(txt_eng, file.split('.')[0]), exist_ok=True)

        df = pd.read_csv(csv_file)
        df = df.reindex(sorted(df.columns, reverse=True), axis=1)

        for sample in df.iterrows():
            file_txt_eng = os.path.join(txt_eng, file.split('.')[0], str(sample[1]['idx']) + '.txt')
            with open(file_txt_eng, 'w') as eng:
                for key, value in sample[1].items():
                    if value != value:  # test for Nan values
                        continue
                    else:
                        eng.write(str(key) + ":" + str(value) + '\n')


def simplify_record_key(key):
    if 'answers' in key:
        e = key.split('.')
        return 'q.' + e[1] + '.a.' + e[3]
    if 'entities' in key:
        e = key.split('.')
        return 'e.' + e[2]


def csv2txt_record(csv_eng, txt_eng, first_n):
    """Drop entities which are also answers, the answer will be embedded into a text"""
    for file in os.listdir(csv_eng):
        csv_file = os.path.join(csv_eng, file)
        os.makedirs(os.path.join(txt_eng, file.split('.')[0]), exist_ok=True)

        df = pd.read_csv(csv_file, low_memory=False)  # some columns contain nan values
        df = df.reindex(sorted(df.columns), axis=1)

        for num, sample in enumerate(df.iterrows()):
            if num > first_n:
                break
            file_txt_eng = os.path.join(txt_eng, file.split('.')[0], str(sample[1]['idx']) + '.txt')
            with open(file_txt_eng, 'w') as eng:
                data = sample[1]
                data = data.dropna()

                # wrap all entities
                text = data['passage.text']
                data_indices = data.filter(regex='start|end')

                ent = data_indices.filter(regex='entities').sort_values(ascending=False)
                ans = {val: key for key, val in data_indices.filter(regex='answers').items()}  # answers set is a subset of entities set

                for key, val in ent.items():
                    val = int(val)
                    if val in ans.keys():
                        key = ans[val]
                    if key.endswith('end'):
                        key = simplify_record_key(key)
                        text = text[:val+1] + '</' + key + '>' + text[val+1:]
                    if key.endswith('start'):
                        key = simplify_record_key(key)
                        text = text[:val] + '<' + key + '>' + text[val:]

                text = text.replace('\n', ' ')  # remove newlines
                data['passage.text'] = text
                data2write = data.filter(regex='text|query')

                for key, value in data2write.items():
                    eng.write(str(key) + ":" + str(value) + '\n')
                eng.write('idx:' + str(data['idx']) + '\n')
                eng.write('source:' + str(data['source']) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Format conversion tool'
    )

    parser.add_argument('--csv', required=True)
    parser.add_argument('--txt', required=True)

    args = parser.parse_args()

    # variables
    CSV = args.csv
    TXT = args.txt

    # Group transformation (no nesting, no indices, no NA values)
    group = ['CB', 'COPA', 'RTE', 'BoolQ']
    for dataset in group:
        print(dataset)
        csv_eng = os.path.join(CSV, dataset)
        txt_eng = os.path.join(TXT, dataset)
        csv2txt_group(csv_eng, txt_eng)

    # WSC
    print('wsc')
    csv2txt_wsc(f'{CSV}/WSC', f'{TXT}/WSC')

    # Wic
    print('wic')
    csv2txt_wic(f'{CSV}/WiC', f'{TXT}/WiC')

    # multirc
    print('multirc')
    csv2txt_multirc(f'{CSV}/MultiRC', f'{TXT}/MultiRC')

    # record
    print('record')
    csv2txt_record(f'{CSV}/ReCoRD', f'{TXT}/ReCoRD', first_n=1000)  # large dataset


