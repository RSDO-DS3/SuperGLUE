"""Number of translated documents for each dataset"""

import os
from collections import defaultdict

d = defaultdict(int)
for root, dirs, files in os.walk("slovene-translations/txt"):
    if not dirs:
        # print(root, dirs, files)
        task = '-'.join(root.split('/')[2:])
        d[task] += len(files)

l = sorted([(key, value) for key, value in d.items()])
for task, num in l:
    print(task, ':', num, '\n')

