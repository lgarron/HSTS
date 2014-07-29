# State of HSTS on the Web

## Running

    pip install requests requests_cache tldextract
    git clone -b scan https://github.com/lgarron/HSTS.git && cd HSTS
    python scan.py


## Interpretation

  - `h`:  `http://example.com`
  - `hw`: `http://example.com`
  - `s`:  `https://www.example.com`
  - `sw`: `https://example.com`
  - `-`: no HSTS
  - `0`: sends HSTS with `max-age` 0
  - `*`: sends `includeSubDomains` with HSTS
  - `top` vs. `sub`: Top of site domain vs. subdomain (based on the [Public Suffix List](https://publicsuffix.org/) using `tldextract`)


## Sample Data

Each set of brackets denotes the chain of redirects, starting from `h`, `s`, `hw`, and `sw`, respectively.

    [-h +s +*sw][+s][-hw +*sw][+*sw],top,dropbox.com
    [+h +s][+s][-hw +s][-sw +s],top,duckduckgo.com
    [-h -hw][-s -hw][-hw][0*sw -hw],top,etsy.com
    [-h -hw 0sw][-s 0sw][-hw][0sw],top,facebook.com
    [-h +s][+s][+hw +s][+sw +s],top,foursquare.com
    [-h +s][+s][-hw +s][-sw +s],top,github.com
    [-h +*sw][-s +*sw][-hw +*sw][+*sw],top,icloud.com
    [-h 0hw][-s 0hw][0hw][0sw],top,intuit.com
    [-h +s][+s][-hw +s][+sw],top,mega.co.nz
    [-h +s -hw +sw][+s][-hw][+sw],top,odesk.com
    [-h +s +sw -sw][+s][X][+sw],top,paypal.com
    [0h 0hw][0s 0hw][0hw][0sw 0hw],top,prestashop.com
    [-h][0s][-hw][+sw],top,t.co
    [-h +s][+s][-hw +s][+sw +s],top,twitter.com
    [-h -hw][-s +sw][-hw][+sw],top,zoho.com


