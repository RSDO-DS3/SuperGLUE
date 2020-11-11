"""This script validates whether a translation is in the right encoding"""

import os

for root, dirs, files in os.walk("/home/ales/Downloads/diaci-4.11./BoolQ-20k"):
    if not dirs:
        for file in files:
            file = os.path.join(root, file)
            with open(file, encoding='utf-8') as f:
                try:
                    f.read()
                    print(file, 'UTF-8')
                except:
                    print(file, 'Not UTF-8')
