from consts.base_consts import *
from service.service_block import *
from service.service_consts import *
from service.service_info import *
from service.service_url import *


# 1 уровень заполняется 2, 3, 4, 5
def block2_main_1_2345():
    process_block(1, 6, 'block2', level_mode = 1) 

# заполняем 3 уровень 4 уровнем
def block2_main_3_4():
    process_block(3, 4, 'block2')  

#4 уровень заполняется 4 уровнем
def block2_main_4_4():
    process_block(4, 4, 'block2', url_name = 'parent', url_mode = 1)

# 2 уровень заполняется 3, 5 уровнем
def block2_main_2_345():
    process_block(2, 6, 'block2', level_mode = 1) 

# заполняем 4 уровень 5 уровнем
def block2_main_4_5():
    process_block(4, 5, 'block2')  

# 5 уровень заполняется 5 уровнем
def block2_main_5_5():
    process_block(5, 5, 'block2', url_name = 'parent', url_mode = 1)

# заполняем 3 уровень 5 уровнем
def block2_main_3_5():
    process_block(3, 5, 'block2')  

# заполняем 3 уровень 3 уровнем
def block2_main_3_3():
    process_block(3, 3, 'block2', url_name = 'parent', url_mode = 1) 

def block1_main_2345_2345(name_block = 'block1', geo1 = False, geo2 = False, url_name = 'url', city = 'Минск'):
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if main_info.get('is_price'): continue
        if main_info['GEO']['is'] != geo1: continue
        if main_info['level'] != 1: continue
        levels = [[], [], [], []]
        for child_info in get_child_level(main_info['url'], level1 = 1, level2 = 6, url_name='url', url_mode = 0, level_mode = 1, geo = geo2):
            levels[child_info['level'] - 2].append(child_info)

        info_outs = []
        for level in levels:
            info_outs.extend(sorted(level, key=lambda info: info['online_outlinks'][name_block]['main']))

        for info_out in info_outs:
            #if info_out['url'] == 'https://redsale.by/foto-i-video/photographer/obrabotka-fotografiy/restavratsiya-fotografiy':
            #    print('!!!')
            levels_in = []
            for level in levels:
                random.shuffle(level)
            for level in levels:
                levels_in.append(sorted(level, key=lambda info: info['online_inlinks']['all_links']))
            while 1:
                i_random = random.randint(0, 100)
                in1 = len(levels_in[0])
                in2 = len(levels_in[1])
                in3 = len(levels_in[2])
                in4 = len(levels_in[3])
                if not (in1 or in2 or in3 or in4): break 
                i_result = 0
                if in1 > 0 and i_random < 90:
                    i_result = 0
                elif in2 > 0 and i_random > 89 and i_random < 93:
                    i_result = 1
                elif in3 > 0 and i_random > 92 and i_random < 97:
                    i_result = 2
                elif in4 > 0 and i_random > 96:
                    i_result = 3
                elif in2 > 0:
                    i_result = 1
                elif in3 > 0:
                    i_result = 2
                elif in4 > 0:
                    i_result = 3
                
                random_max =  1
                if random_max < len(levels_in[i_result]) - 1: 
                    random_max += 1
                else:
                    random_max = 0 
                child_info = levels_in[i_result].pop(random.randint(0, random_max))
                #if child_info['url'].find('remont/') != -1:
                #    print('')
                if get_url_part(child_info['url'], 1) != get_url_part(info_out['url'], 1) or get_url_part(child_info['url'], 2) == get_url_part(info_out['url'], 2): continue
                try:
                    add_info_in_block(info_out, child_info, name_block, city=city)
                except MainConstError:
                    break
                except ChildConstError:
                    pass
                except TagUrlError:
                    pass

def block4_main_geo_12345_12345(name_block = 'block4'):
    #block1_main_234_234(name_block = name_block, geo1 = False, geo2 = True, url_name = 'parent', city = '', url_mode = 0)
     
    base_geo = dict()
    for info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if not info['GEO']['is']: continue
        if info.get('is_price'): continue
        base = base_geo.get(info['parent'])
        if base is None: 
            base = list()
            base_geo.update({info['parent']:base})
        base.append(info) 
    for info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if info['GEO']['is']: continue
        if info.get('is_price'): continue
        bases = base_geo.get(info['url'].replace('/tag', ''))
        if not bases: continue
        random.shuffle(bases)
        for child_info in bases:
            if info['level'] != child_info['level']: continue
            try:
                add_info_in_block(info, child_info, name_block)
            except MainConstError:
                break
            except ChildConstError:
                pass
            except TagUrlError:
                pass

# 1 уровень GEO заполняется 2, 3, 4
def block4_main_geo_1_2345(name_block = 'block4'):
    base_levels = dict()
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if main_info.get('is_price'): continue
        if main_info['GEO']['is']:
            if main_info['level'] == 1: continue
            parent = get_url_part(main_info['url'], 1)
            base = base_levels.get(parent)
            if base is None:
                base = (None, list())
                base_levels.update({parent:base})
            base[1].append(main_info)
        elif main_info['level'] == 1:
            base = base_levels.get(main_info['url'])
            if base is None:
                base_levels.update({main_info['url']:(main_info, list())})
            elif base[0] is None:
                base_levels.update({main_info['url']:(main_info, base[1])})
    fill_block(list(filter(lambda x: x[0], map(list, base_levels.values()))), name_block)
    return 
    # если сработает всё ок можно удалять
    for main_info, childs in base_levels.values():
        if main_info is None: continue
        random.shuffle(childs)
        childs = sorted(childs, key=lambda info: info['online_inlinks']['all_links'])
        for child_info in childs:
            try:
                add_info_in_block(main_info, child_info, name_block)
            except MainConstError:
                break
            except ChildConstError:
                pass
            except TagUrlError:
                pass

def block4_geo_1234_1234(name_block = 'block4'):
    base = dict()
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if not main_info['GEO']['is']: continue
        if main_info.get('is_price'): continue
        base_parent = base.get(main_info['parent'])
        if base_parent is None: 
            base_parent = list()
            base.update({ main_info['parent']:base_parent})
        base_parent.append(main_info)
    for base_parent in base.values():
        base_child = base_parent.copy()
        for main_info in base_parent:
            random.shuffle(base_child)
            base_child = sorted(base_child, key=lambda info: info['online_inlinks'][name_block]['geo'])
            for child_info in base_child:
                try:
                    add_info_in_block(main_info, child_info, name_block)
                except MainConstError:
                    break
                except ChildConstError:
                    pass
                except TagUrlError:
                    pass

# 1 уровень заполняется 2, 3, 4
def block2_geo_main_1_2345():
    process_block(1, 6, 'block2', url_name='parent', geo1 = True, geo2 = False, level_mode = 1) #Вакансии

def block2_geo_main_2_3(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 2, level2 = 3, parent_level = 2)

def block2_geo_main_2_4(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 2, level2 = 4, parent_level = 2)

def block2_geo_main_4_5(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 4, level2 = 5, parent_level = 2)

def block2_geo_main_3_5(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 3, level2 = 5, parent_level = 2)

def block2_geo_main_2_5(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 2, level2 = 5, parent_level = 2)

def block2_geo_main_3_3(name_block = 'block2'):
    block2_geo_main(name_block = name_block, level1 = 3, level2 = 3, parent_level = 2)

def block2_geo_main_4_4(name_block = 'block2'):
    block2_geo_main(name_block = name_block)

def block2_geo_main(name_block = 'block2', level1 = 4, level2 = 4, parent_level = 3, geo1 = True, geo2 = False):
    base_main = dict()
    base_child = dict()
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if main_info.get('is_price'): continue
        if main_info['GEO']['is'] == geo1:
            if not main_info['level'] == level1: continue
            base = base_main
        elif main_info['GEO']['is'] == geo2:
            if not main_info['level'] == level2: continue
            base = base_child
        else:
            continue
        parent = get_url_part(main_info['url'], parent_level)
        
        base2 = base.get(parent)
        if base2 is None:
            base2 = list()
            base.update({parent:base2})
        base2.append(main_info)
    fill_block2(base_main, base_child, name_block = name_block)

def block1_main_234_1234(name_block = 'block1'):
    block1_geo_234_1234(name_block, geo = False, mode_find = 1)

def block5_main_12345_12345(name_block = 'block5'):
    bases = dict()
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        i = 0 if main_info['url'].find('/vacancy/') == -1 else 1
        parent = main_info['url'].replace('/vacancy/', '/')
        base = bases.get(parent)
        if base is None:
            base = [None, None]
            bases.update({parent:base})
        base[i] = main_info
    for main_info, child_info in bases.values():
        if not (main_info and child_info): continue
        try:
            add_info_in_block(main_info, child_info, name_block)
        except MainConstError:
            pass
        except ChildConstError:
            pass
        except TagUrlError:
            pass


def block1_geo_234_1234(name_block = 'block1', geo = True, mode_find = 0):
    base_main = list()
    base_child = list()
    check = (
        lambda main_info, geo: main_info['GEO']['is'] == geo,
        lambda main_info, geo: main_info['GEO']['is'] == geo and main_info['url'].find('/vacancy/') != -1,
    )
    func_check = check[mode_find]
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if main_info.get('is_price'): continue
        if not func_check(main_info, geo): continue
        if main_info['level'] != 1:base_main.append(main_info)
        base_child.append(main_info)

    stop = False
    while not stop:
        stop = True
        for main_info in base_main:
            main_parent1 = get_url_part(main_info['url'], 1)
            main_parent = get_url_part(main_info['url'], 2)
            random.shuffle(base_child)
            base_child = sorted(base_child, key=lambda info: info['online_inlinks']['all_links'])
            for child_info in base_child:
                #print(main_parent, get_url_part(child_info['url'], 2))
                if main_parent1 != get_url_part(child_info['url'], 1) or main_parent == get_url_part(child_info['url'], 2): continue
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

# 234 по parent 1 лвла
def block1_geo_1_234(name_block = 'block1'):
    base = list()
    for main_info in BASE_DOMEN[DOMEN_SELECT[0]]:
        if main_info.get('is_price'): continue
        if not main_info['GEO']['is'] or main_info['level'] != 1: continue
        base.append((main_info, get_child_level(main_info['parent'], 1, 5, url_name = 'url', geo = True, level_mode = 1)))

    for main_info, base_child in base:
        for child_info in base_child:
            random.shuffle(base_child)
            base_child = sorted(base_child, key=lambda info: info['online_inlinks'][name_block]['geo'])
            for child_info in base_child:
                try:
                    add_info_in_block(main_info, child_info, name_block)
                except MainConstError:
                    break
                except ChildConstError:
                    pass
                except TagUrlError:
                    pass

def block3_main_1234_1234(name_block = 'block3'):
    base_telo = dict()
    for main_info in BASE_DATA:
        if main_info['GEO']['is']: continue
        if main_info.get('is_price'): continue
        url_telo = get_url_body(main_info['url'])
        base = base_telo.get(url_telo)
        if base is None:
            base = list()
            base_telo.update({url_telo:base})
        base.append(main_info)
    for base in base_telo.values():
        for main_info in base:
            for child_info in base:
                try:
                    add_info_in_block(main_info, child_info, name_block, mode_get_tag_url = False)
                except MainConstError:
                    break
                except ChildConstError:
                    pass
                except TagUrlError:
                    pass

def block1_main_price_1234_234(name_block = 'block1'):
    #block1_main_234_234(name_block = name_block, geo1 = False, geo2 = True, url_name = 'parent', city = '', url_mode = 0)
    #base_price = list()
    bases = dict()
    for info in BASE_DOMEN[DOMEN_SELECT[0]]:
          # base_price1.get_url_part(info['url'], 1)
        part1 = get_url_part(info['parent'], 1)
        i = 0
        if info.get('is_price'): i = 1
        base = bases.get(part1)
        if base is None:
            base = ([], [])
            bases.update({part1:base})
        base[i].append(info)
        #base_price.append(info)
    #del base_level1
    for base in bases.values():
        stop = True
        while stop:
            random.shuffle(base[0])
            random.shuffle(base[1])
            stop = False
            for main_info, child_info in zip(*base):
                if main_info['parent'].find(child_info['parent']) != -1: continue
                try:
                    add_info_in_block(main_info, child_info, name_block)
                    stop = True
                except MainConstError:
                    base[0].remove(main_info)
                except ChildConstError:
                    base[1].remove(child_info)
                except TagUrlError:
                    pass