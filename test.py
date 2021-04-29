import copy
import hashlib
import json
import random

from block import *
from consts import base_consts
from consts.base_consts import *

NEW_HASH = True

TEST_STEP = True
TEST_FULL = True
filename = 'table_test.xlsx'

dir = 'tests\\'

random.seed(123)

NAME_FUNC = (
    'block2_main_1_234',
    'block2_main_3_4',
    'block2_main_4_4',
    'block2_main_2_3',
    'block2_main_3_3',
    'block2_main_2_4',
    'block1_main_234_234',
)

def add_hash(base_hash, name, obj):
    if NEW_HASH:save_result(obj, name + 'new')
    hash = hashlib.md5(str(obj).encode())
    base_hash.update({name:hash.hexdigest()})

def pass_func():
    print('функции не существует!')

def get_hashs():
    global BASE_DATA
    process_sheet('Data (Вакансии)')
    base_hash = dict()
    add_hash(base_hash = base_hash, name = 'sheet', obj = BASE_DATA)
    if TEST_STEP:
        #base_data_save = copy.deepcopy(BASE_DATA)
        #print(id(base_data_save), id(BASE_DATA))
        for name in NAME_FUNC:
            process_sheet('Data (Вакансии)')
            init()
            globals().get(name, pass_func)()
            add_hash(base_hash = base_hash, name = name, obj = BASE_DATA)
            #print(base_data_save == BASE_DATA)
            #BASE_DATA = copy.deepcopy(base_data_save)
            #print(id(base_data_save), id(BASE_DATA))
    if TEST_FULL:
        process_sheet('Data (Вакансии)')
        init()
        for name in NAME_FUNC:
            globals().get(name, pass_func)()
        add_hash(base_hash = base_hash, name = 'result', obj = BASE_DATA)
    return base_hash

def process_pagerank():
    import numpy as np
    from fast_pagerank import pagerank
    from scipy import sparse
    base_urls = tuple(map(lambda info: info['url'], BASE_DATA))

    page_counts = len(base_urls)
    
    result = list()
    
    for info_url in BASE_DATA:
        main_i = base_urls.index(info_url['url'])
        for i_block in range(1, 4):
            for tag_url in info_url['name_bloks'][f'block{i_block}']["tag_url"]:
                result.append([main_i, base_urls.index(tag_url[1])])
    if not len(result): return
    A = np.array(result)
    G = sparse.csr_matrix(([1] * len(A), (A[:,0], A[:,1])), shape=(page_counts, page_counts))  #shape=(4, 4))
    pr = pagerank(G, p=0.85)
    for info in zip(BASE_DATA, pr):
        info[0].update({'PR':info[1]})

def process_sheet(table_name = 'Data (Вакансии)'):
    from openpyxl import load_workbook
    wb = load_workbook(f'{dir}{filename}', read_only= True)
    sheet_data = wb[table_name]
    for row in tuple(sheet_data.rows)[1:]:
        url = row[0].value
        if url is None or url == '': continue
        add_info(get_info_url(url), row)
    

def save_result(base_write, name = 'result'):
    with open(f'{dir}{name}.json', "w", encoding='UTF-8') as f:
        f.write(json.dumps(base_write, indent=4, ensure_ascii=False))

def get_result(name = 'result'):
    with open(f'{dir}{name}.json', "r") as f:
        return json.load(f)

def main():
    #process_sheet()
    base_hashs_new = get_hashs()
    if NEW_HASH: 
        save_result(base_hashs_new, 'result_new')
    base_hashs = get_result()
    for key, hash in base_hashs.items():
        print(key, end=' - ')
        if base_hashs_new[key] == hash:
            print('Ok')
        else:
            print('ERROR')

import time

if __name__ == '__main__':
    time_start = time.time()
    main()
    print(time.time() - time_start)
