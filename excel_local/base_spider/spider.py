import requests
from requests import Session,Request,exceptions
import logging,sys,math
from requests.exceptions import ReadTimeout
import urllib.request
from .Throttle import Throttle


class base_spider:



    def __init__(self,delay,retry=1):
        self.retry=retry
        self.throttle = Throttle(delay)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        logging.info('start crawl')
    def get_content(self,url,header=None,timeout=5,proxies=None,maxretry=5):
        self.throttle.wait(url)
        s = Session()
        req = Request('GET', url,headers=header)
        prepped = req.prepare()
        try:
            resp = s.send(prepped,proxies=proxies,timeout=timeout)
            return resp
        except exceptions.Timeout as e:
            self.retry += 1
            self.logger.error(str(e)+"try to retry {}".format(self.retry))
            if self.retry>=maxretry:
                self.logger.error("retry =5 return None".format(self.retry))
                self.retry=0
                resp=None
                return resp
            else:
                self.get_content(url,header,timeout,proxies,maxretry)


        except exceptions.HTTPError as e:
            self.retry += 1
            self.logger.error(str(e) + "try to retry {}".format(self.retry))
            if self.retry >= maxretry:
                self.logger.error("retry =5 return None".format(self.retry))
                self.retry = 0
                resp = None
                return resp
            else:
                self.get_content(url, header, timeout, proxies, maxretry)

        except exceptions.ConnectionError as e:
            self.retry += 1
            self.logger.error(str(e) + "try to retry {}".format(self.retry))
            if self.retry >= maxretry:
                self.logger.error("retry =5 return None".format(self.retry))
                self.retry = 0
                resp = None
                return resp
            else:
                self.get_content(url, header, timeout, proxies, maxretry)

    def report(self,count, blockSize, totalSize):
            percent = int(count * blockSize * 100 / totalSize)
            sys.stdout.write("\r%d%%" % percent + ' complete')
            sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(count * blockSize * 50 / totalSize)), percent))
            sys.stdout.flush()

    def down_load_imge_video(self,url,path):
        self.logger.info("start to download")
        urllib.request.urlretrieve(url,path,reporthook=self.report)
        self.logger.info("download ok!")

