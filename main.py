import json
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
import time


class WebScraper():
    def __init__(self,name,dct) -> None:
        self.name = name
        self.configuration = dct
    
    def __repr__(self) -> str:
        return 'WebScraper(' + self.name + ',' + self.configuration['url'] + ')'
    
    def data_request(self):
        """handling web connection
        """
        try: 
            http_response = requests.get(self.configuration['url'])
            return http_response
        except ConnectionError as msg:
            return f"Connection Error :: {msg}"
    
    def dictionary(self) -> dict:
        content = self.data_request()
        soup = bs(content.text,"html.parser")
        data = soup.find_all(self.configuration['html_tag'])
        datalist = [d.get_text() for d in data]
        sino_list = datalist[0::4]
        pinyin_list =  datalist[1::4]
        role_list = datalist[2::4]
        en_list =  datalist[3::4]
        return dict(zip(sino_list,zip(pinyin_list,role_list,en_list)))
    # def control_data_flow(dictionary,N,timelapse):
#     keys_list = list(dictionary.keys())
#     random.shuffle(keys_list)
#     n = 0
#     while n < N:
#         k = keys_list.pop(n)
#         print(f"| {k} | {d[k]} |")
#         print("-"*47)
#         time.sleep(timelapse)
#         n += 1

if __name__ == "__main__":

    start = time.time()

    with open("config.json") as f:
        cfg = json.load(f)
    
    scp = WebScraper("myscraper",cfg)
    dct = scp.dictionary()

    with open("mydict.json","w") as f:
        json.dump(dct,f)
    
    end = time.time()

    print(f"EXECUTION TIME : {end-start}")