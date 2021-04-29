import random

from consts.base_consts import *
from service.service_info import *
from service.service_consts import *

def get_child_level(url, level1, level2, url_name, geo = False, level_mode = 0, url_mode = 0):
    '''
    level_mode = 0 -> level2 == child_level;
    level_mode = 1 -> level1 < child_level < level2;
    url_mode = 0 -> начинается ли child_url с url
    url_mode = 1 -> child_url == url;
    '''
    result = list()
    check_level = (
        lambda a, b, info: b == info['level'],
        lambda a, b, info: a < info['level'] and info['level'] < b,
        #lambda a, b, c: a > b,
    )
    check_url = (
        lambda url, url_child: url_child.startswith(url), # URL начинается с URL
        lambda url, url_child: url == url_child # URL = URL
    )
    check_level_func = check_level[level_mode]
    check_url_func = check_url[url_mode]
    for info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if info.get('is_price'): continue
        #if not (info['GEO']['is'] == geo and check_level_func(level1, level2, info) and check_url_func(url, info[url_name])): continue
        if not info['GEO']['is'] == geo: continue
        if not (check_level_func(level1, level2, info) and check_url_func(url, info[url_name])): continue
        result.append(info)

    random.shuffle(result)
    return list(sorted(result, key=lambda info: info['online_inlinks']['all_links']))
# заполняем какой то уровень каким то другим уровнем 1-2, 2-4, 3-4. дочерними ссылками.
def process_block(level1, level2, name_block, url_name = 'url', geo1 = False, geo2 = False, level_mode = 0, url_mode = 0):
    bases = list() #https://redsale.by/mebel/peretyazhka-mebeli/peretyazhka-divana/tag/peretyazhka-kuhonnogo-ugolka/derevo
    for info in BASE_DOMEN[DOMEN_SELECT[0]]: # откалываем часть GEO https://redsale.by/mebel/kamennaya-gorka должно остаться https://redsale.by/mebel/
        if info.get('is_price'): continue
        if info['GEO']['is'] != geo1 or info['level'] != level1: continue
        url = info[url_name]
        bases.append([info, get_child_level(url, level1, level2, url_name = url_name, geo = geo2, level_mode = level_mode, url_mode = url_mode)])
    fill_block(bases, name_block)

def fill_block(bases, name_block):
    stop = True
    while stop:
        stop = False
        for info in bases:
            #print(info)
            if len(info[1]) == 0: continue
            random.shuffle(info[1])
            info[1] = sorted(info[1], key=lambda info: info['online_inlinks']['all_links'])
            try:
                add_info_in_block(info[0], info[1].pop(0), name_block)
                stop = True
            except MainConstError:
                pass
            except ChildConstError:
                pass
            except TagUrlError:
                pass

def fill_block2(base1, base2, name_block):
    stop = False
    while not stop:
        stop = True
        for key, base_main in base1.items():
            random.shuffle(base_main)
            base_child = base2.get(key)
            if not base_child or not len(base_child): continue
            for main_info in base_main:
                random.shuffle(base_child)
                base_child = sorted(base_child, key=lambda info: info['online_inlinks'][name_block]['geo'])
                for child_info in base_child:
                    if main_info['parent'] == child_info['url'].replace('/tag', ''): continue
                    try:
                        add_info_in_block(main_info, child_info, name_block)
                        stop = False
                        break
                    except MainConstError:
                        break
                    except ChildConstError:
                        pass
                    except TagUrlError:
                        pass