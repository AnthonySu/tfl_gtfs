import gzip
import json
from pprint import pprint
import glob

for file in glob.glob("*.json.gz"):
	file_s = gzip.open(file)
	results = json.load(file_s)
	print(len(results))
	pprint(results[2])