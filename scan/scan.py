
from __future__ import print_function

import csv
import requests
import requests_cache
import re

from itertools import groupby

from collections import OrderedDict

import shelve

# Cache requests on disk.
requests_cache.install_cache(
  "data/cache",
  allowable_codes=range(1000), # Just cache everything (we care about 200, 301, 302).
  backend="sqlite"
)

excludes = shelve.open("data/excludes")

print_success = False

def load(url):

  # print("\n###", url)

  if url in excludes:
    if print_success: print("[skipping]", url)
    return (None, excludes[url])

  headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36"
  }

  try:
    r = requests.get(url, headers=headers, timeout=10)
    if print_success: print("[success]", url)
  except Exception as e:
    # TODO: if failed, try only one-hop
    exceptionName = type(e).__name__
    excludes[url] = exceptionName
    if print_success: print("[adding to excludes]", url, "[", exceptionName, "]")
    return (None, exceptionName)

  return (r, None)

prefixes = OrderedDict()
prefixes["http://"] = "h"
prefixes["http://www."] = "hw"
prefixes["https://"] = "s"
prefixes["https://www."] = "sw"


def canonicalize(r, domain):
  s = re.sub(domain + ".*", "", r.url)

  hsts = ""
  if s not in ["http://", "http://www."]:
    if "strict-transport-security" in r.headers:
      hsts = "+"
    else:
      hsts = "-"

  if s in prefixes:
    return hsts + prefixes[s]
  else:
    return hsts + r.url


def go(domain):
  chains = []
  for prefix in prefixes.keys():
    r, e = load(prefix + domain)
    if hasattr(r, "status_code"):
      chain = list(r.history) + [r]

      canon = [canonicalize(h, domain) for h in chain]
      # Remove redundant redirects (from an HSTS perspective):
      canon = [i[0] for i in groupby(canon)]

      chains.append("[" + (" ".join(canon)) + "]")
    else:
      # chains.append("[" + e + "]")
      chains.append("[X]")
  print("".join(chains) + "," + domain)

inFile = open("data/hsts_list_test.csv", "r")
inFile = open("data/hsts_list.csv", "r")
reader = csv.reader(inFile)

for row in reader:
  domain = row[0]
  go(domain)
