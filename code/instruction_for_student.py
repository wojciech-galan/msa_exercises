#! /usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import glob
import shutil
import os
import random
from code.run_analysis import SPTC, Result


instruction = '''Celem tego ćwiczenia jest zapoznanie się z różnymi metodami dopasowywania sekwencji oraz ich porównanie.
1. Pobierz plik z sekwencjami w formacie fasta znajdujący się pod adresem %s. Plik zawiera mniej-więcej równo oddalone od siebie sekwencje. Użyj programów ClustalX, Clustal Omega oraz MUSCLE do stworzenia dopasowań wielosekwencyjnych w formacie msf. Czy zauważyłeś różnicę w szybkości tworzenia dopasowania? Obejrzyj uzyskane dopasowania. Czy widzisz jakieś różnice?
1.1. Możesz łatwo ocenić, jak szybko działa program do tworzenia dopasowań. Ale czy te dopasowania zostały utworzone prawidłowo? Aby to sprawdzić, skorzystaj z bazy dopasowań referencyjnych BAliBASE. W zbiorze dopasowań referencyjnych 1.2 znajduje się dopasowanie o takim samym identyfikatorze, jak Twój zbiór sekwencji, czyli %s. Skorzystaj z programu bali_base, aby porównać dopasowania utworzone przez Ciebie z dopasowaniem referencyjnym. Czy wyniki uzyskane różnymi programami różnią się znacznie od siebie?
2. W tej części ćwiczenia również będziesz tworzył dopasowania zestawów sekwencji zawierających pewną ilość sekwencji podobnych (>25%% identyczności na poziomie sekwencji) i 1-3 spokrewnione, lecz odstające (<20%% identyczności, lecz podobna struktura). Sekwencje takie znajdują się w bazie BAliBASE w zbiorze 2. Pobierz dopasowanie o identyfikatorze %s. Przy pomocy programu ClustalX usuń przerwy (zastanów się, co się wtedy stało z dopasowaniem) i zapisz zmieniony plik. Dopasuj uzyskane sekwencje programami ClustalX, Clustal Omega oraz MUSCLE. Porównaj utworzone przez Ciebie dopasowania z dopasowaniem referencyjnym. Czy widzisz różnice?
3. W trzeciej części ćwiczenia będziesz tworzył dopasowania zestawów sekwencji, które według twórców bazy BAliBASE najbardziej odpowiadają realnym problemom badawczym spotykanym przez naukowców. Sekwencje te znajdziesz w zbiorze 10. Pobierz dopasowanie referencyjne o identyfikatorze %s (zastanów się nad właściwym formatem), oraz wykonaj na nowo dopasowanie sekwencji z pobranego przez Ciebie pliku (zastanów się, jakie kroki musisz wykonać, aby to zrobić), mierząc przy okazji czas wykonania dopasowania. Który z użytych programów (ClustalX, Clustal Omega, MUSCLE) wykonał je według Ciebie najszybciej, a który najlepiej?'''


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


if __name__ == '__main__':
    how_many_elements = 36
    fastas_dir = 'fastas'
    sorted_data_set_12 = sort_according_to_time('res/1.2.dump', 'cl_omega')
    paths_of_interest_12 = [x[0] for x in sorted_data_set_12[:how_many_elements]]
    file_pattern_12 = 'https://raw.githubusercontent.com/wojciech-galan/msa_exercises/master/%s/%s'
    data_set_2 = unpickle_file('res/2.dump')
    sorted_data_set_10 = sort_according_to_time('res/10.dump', 'cl_omega')
    offset = 3
    truncated_sorted_data_set_10 = list(reversed(sorted_data_set_10[offset:offset+how_many_elements]))
    try:
        shutil.rmtree(fastas_dir)
        os.makedirs(fastas_dir)
    except IOError:
        pass
    for i, path in enumerate(paths_of_interest_12):
        #print(path)
        id_12, name_12 = get_id_and_fasta_name_from_path_fragment(path)
        shutil.copyfile(path + 'tfa', os.path.join(fastas_dir, name_12))
        path_fragment_2 = random.choice(list(data_set_2))
        id_2, _ = get_id_and_fasta_name_from_path_fragment(path_fragment_2)
        id_10, _ = get_id_and_fasta_name_from_path_fragment(truncated_sorted_data_set_10[i][0])
        print(instruction%(file_pattern_12 % (fastas_dir, name_12), id_12, id_2, id_10))



