
class MainConstError(Exception):pass
class ChildConstError(Exception):pass

def check_const(info, name_block, const_name = 'outlinks', name = 'main'): 
    return not (info[f'online_{const_name}']['all_links'] < info[f'const_{const_name}']['all_links'] and info[f'online_{const_name}'][name_block][name] < info[f'const_{const_name}'][name_block][name])

def up_online(main_info, child_info, name_block):
    geo1 = main_info['GEO']['is'] 
    geo2 = child_info['GEO']['is']
    if not geo1 and not geo2:# main + main
        name1 = 'main'
        name2 = 'main'
    elif geo1 and not geo2: # geo + main
        name1 = 'main'
        name2 = 'geo'
    elif not geo1 and geo2: # main + geo
        name1 = 'geo'
        name2 = 'main'
    else: # geo + geo
        name1 = 'geo'
        name2 = 'geo'
    if check_const(main_info, name_block, const_name='outlinks', name = name1): raise MainConstError()
    if check_const(child_info, name_block, const_name='inlinks', name = name2): raise ChildConstError() 
    main_info['online_outlinks']['all_links'] += 1
    main_info['online_outlinks'][name_block][name1] += 1
    child_info['online_inlinks']['all_links'] += 1
    child_info['online_inlinks'][name_block][name2] += 1