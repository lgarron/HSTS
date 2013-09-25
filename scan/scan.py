
from __future__ import print_function

import csv
import requests
import requests_cache

import shelve

# Cache requests on disk.
requests_cache.install_cache(
  "data/cache",
  allowable_codes=range(1000), # Just cache everything (we care about 200, 301, 302).
  backend="sqlite"
)

excludes = shelve.open("data/excludes")

def load(url):

  print("\n###", url)

  if url in excludes:
    print("[skipping]", url)
    return

  headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36"
  }

  try:
    r = requests.get(url, allow_redirects=False, headers=headers, timeout=3)
    print("[success]", url)
  except:
    excludes[url] = "exclude"
    print("[adding to excludes]", url)
    return

  print("status:", r.status_code)

  for key in ["strict-transport-security",
              "location",
              "pragma",
              "cache-control"]:
    try:
      print(key + ":", r.headers[key])
    except:
      pass

def go(base_url):
  for protocol in ["http", "https"]:
    for subdomain in ["www.", ""]:
      load(protocol + "://" + subdomain + base_url)

inFile = open("data/hsts_list.csv", "r")
reader = csv.reader(inFile)

for row in reader:
  domain = row[0]
  go(domain)
