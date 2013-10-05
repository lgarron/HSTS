import csv
import subprocess
import time

inFile = open("data/hsts_list_test.csv", "r")
inFile = open("data/hsts_list.csv", "r")
reader = csv.reader(inFile)

for row in reader:
  domain = row[0]
  time.sleep(8)
  subprocess.Popen(["phantomjs", "scan.js", "http://" + domain])
  time.sleep(8)
  subprocess.Popen(["phantomjs", "scan.js", "http://www." + domain])
  time.sleep(8)
  subprocess.Popen(["phantomjs", "scan.js", "https://" + domain])
  time.sleep(8)
  subprocess.Popen(["phantomjs", "scan.js", "https://www." + domain])
