import requests
import json
import urllib
from urllib.parse import urljoin
import time

def requestPost(host, path, param):
	try:
		url = urllib.parse.urljoin(host, path)
		r = requests.post(url, json=param)
		return json.loads(r.text)
	except Exception as e:
		pass
	

if __name__ == '__main__':
	print(requestPost('http://127.0.0.1:3004', '/history', {}))
	time.sleep(1)
	print(requestPost('http://127.0.0.1:3004', '/open', {'user':'remote'}))
	time.sleep(1)
	print(requestPost('http://127.0.0.1:3004', '/history', {}))
	time.sleep(1)
	print(requestPost('http://127.0.0.1:3004', '/warn', {}))
	time.sleep(1)
