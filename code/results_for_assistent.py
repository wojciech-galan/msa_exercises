#! /usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import glob
from code.run_analysis import SPTC, Result

if __name__ == '__main__':
    for path in glob.glob('res/*.dump'):
        print(path.split('/')[-1][:-5])
        with open(path, 'rb') as f:
            content = pickle.load(f)
            for seqset_name, results in sorted(content.items()):
                print('\t', seqset_name.split('/')[-1][:-1], str(results[0]), {k:int(v) for k, v in results[1].items()})