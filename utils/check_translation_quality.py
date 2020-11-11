"""With this script, you write random samples of original/translation pairs (for translation quality)"""

import os
import random

NUM = 5  # number of random translations to check
dataset = 'combined-txt-eng/BoolQ/train'
translations = 'slovene-translations/txt/BoolQ/train'
with open('for_checking.txt', 'w') as out:
    folder = list(os.listdir(translations))
    random.shuffle(folder)
    for idx, file in enumerate(folder):

        with open(os.path.join(translations, file)) as tgt:
            out.writelines(tgt.readlines())
            out.write('\n')

        with open(os.path.join(dataset, file)) as src:
            out.writelines(src.readlines())
            out.write(5*'\n')

        if idx == NUM:
            break
