import json
import random
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
import time


class WebScraper:
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

class DataFlowControl:
    def __init__(self,name,timelapse,data,number) -> None:
        self.name = name
        # the time between two data
        self.timelapse = timelapse
        # declare a dictionary to store data
        self.data = data
        self.number = number
    def __repr__(self) -> str:
        return 'DataFlowControl(' + self.name + "," + str(self.timelapse) + "," + str(type(self.data)) + ')'
    def control(self) -> None:
        keys_list = list(self.data.keys())
        random.shuffle(keys_list)
        if 0 < self.number <= len(self.data):
            n = 0
            while n < self.number:
                k = keys_list.pop(n)
                print(f"| {k} | {self.data[k]} |")
                print("-"*43)
                time.sleep(self.timelapse)
                n += 1
        else:
            print("Value Error")
            print(f"Expect a number between 1 and {len(self.data)}")

if __name__ == "__main__":

    start = time.time()

    with open("config.json") as f:
        cfg = json.load(f)
    
    scp = WebScraper("@scraper",cfg)
    dct = scp.dictionary()

    # save the data into a json file
    with open("mydict.json","w") as f:
        json.dump(dct,f)
    # print the data with our own values
    # number refer to the number of sinographs wanted
    ctrl = DataFlowControl("@dataflow",timelapse=2,data=dct,number=0)
    
    ctrl.control()
    
    end = time.time()

    print(f"EXECUTION TIME : {end-start}")