#! /usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import glob
import shutil
import os
from code.run_analysis import SPTC, Result

def unpickle_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    how_many_elements = 36
    fastas_dir = 'fastas'
    data_set_12 = sorted(unpickle_file('res/1.2.dump').items(), key=lambda x:x[1][1]['cl_omega'], reverse=True)
    paths_of_interest_12 = [x[0] for x in data_set_12[:how_many_elements]]
    file_pattern_12 = 'https://github.com/wojciech-galan/msa_exercises/tree/master/%s/%s'
    try:
        shutil.rmtree(fastas_dir)
        os.makedirs(fastas_dir)
    except IOError:
        pass
    for path in paths_of_interest_12:
        name = path.split('/')[-1]+'tfa'
        shutil.copyfile(path+'tfa', os.path.join(fastas_dir, name))
        print(file_pattern_12%(fastas_dir, name))

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