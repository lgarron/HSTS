#!/bin/bash

DIR=$(dirname "${0}")
cd "${DIR}"

BATCH_SIZE="${1}"
START="${2}"

mkdir -p "data/${BATCH_SIZE}"

# To get scrapy for myths.
PATH="$PATH:~/.local/bin"

scrapy crawl hsts \
  -t json \
  -o "data/${BATCH_SIZE}/items-${START}.json" \
  -a url_file="../data/top-1m.csv" \
  -a num="${BATCH_SIZE}" \
  -a start="${START}"