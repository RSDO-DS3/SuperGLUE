import pandas as pd
import os
from unflatten import unflatten
import jsonlines

def test_jsonl(org, rev, file):
    org = pd.read_json(org, lines=True)
    org = org.reindex(sorted(org.columns), axis=1)
    rev = pd.read_json(rev, lines=True)
    rev = rev.reindex(sorted(rev.columns), axis=1)
    if org.equals(rev):  # equals fails if two entries are of a different dtype
        print(f'{file:15}OK')
    else:
        # important: inspect failed files manually
        print(f'{file:15}FAIL')


def csv2jsonl(json_eng, csv_eng):
    nested_datasets = ['MultiRC', 'WSC', 'ReCoRD']

    for file in os.listdir(csv_eng):
        save_to = os.path.join(json_eng, file[:-4] + '.jsonl')

        if os.path.join(csv_eng, file).split('/')[-2] in nested_datasets:
            df = pd.read_csv(os.path.join(csv_eng, file))
            with jsonlines.open(save_to, mode='w') as writer:
                for sample in df.iterrows():
                    sample = sample[1].dropna()
                    sample = unflatten(sample.to_dict())
                    writer.write(sample)
        else:
            df = pd.read_csv(os.path.join(csv_eng, file), encoding='utf-8')
            df.to_json(path_or_buf=save_to, orient='records', lines=True, force_ascii=False)  # force_ascii

        # # test (if you want to compare)
        # org_json = os.path.join('combined-json-eng', json_eng.split('/')[1], file[:-4] + '.jsonl')
        # rev_json = save_to
        # test_jsonl(org_json, rev_json, file)


if __name__ == '__main__':
    # variables
    CSV = 'files/csv-eng-reverse'
    JSON = 'files/jsonl-eng-reverse'

    for dataset in os.listdir(CSV):
        print(dataset)
        json_eng = os.path.join(JSON, dataset)
        csv_eng = os.path.join(CSV, dataset)
        os.makedirs(json_eng, exist_ok=True)
        csv2jsonl(json_eng, csv_eng)
