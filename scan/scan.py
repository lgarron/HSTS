
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


# Chromium STS Headliners
go("google.com")
go("paypal.com")
go("twitter.com")
go("simple.com")
go("linode.com")
go("stripe.com")
go("lastpass.com")

# Miscellaneous
go("dropbox.com")
go("paypal.com")
go("mega.co.nz")
go("lastpass.com")
go("stripe.com")
go("squareup.com")
go("torproject.org")
go("bugzilla.mozilla.org")
go("braintreepayments.com")
go("greplin.com")

# Personal Interest
go("icloud.com")
go("worldcubeassociation.org")

# From Chrome preload list
go("paypal.com")
go("paypal.com")
go("elanex.biz")
go("jottit.com")
# go("sunshinepress.org") # doesn't exist anymore?
go("noisebridge.net")
go("neg9.org")
go("riseup.net")
go("factor.cc")
go("members.mayfirst.org")
go("support.mayfirst.org")
go("id.mayfirst.org")
go("lists.mayfirst.org")
go("webmail.mayfirst.org")
go("roundcube.mayfirst.org")
go("aladdinschools.appspot.com")
go("ottospora.nl")
go("paycheckrecords.com")
go("lastpass.com")
go("lastpass.com")
go("keyerror.com")
go("entropia.de")
go("entropia.de")
go("romab.com")
go("logentries.com")
go("logentries.com")
go("stripe.com")
go("cloudsecurityalliance.org")
go("login.sapo.pt")
go("mattmccutchen.net")
go("betnet.fr")
go("uprotect.it")
go("squareup.com")
go("square.com")
go("cert.se")
go("crypto.is")
go("include_subdomains")
go("linx.net")
go("dropcam.com")
go("dropcam.com")
go("ebanking.indovinabank.com.vn")
go("epoxate.com")
go("torproject.org")
go("blog.torproject.org")
go("check.torproject.org")
go("torproject.org")
go("dist.torproject.org")
go("moneybookers.com")
go("ledgerscope.net")
go("ledgerscope.net")
go("app.recurly.com")
go("api.recurly.com")
go("greplin.com")
go("greplin.com")
go("luneta.nearbuysystems.com")
go("ubertt.org")
go("pixi.me")
go("grepular.com")
go("mydigipass.com")
go("mydigipass.com")
go("developer.mydigipass.com")
go("developer.mydigipass.com")
go("sandbox.mydigipass.com")
go("sandbox.mydigipass.com")
go("crypto.cat")
go("bigshinylock.minazo.net")
go("crate.io")
go("twitter.com")
go("twitter.com")
go("braintreegateway.com")
go("braintreepayments.com")
go("braintreepayments.com")
go("emailprivacytester.com")
go("business.medbank.com.mt")
go("arivo.com.br")
go("apollo-auto.com")
go("cueup.com")
go("jitsi.org")
go("jitsi.org")
go("download.jitsi.org")
go("sol.io")
go("irccloud.com")
go("irccloud.com")
go("alpha.irccloud.com")
go("passwd.io")
go("browserid.org")
go("login.persona.org")
go("neonisi.com")
go("neonisi.com")
go("shops.neonisi.com")
go("piratenlogin.de")
go("howrandom.org")
go("intercom.io")
go("api.intercom.io")
go("intercom.io")
go("fatzebra.com.au")
go("csawctf.poly.edu")
go("makeyourlaws.org")
go("makeyourlaws.org")
go("iop.intuit.com")
go("surfeasy.com")
go("surfeasy.com")
go("packagist.org")
go("lookout.com")
go("lookout.com")
go("mylookout.com")
go("mylookout.com")
go("dm.lookout.com")
go("dm.mylookout.com")
go("itriskltd.com")
go("stocktrade.de")
go("openshift.redhat.com")
go("therapynotes.com")
go("therapynotes.com")
go("wiz.biz")
go("my.onlime.ch")
go("webmail.onlime.ch")
go("crm.onlime.ch")
go("gov.uk")
go("silentcircle.com")
go("silentcircle.org")
go("serverdensity.io")
go("my.alfresco.com")
go("webmail.gigahost.dk")
go("paymill.com")
go("paymill.de")
go("gocardless.com")
go("espra.com")
go("zoo24.de")
go("mega.co.nz")
go("api.mega.co.nz")
go("lockify.com")
go("writeapp.me")
go("bugzilla.mozilla.org")
go("members.nearlyfreespeech.net")
go("ssl.panoramio.com")
go("kiwiirc.com")
go("pay.gigahost.dk")
go("controlcenter.gigahost.dk")
go("simple.com")
go("simple.com")
go("fj.simple.com")
go("api.simple.com")
go("bank.simple.com")
go("bassh.net")
go("sah3.net")
go("grc.com")
go("grc.com")
go("linode.com")
go("linode.com")
go("manager.linode.com")
go("blog.linode.com")
go("library.linode.com")
go("forum.linode.com")
go("p.linode.com")
go("paste.linode.com")
go("pastebin.linode.com")
go("inertianetworks.com")
go("carezone.com")
go("conformal.com")
go("cyphertite.com")
go("logotype.se")
go("bccx.com")
go("launchkey.com")
go("carlolly.co.uk")
go("cyveillance.com")
go("blog.cyveillance.com")
go("whonix.org")
go("blueseed.co")
go("forum.quantifiedself.com")
go("shodan.io")
go("rapidresearch.me")
go("surkatty.org")
go("securityheaders.com")
go("haste.ch")
go("mudcrab.us")
go("mediacru.sh")
go("lolicore.ch")
go("cloudns.com.au")
go("oplop.appspot.com")
go("bcrook.com")
go("wiki.python.org")
go("lumi.do")
go("appseccalifornia.org")
go("crowdcurity.com")
go("saturngames.co.uk")
go("strongest-privacy.com")
