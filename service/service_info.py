import copy
from consts.base_consts import *
from service.service_url import *
from service.service_consts import *

class TagUrlError(Exception):pass

def check_GEO(info):
    info['GEO'].update({'city':CONST_GEO['city'].get(get_url_parent0(info['url']))})
    geo_name = get_url_end(info['url'])
    for type_ in CONST_GEO_TYPE:
        name = CONST_GEO[type_].get(geo_name)
        if name is None: continue
        info['level'] -= 1
        info['GEO'].update({'name':name, 'type':type_, 'is':True})
        break

def base_add_info(info):
    url_domen = get_url_parent0(info['url'])
    base = BASE_DOMEN.get(url_domen)
    if base is None:
        base = list()
        BASE_DOMEN.update({url_domen:base})
    base.append(info)
    BASE_DATA.append(info)

def info_add_tags(info, row, index_block):
    tags = dict()
    for i_tag, r in enumerate(row[index_block:index_block + 5]):
        tags.update({f'tag{i_tag + 1}':[r.value, 0]})
    info.update({'name_tags':tags})

def info_add_block(info, row, index_block):
    bloks = dict()
    for i_block, r in enumerate(row[index_block + 5:index_block + 10]):
        bloks.update({f'block{i_block + 1}':{'name':r.value, 'tag_url':[]}})
    info.update({'name_bloks':bloks})

def add_info(row, index_block = 3):
    url = row[0].value
    if url is None or url == '': return
    #if url.find('redsale.by/mebel') != -1 or url.find('redsale.by/vacancy') != -1: return
    level = get_url_level(url)
    if url.find('redsale.by/price/') != -1:
        pass #level = 2

    info = {
        'level':level,
        'url':url,
        'parent':get_url_parent(url),
        'PR':0,
        'id_container':int(row[2].value) if row[2].value else '',
        'GEO':{
            'is':False
        }
    }
    if url.find('redsale.by/price/') != -1:
        info.update({'is_price':True}) #level = 2

    check_GEO(info)
    info_add_block(info, row, index_block = index_block)
    info_add_tags(info, row, index_block = index_block)

    if info['GEO']['is']:
        info.update(copy.deepcopy(CONST_DATA_GEO[f'level{info["level"]}']))
    else:
        info.update(copy.deepcopy(CONST_DATA[f'level{info["level"]}']))
    
    base_add_info(info)

def get_tag_url(info_url, city = ''):
    tags = tuple(filter(lambda tag: not tag is None, info_url['name_tags'].values()))
    min_i, min_count = 0, tags[0][1] - 1
    for i in range(1, len(tags) - 1):
        if not tags[i][0] is None and min_count > tags[i][1]:
            min_count = tags[i][1]
            min_i = i
    tag = tags[min_i][0]
    info_url['name_tags'][f'tag{min_i + 1}'][1] += 1
    if city != '': city = info_url['GEO']['city']
    return [f'{tag} {city}', info_url['url'], info_url['GEO'].get('name', ''), info_url['level']]

def add_info_in_block(main_info, child_info, name_block, city = '', mode_get_tag_url = True):
    if main_info['url'] == child_info['url']: return

    for block in main_info['name_bloks'].values():
        for tag_url in block['tag_url']:
            if tag_url[1] == child_info['url']: raise TagUrlError() 

    up_online(main_info, child_info, name_block)
    if mode_get_tag_url:
        tag_url = get_tag_url(child_info, city)
    else:
        tag_url = (child_info["GEO"]["city"], child_info['url'])
    main_info['name_bloks'][name_block]["tag_url"].append(tag_url)
