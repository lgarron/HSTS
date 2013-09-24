from __future__ import print_function
import requests


def load(url):

  print("\n###", url);
  r = requests.get(url, allow_redirects=False)

  print("status:", r.status_code)

  for key in ["strict-transport-security", "location", "pragma", "cache-control"]:
    try:
      print(key + ":", r.headers[key])
    except:
      pass

def go(base_url):
  for protocol in ["http", "https"]:
    for subdomain in ["www.", ""]:
      load(protocol + "://" + subdomain + base_url)

go("dropbox.com")
go("paypal.com")
go("stripe.com")
go("squareup.com")
go("lastpass.com")
go("mega.co.nz")