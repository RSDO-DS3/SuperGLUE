import os
from google.cloud import translate_v2 as translate
from tqdm import tqdm


def translate_multirc(root_folder):
    splits = ['test', 'val', 'train']
    for s in splits:
        os.makedirs(os.path.join(SAVE, 'MultiRC', s), exist_ok=True)
        folder = os.path.join(root_folder, s)
        for file in tqdm(os.listdir(folder)):
            file_path = os.path.join(folder, file)
            output = []
            with open(file_path, 'r') as f:
                for line in f:
                    key, text = line.split(':', 1)
                    if ('idx' or 'label') in key:
                        output.append(line)
                    else:
                        result = translate_client.translate(text, source_language='en', target_language='sl')
                        line = key + ':' + result["translatedText"] + '\n'
                        output.append(line)
            output_file = os.path.join(SAVE, 'MultiRC', s, file)
            with open(output_file, 'w') as out:
                out.writelines(output)

    return 'Dataset translated!'


def translate_boolq(root_folder):
    splits = ['val', 'test', 'train']
    for s in splits:
        os.makedirs(os.path.join(SAVE, 'BoolQ', s), exist_ok=True)
        folder = os.path.join(root_folder, s)
        for file in tqdm(os.listdir(folder)):
            file_path = os.path.join(folder, file)
            output = []
            with open(file_path, 'r') as f:
                for line in f:
                    key, text = line.split(':', 1)
                    if key in ['idx', 'label']:
                        output.append(line)
                    else:
                        result = translate_client.translate(text, source_language='en', target_language='sl')
                        line = key + ':' + result["translatedText"] + '\n'
                        output.append(line)
            output_file = os.path.join(SAVE, 'BoolQ', s, file)
            with open(output_file, 'w') as out:
                out.writelines(output)

    return 'Dataset translated!'


if __name__ == '__main__':
    SOURCE = 'combined-txt-eng'
    SAVE = 'google-translations/combined-txt-eng'
    translate_client = translate.Client()

    # print('MultiRC:', translate_multirc(f'{SOURCE}/MultiRC'))
    # print('BoolQ:', translate_boolq(f'{SOURCE}/BoolQ'))