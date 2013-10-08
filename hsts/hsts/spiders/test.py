from scrapy.spider import BaseSpider
from hsts.items import HSTSItem
import csv
import re


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

        self.start_urls = self.get_start_urls(url_file)

    def get_start_urls(self, url_file):
        urls = []

        self.regex = re.compile(r"^(https?://(www\.)?)(.*)")
        self.indices = {}
        self.indices_www = {}

        inFile = open(url_file, "r")
        reader = csv.reader(inFile)

        for i in range(1, self.start):
            print("Skipping.")
            reader.next()

        for i in range(self.num):
            row = reader.next()
            self.indices[row[1]] = row[0]
            self.indices["www." + row[1]] = row[0]
            for protocol in ["http", "https"]:
                for www in ["", "www."]:
                    urls.append(protocol + "://" + www + row[1])

        return urls

    def parse(self, response):
        item = HSTSItem()
        item["status"] = response.status
        item["hsts"] = response.headers.get("strict-transport-security", None)

        urls = response.meta.get("redirect_urls", [])
        urls.append(response.url)
        item["url"] = self.regex.sub(r"\1\3", urls[0])
        item["urls"] = urls

        domain = self.regex.sub(r"\3", urls[0])
        item["index"] = self.indices.get(domain,
            self.indices_www.get(domain, None)
        )

        return [item]
