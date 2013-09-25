#!/bin/bash

ssh corn01 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh   2500 2500   50000" &
ssh corn03 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh  52500 2500  100000" &
ssh corn15 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 102500 2500  150000" &
ssh corn12 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 152500 2500  200000" &
ssh corn08 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 202500 2500  250000" &
ssh corn07 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 252500 2500  300000" &
ssh corn14 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 302500 2500  350000" &
ssh corn20 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 352500 2500  400000" &
ssh corn17 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 402500 2500  450000" &
ssh corn02 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 452500 2500  500000" &
ssh corn11 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 502500 2500  550000" &
ssh corn13 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 552500 2500  600000" &
ssh corn06 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 602500 2500  650000" &
ssh corn04 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 652500 2500  700000" &
ssh corn18 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 702500 2500  750000" &
ssh corn05 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 752500 2500  800000" &
ssh corn30 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 802500 2500  850000" &
ssh corn23 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 852500 2500  900000" &
ssh corn16 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 902500 2500  950000" &
ssh corn09 "cd ~/HSTS-chrome_1m/scan/data && ./scan.sh 952500 2500 1000000" &