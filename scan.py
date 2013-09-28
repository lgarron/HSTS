
from __future__ import print_function

import csv
import requests
import requests_cache
import re
import tldextract

from itertools import groupby
from requests.exceptions import SSLError

from collections import OrderedDict

import shelve

# Cache requests on disk.
req = requests_cache.CachedSession(
  "data/cache/requests",
  allowable_codes=range(1000), # Just cache everything (we care about 200, 301, 302).
  backend="sqlite"
)

ssl_errors = shelve.open("data/cache/ssl_errors")
excludes = shelve.open("data/cache/excludes")

print_success = False
print_exceptions = False

def exclude(e, url):
  # TODO: if failed, try only one-hop
  exceptionName = type(e).__name__
  excludes[url] = exceptionName
  if print_success: print("[adding to excludes]", url, "[", exceptionName, "]")
  return (None, exceptionName)

def load(url):

  # print("\n###", url)

  if url in excludes:
    if print_success: print("[skipping]", url)
    return (None, excludes[url])

  headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36"
  }

  try:
    r = req.get(url, headers=headers, timeout=10)
  except Exception as e:
    if not isinstance(e, SSLError):
      return exclude(e, url)
    try:
      if print_exceptions:
        print("\nSSLError:", e, "\n")
      # TODO: This still doesn't work.
      r = req.get(url, headers=headers, timeout=10, verify=False)
      ssl_errors[url] = "ignoring"
    except Exception as e2:
      if print_exceptions:
        print("\nException:", e2, "\n")
      return exclude(e2, url)

  ssl_error = " (with SSLError)" if str(url) in ssl_errors else ""
  if print_success:
    print("[success" + ssl_error + "]", url)

  return (r, None)


prefixes = OrderedDict()
prefixes["http://"] = "h"
prefixes["https://"] = "s"
prefixes["http://www."] = "hw"
prefixes["https://www."] = "sw"


def canonicalize(r, domain):
  s = re.sub(domain + ".*", "", r.url)

  hsts = ""
  # if s not in ["http://", "http://www."]:
  if "strict-transport-security" in r.headers:
    hsts += "0" if "max-age=0" in r.headers["strict-transport-security"] else "+"
    hsts += "*" if "includesubdomains" in r.headers["strict-transport-security"].lower() else ""
  else:
    hsts = "-"

  ssl_error = "!" if str(r.url) in ssl_errors else ""

  if s in prefixes:
    return hsts, ssl_error, prefixes[s]
  else:
    # return hsts, ssl_error, r.url
    return hsts, ssl_error, "Z"

def is_subdomain(domain):
  res = tldextract.extract(domain)
  return (res.subdomain not in ["", "www"])

def kind(domain):
  chains = []
  for prefix in prefixes.keys():
    r, e = load(prefix + domain)
    if hasattr(r, "status_code"):
      chain = list(r.history) + [r]

      canon = [canonicalize(h, domain) for h in chain]

      # Remove redundant redirects (from an HSTS perspective):
      canon = [i[0] for i in groupby(canon)]

      chains.append(canon)
    else:
      # chains.append("[" + e + "]")
      chains.append([["", "", "X"]])
  return chains

def go(domain):
  k = kind(domain)
  # print(k)
  def brac(s):
    return "[%s]" % s
  kind_end = "".join([brac([canon[-1] for canon in chain][-1]) for chain in k])
  kind_plain = "".join([brac(" ".join([canon[-1] for canon in chain])) for chain in k])
  kind_hsts = "".join([brac(" ".join(["".join(canon) for canon in chain])) for chain in k])
  sub = "sub" if is_subdomain(domain) else "top"
  print(kind_end + "," + kind_plain + "," + kind_hsts + "," + sub + "," + domain)

inFile = open("data/hsts_list_test.csv", "r")
inFile = open("data/hsts_list.csv", "r")
reader = csv.reader(inFile)

for row in reader:
  domain = row[0]
  go(domain)
