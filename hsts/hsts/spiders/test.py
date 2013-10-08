from scrapy.spider import BaseSpider
from hsts.items import HSTSItem
from scrapy.http import Request
import csv
import re
import itertools


class MySpider(BaseSpider):
    name = 'hsts'
    handle_httpstatus_list = range(1000)

    def __init__(self,
            url_file="../data/alexa-top-100k-2013-09-24.csv",
            start=1,
            num=1000,
            *args, **kwargs):

        super(MySpider, self).__init__(*args, **kwargs)

        try:
            self.start = int(start)
        except:
            pass

        try:
            self.num = int(num)
        except:
            pass

        self.url_file = url_file

    def start_requests(self):
        inFile = open(self.url_file, "r")
        reader = csv.reader(inFile)
        l = []

        for i in range(self.start - 1):
            # Drop the item.
            reader.next()

        for index, url in itertools.islice(reader, self.num):
            for protocol in ["http", "https"]:
                for www in ["", "www."]:
                    l.append(Request(
                        protocol + "://" + www + url,
                        meta={
                            "index": index,
                            "url": url,
                            "protocol": protocol,
                            "www": www
                        }
                    ))

        return l

    def parse(self, response):
        item = HSTSItem()
        item["status"] = response.status
        item["hsts"] = response.headers.get("strict-transport-security", None)
        item["location"] = response.headers.get("location", None)

        # urls = response.meta.get("redirect_urls", [])
        # urls.append(response.url)
        item["url"] = response.meta["url"]
        # item["urls"] = urls

        item["index"] = response.meta["index"]
        item["protocol"] = response.meta["protocol"]
        item["www"] = response.meta["www"]

        return [item]
