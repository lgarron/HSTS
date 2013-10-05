from scrapy.spider import BaseSpider
from hsts.items import HSTSItem
import csv
import re

from scrapy.contrib.downloadermiddleware.redirect import RedirectMiddleware


def process_response(self, request, response, spider):
    if 'dont_redirect' in request.meta:
        return response

    print "HI there."

    if request.method == 'HEAD':
        if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = request.replace(url=redirected_url)
            print(type(request))
            return self._redirect(redirected, request, spider, response.status)
        else:
            return response

    if response.status in [302, 303] and 'Location' in response.headers:
        redirected_url = urljoin(request.url, response.headers['location'])
        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)

    if response.status in [301, 307] and 'Location' in response.headers:
        redirected_url = urljoin(request.url, response.headers['location'])
        redirected = request.replace(url=redirected_url)
        return self._redirect(redirected, request, spider, response.status)

    return response

RedirectMiddleware.process_response = process_response


class MySpider(BaseSpider):
    name = 'hsts'

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

        self.regex = re.compile(r"^(https?://(www\.)?)([^/]*)(/.*)?")
        self.indices = {}

        inFile = open(url_file, "r")
        reader = csv.reader(inFile)

        for i in range(1, self.start):
            print("Skipping.")
            reader.next()

        for i in range(self.num):
            row = reader.next()
            self.indices[row[1]] = row[0]
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
        item["index"] = self.indices.get(domain, None)

        return [item]
