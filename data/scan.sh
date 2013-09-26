#!/bin/bash

mkdir -p "headers"
mkdir -p "exclude"

TOP_SITES_FILE="alexa-top-100k-2013-09-24.csv"
CHROME_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.26"

function query {
  URL_HERE="${1}"
  FILE="${2}"

  if [ -f "headers/${FILE}" ] ; then return ; fi
  if [ -f "exclude/${FILE}" ] ; then return ; fi

  HEADERS=$(curl --user-agent "${CHROME_USER_AGENT}" "--max-time" 20 -sI "${URL_HERE}")
  RETURN_CODE="${?}"
  if [ "${RETURN_CODE}" = "0" ]
  then
    echo -e "\033[92m[+] ${URL_HERE}\033[0m"
    echo -n "${HEADERS}" > "headers/${FILE}"
  elif [ "${RETURN_CODE}" = "143" ]
  then
    # Caused by `killall curl`.
    echo -e "\033[91m[-] Aborting ${URL_HERE} (error: ${RETURN_CODE})\033[0m"
  else
    echo -e "\033[91m[-] ${URL_HERE} (error: ${RETURN_CODE})\033[0m"
    echo -n "${RETURN_CODE}" > "exclude/${FILE}"
  fi
}


function go {
  for URL in $(cat "${TOP_SITES_FILE}" | head -n ${2} | tail -n ${1} | awk -F "," "{print \$2;}")
  do

    # Filter out bad entries that are not actually domains.
    if [[ "${URL}" == *"/"* ]] ; then return ; fi

    echo "[${2}] ${URL}"
    query "http://${URL}" "http-${URL}.txt"
    query "http://www.${URL}" "http-www.${URL}.txt"
    query "https://${URL}" "https-${URL}.txt"
    query "https://www.${URL}" "https-www.${URL}.txt"
  done
}

GROUP_SIZE="100"

for i in $(seq ${GROUP_SIZE} ${GROUP_SIZE} 10000)
do
  # Take the last ${GROUP_SIZE} of the top ${i}.
  echo "${i}"
  go ${GROUP_SIZE} "${i}" &
done