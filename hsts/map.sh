#!/bin/bash

ssh corn24 "~/HSTS/HSTS/hsts/worker.sh 100000 000001" &
ssh corn27 "~/HSTS/HSTS/hsts/worker.sh 100000 100001" &
ssh corn23 "~/HSTS/HSTS/hsts/worker.sh 100000 200001" &
ssh corn30 "~/HSTS/HSTS/hsts/worker.sh 100000 300001" &
ssh corn29 "~/HSTS/HSTS/hsts/worker.sh 100000 400001" &
ssh corn26 "~/HSTS/HSTS/hsts/worker.sh 100000 500001" &
ssh corn28 "~/HSTS/HSTS/hsts/worker.sh 100000 600001" &
ssh corn19 "~/HSTS/HSTS/hsts/worker.sh 100000 700001" &
ssh corn03 "~/HSTS/HSTS/hsts/worker.sh 100000 800001" &
ssh corn11 "~/HSTS/HSTS/hsts/worker.sh 100000 900001" &