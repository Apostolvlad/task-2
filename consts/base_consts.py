import json

def convert_txt_to_json():
    base = dict()
    with open("t.txt", "r", encoding='UTF-8') as read_file: 
        for line in read_file:
            base.update({line.split('	', 1)[0]:line.split('	', 1)[1].replace('\n', '')})
    print(json.dumps(base, indent=4, ensure_ascii=False))
    input()

with open(r"consts\const-main.json", "r") as read_file: CONST_DATA = json.load(read_file)
with open(r"consts\const-geo.json", "r") as read_file: CONST_DATA_GEO = json.load(read_file)

with open(r"consts\name-geo.json", "r", encoding='UTF-8') as read_file: CONST_GEO = json.load(read_file)
CONST_GEO_TYPE = ('metro', 'district', 'microdistrict')

def init():
    global BASE_URL, BASE_DATA, BASE_DOMEN, DOMEN_SELECT
    BASE_URL = list()
    BASE_DOMEN = dict()
    DOMEN_SELECT = [None,]
    BASE_DATA = list()
init()