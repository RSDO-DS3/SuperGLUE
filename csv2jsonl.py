import pandas as pd
import os
from unflatten import unflatten


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
        # # todo: create nested jsonl files if you need them (UNFINISHED)
        # if os.path.join(csv_eng, file).split('/')[-2] in nested_datasets:
        #     df = pd.read_csv(os.path.join(csv_eng, file))
        #     for sample in df.iterrows():
        #         sample = sample[1].dropna()
        #         sample = unflatten(sample.to_dict())
        # else:
        #    df = pd.read_csv(os.path.join(csv_eng, file))

        df = pd.read_csv(os.path.join(csv_eng, file), encoding='utf-8')

        save_to = os.path.join(json_eng, file[:-4] + '.jsonl')
        df.to_json(path_or_buf=save_to, orient='records', lines=True, force_ascii=False)  # force_ascii

        # # test (if you want to compare)
        # org_json = os.path.join('combined-json-eng', json_eng.split('/')[1], file[:-4] + '.jsonl')
        # rev_json = save_to
        # test_jsonl(org_json, rev_json, file)


for dataset in os.listdir('google-translations/csv'):
    print(dataset)
    json_eng = os.path.join('google-translations/json', dataset)
    csv_eng = os.path.join('google-translations/csv', dataset)
    os.makedirs(json_eng, exist_ok=True)
    csv2jsonl(json_eng, csv_eng)
