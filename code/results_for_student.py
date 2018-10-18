#! /usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import glob
from code.run_analysis import SPTC, Result

def unpickle_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    how_many_elements = 36
    data_set_12 = sorted(unpickle_file('res/1.2.dump').items(), key=lambda x:x[1][1]['cl_omega'], reverse=True)[:how_many_elements]
    print(data_set_12)
    data_set_2 = unpickle_file('res/2.dump')
    data_set_10 = unpickle_file('res/10.dump')
    for x in range(36): # 36 zestawów danych do analizy
        pass
    for path in glob.glob('res/*.dump'):
        print(path.split('/')[-1][:-5])
        with open(path, 'rb') as f:
            content = pickle.load(f)
            for seqset_name, results in sorted(content.items()):
                print('\t', seqset_name, str(results[0]), results[1])