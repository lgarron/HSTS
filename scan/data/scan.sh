#!/bin/bash

mkdir -p "results"
mkdir -p "done"

TOP_SITES_FILE="alexa-top-1m-2013-09-24.csv"
CHROME_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.26"

function query {
  URL_HERE="${1}"
  FILE="${2}"
  GROUP="${3}"

  HEADERS=$(curl --user-agent "${CHROME_USER_AGENT}" "--max-time" 5 -sI "${URL_HERE}" | grep -i "strict-transport-security")
  RETURN_CODE="${?}"
  if [ "${RETURN_CODE}" = "0" ]
  then
    echo -e "\033[92m[+] ${URL_HERE}\033[0m"
    echo "${URL_HERE}" >> "results/secures-${GROUP}.txt"
  else
    echo -e "\033[91m[-] ${URL_HERE} (error: ${RETURN_CODE})\033[0m"
    echo "${URL_HERE}" >> "results/non-secures-${GROUP}.txt"
  fi
}


function go {
  for URL in $(cat "${TOP_SITES_FILE}" | head -n ${2} | tail -n ${1} | awk -F "," "{print \$2;}")
  do

    # Filter out bad entries that are not actually domains.
    if [[ "${URL}" == *"/"* ]] ; then return ; fi

    echo "[${2}] ${URL}"
    query "http://${URL}" "http-${URL}.txt" "${2}"
    query "http://www.${URL}" "http-www.${URL}.txt" "${2}"
    query "https://${URL}" "https-${URL}.txt" "${2}"
    query "https://www.${URL}" "https-www.${URL}.txt" "${2}"
  done

  touch "done/${2}.txt"
}

START="${1}" # 2500
GROUP_SIZE="${2}" # 2500
END="${3}" # 1000000

for i in $(seq ${START} ${GROUP_SIZE} ${END})
do
  # Take the last ${GROUP_SIZE} of the top ${i}.
  echo "${i}"
  go ${GROUP_SIZE} "${i}" &
done
