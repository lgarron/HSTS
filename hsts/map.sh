#!/bin/bash

ssh corn15 "~/HSTS/HSTS/hsts/worker.sh 10000 00001" &
ssh corn29 "~/HSTS/HSTS/hsts/worker.sh 10000 10001" &
ssh corn24 "~/HSTS/HSTS/hsts/worker.sh 10000 20001" &
ssh corn17 "~/HSTS/HSTS/hsts/worker.sh 10000 30001" &
ssh corn21 "~/HSTS/HSTS/hsts/worker.sh 10000 40001" &
ssh corn28 "~/HSTS/HSTS/hsts/worker.sh 10000 50001" &
ssh corn30 "~/HSTS/HSTS/hsts/worker.sh 10000 60001" &
ssh corn25 "~/HSTS/HSTS/hsts/worker.sh 10000 70001" &
ssh corn27 "~/HSTS/HSTS/hsts/worker.sh 10000 80001" &
ssh corn11 "~/HSTS/HSTS/hsts/worker.sh 10000 90001" &
