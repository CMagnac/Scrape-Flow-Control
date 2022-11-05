import json
import random
import requests
from bs4 import BeautifulSoup as bs
import time

with open("config.json") as f:
    cfg = json.load(f)

def extract_data(url=cfg['url']):
    return requests.get(url).text

def transform_data():
    soup = bs(extract_data(),"html.parser")
    return soup

def data_list(soup=transform_data()):
    new_char = soup.find_all(cfg['html_tag'])
    return [sino.get_text() for sino in new_char ]

def create_dictionary(datalist=data_list()):
    sino_list = datalist[0::4]
    pinyin_list =  datalist[1::4]
    role_list = datalist[2::4]
    en_list =  datalist[3::4]
    return dict(zip(sino_list,zip(pinyin_list,role_list,en_list)))

def control_data_flow(dictionary,N,timelapse):
    keys_list = list(dictionary.keys())
    random.shuffle(keys_list)
    n = 0
    while n < N:
        k = keys_list.pop(n)
        print(f"| {k} | {d[k]} |")
        print("-"*47)
        time.sleep(timelapse)
        n += 1

if __name__ == "__main__":

    start = time.time()
    d = create_dictionary()
    control_data_flow(d,5,1)
    end = time.time()
    print(f"EXECUTION TIME : {end-start}")