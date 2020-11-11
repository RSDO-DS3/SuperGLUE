import pandas as pd
import os
from google.cloud import translate_v2 as translate
from tqdm import tqdm


def translate_dataset(folder, columns):
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        df = pd.read_csv(file)
        # df = df.iloc[:TEST]  # uncomment for testing purposes
        for col in tqdm(columns):
            print(col)
            to_translate = df[col].to_list()
            translated = []
            for text in tqdm(to_translate):
                result = translate_client.translate(text, source_language='en', target_language='sl')
                translated.append(result["translatedText"])
            df[col] = translated
        # save translated df
        path_to_save = os.path.join(SAVE, folder)
        file_to_save = os.path.join(SAVE, file)
        os.makedirs(path_to_save, exist_ok=True)
        df.to_csv(file_to_save, index=False)


def boolq(folder):
    columns = ['question', 'passage']
    translate_dataset(folder, columns)
    return 'Dataset translated!'


def cb(folder):
    columns = ['premise', 'hypothesis']
    translate_dataset(folder, columns)
    return 'Dataset translated!'


def copa(folder):
    columns = ['premise', 'choice1', 'choice2']
    translate_dataset(folder, columns)
    return 'Dataset translated!'


def rte(folder):
    columns = ['premise', 'hypothesis']
    translate_dataset(folder, columns)
    return 'Dataset translated!'


def wsc(folder):
    columns = ['text']
    translate_dataset(folder, columns)
    return 'Dataset translated!'


if __name__ == '__main__':
    # TEST = 2
    SOURCE = 'combined-csv-eng'
    SAVE = 'google-translations'
    translate_client = translate.Client()

    # print('BoolQ:', boolq(f'{SOURCE}/BoolQ'))
    # print('CB:', cb(f'{SOURCE}/CB'))
    # print('COPA:', copa(f'{SOURCE}/COPA'))
    # print('RTE:', rte(f'{SOURCE}/RTE'))
    # print('WSC:', wsc(f'{SOURCE}/WSC'))
