#! /usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import shutil
import os
import random
import argparse
import sys
sys.path.insert(0,'/home/galan/msa_exercises/')
print(sys.path)
from code.run_analysis import SPTC, Result


instruction = '''Celem tego ćwiczenia jest zapoznanie się z różnymi metodami dopasowywania sekwencji oraz ich porównanie. Każdorazowo notuj wyniki porównania dopasowań, a w punkcie 3 również czasy ich tworzenia.
1. Pobierz plik z sekwencjami w formacie fasta znajdujący się pod adresem %s. Plik zawiera mniej-więcej równo oddalone od siebie sekwencje. Użyj programów ClustalX, Clustal Omega oraz MUSCLE do stworzenia dopasowań wielosekwencyjnych w formacie msf. Obejrzyj uzyskane dopasowania. Czy widzisz jakieś różnice?
1.1. Możesz łatwo ocenić, jak szybko działa program do tworzenia dopasowań. Ale czy te dopasowania zostały utworzone prawidłowo? Aby to sprawdzić, skorzystaj z bazy dopasowań referencyjnych BAliBASE. W zbiorze dopasowań referencyjnych 1.2 znajduje się dopasowanie o takim samym identyfikatorze, jak Twój zbiór sekwencji, czyli %s. Skorzystaj z programu bali_score, aby porównać dopasowania utworzone przez Ciebie z dopasowaniem referencyjnym. Dopasowania porównywane przez program bali_score muszą być w formacie msf. Czy wyniki uzyskane różnymi programami różnią się znacznie od siebie?
2. W tej części ćwiczenia również będziesz tworzył dopasowania zestawów sekwencji zawierających pewną ilość sekwencji podobnych (>25%% identyczności na poziomie sekwencji) i 1-3 spokrewnione, lecz odstające (<20%% identyczności, lecz podobna struktura). Sekwencje takie znajdują się w bazie BAliBASE w zbiorze 2. Pobierz dopasowanie o identyfikatorze %s. Przy pomocy programu ClustalX usuń przerwy (zastanów się, co się wtedy stało z dopasowaniem) i zapisz zmieniony plik w formacie fasta. Dopasuj uzyskane sekwencje programami ClustalX, Clustal Omega oraz MUSCLE. Porównaj utworzone przez Ciebie dopasowania z dopasowaniem referencyjnym. Czy widzisz różnice?
3. W trzeciej części ćwiczenia będziesz tworzył dopasowania zestawów sekwencji, które według twórców bazy BAliBASE najbardziej odpowiadają realnym problemom badawczym spotykanym przez naukowców. Sekwencje te znajdziesz w zbiorze 10. Niestety nie ma obecnie możliwości pobrania tylko jednego dopasowania, musisz pobrać archiwum zawierające cały zbiór 10. Wybierz dopasowanie referencyjne o identyfikatorze %s (zastanów się nad właściwym formatem), oraz wykonaj na nowo dopasowanie sekwencji z pobranego przez Ciebie pliku (zastanów się, jakie kroki musisz wykonać, aby to zrobić), mierząc przy okazji czas wykonania dopasowania. Który z użytych programów (ClustalX, Clustal Omega, MUSCLE) wykonał je według Ciebie najszybciej, a który najlepiej? Czas wykonania dopasowania programem ClustalX możesz zmierzyć stoperem.'''


def unpickle_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def sort_according_to_time(container_path, container_key):
    '''
    Sortuje słownik znajdujący się pod container_path zawierający wyniki w formacie
    fragment_ścieżki_pliku:(wyniki_z_bali_score, dict(czasy_tworzenia_dopasowania)) według klucza słowników z czasami
    :param container_path:
    :param container_key:
    :return:
    '''
    return sorted(unpickle_file(container_path).items(), key=lambda x: x[1][1][container_key], reverse=True)

def get_id_and_fasta_name_from_path_fragment(path_fragment):
    '''
    :param path_fragment: 'data/ref_1.2/BBS12023.'
    :return: 'BBS12023', 'BBS12023.tfa'
    '''
    id_ = path_fragment.split('/')[-1].rstrip('.')
    name = id_ + '.tfa'
    return id_, name

def curate_paths(path_list):
    """removes paths containing 'BBS' (in fact shorter seqs)"""
    return [x for x in path_list if not 'BBS' in x]

def round_float_values(a_dictionary):
    return {k:round(v) for k, v in a_dictionary.items()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('path', type=str)
    parser.add_argument('--num_of_text_to_create', type=int, default=8)
    args = parser.parse_args()
    how_many_elements = args.num_of_text_to_create
    fastas_dir = 'fastas'
    sorted_data_set_12 = sort_according_to_time('res/1.2.dump', 'cl_omega')
    curated_paths_of_interest_12 = curate_paths([x[0] for x in sorted_data_set_12])
    file_pattern_12 = 'https://raw.githubusercontent.com/wojciech-galan/msa_exercises/master/%s/%s'
    data_set_2 = unpickle_file('res/2.dump')
    sorted_data_set_10 = sort_according_to_time('res/10.dump', 'cl_omega')
    offset = 6
    truncated_sorted_data_set_10 = list(reversed(sorted_data_set_10[offset:offset+how_many_elements]))
    curated_data2_fragments = curate_paths(data_set_2)  # w bazie nie widać linków do BBS
    print(1.2)
    for k, v in sorted(sorted_data_set_12):
        if not 'BBS' in k:
            print(k.strip('.').split('/')[-1], v[0], round_float_values(v[1]))
    print(2)
    for k, v in sorted(data_set_2.items()):
        if not 'BBS' in k:
            print(k.strip('.').split('/')[-1], v[0], round_float_values(v[1]))
    print(10)
    for k, v in sorted(truncated_sorted_data_set_10):
        print(k.strip('.').split('/')[-1], v[0], round_float_values(v[1]))
    try:
        shutil.rmtree(fastas_dir)
        os.makedirs(fastas_dir)
    except IOError:
        pass
    for path in curated_paths_of_interest_12:
        id_12, name_12 = get_id_and_fasta_name_from_path_fragment(path)
        shutil.copyfile(path + 'tfa', os.path.join(fastas_dir, name_12))
    for i in range(how_many_elements):
        path_12 = random.choice(curated_paths_of_interest_12)
        id_12, name_12 = get_id_and_fasta_name_from_path_fragment(path_12)
        path_fragment_2 = random.choice(curated_data2_fragments)
        id_2, _ = get_id_and_fasta_name_from_path_fragment(path_fragment_2)
        id_10, _ = get_id_and_fasta_name_from_path_fragment(random.choice(truncated_sorted_data_set_10)[0])
        with open(os.path.join(args.path+str(i), 'instrukcja'), 'w') as f:
            f.write(instruction%(file_pattern_12 % (fastas_dir, name_12), id_12, id_2, id_10))

    print(i, len(curated_data2_fragments), len(sorted_data_set_10))



