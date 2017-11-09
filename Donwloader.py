import os
import re
import urllib2
import urlparse
import time


class Downloader(object):
    def __init__(self):
        self.header = {}
        pass

    def set_headers(self, headers):
        self.headers = headers

    def _mkdir(self, path):
        path = path.strip()

        isExists = os.path.exists(path)

        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def get_image_list(self, html):
        return re.findall('zoomfile="(.*?[jpg])"', html)

    def _save(self, name, pic):
        with open("./image/" + str(name) +".jpg", "w+") as myfile:
            myfile.write(pic)

    def __call__(self, url, headers={}):
        html = self.download(url, self.headers or headers)
        return html


    def download(self, url, headers={}, data=None):
        time.sleep(3)
        print 'url----is [%s]' % url
        request = urllib2.Request(url, data, self.headers or headers)
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print 'Download error:', str(e)

        return response.read()

class Work(object):
    def __init__(self, url, path):
        self.down = Downloader()
        self.down._mkdir(path)
        self.html = self.down(url)

    def set_headers(self, headers={}):
        self.down.set_headers(headers)

    def work(self):
        image_list = self.down.get_image_list(self.html)
        for i, pic_url in enumerate(image_list):
            pic_info = self.down(pic_url)
            self.down._save(i, pic_info) 


def main():
    url = "http://www.tuyimm.com/thread-7290-1-1.html"
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'pan.baidu.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    
    test = Work(url,"image")
    test.set_headers(header)
    test.work()
if __name__ == "__main__":
    main()
