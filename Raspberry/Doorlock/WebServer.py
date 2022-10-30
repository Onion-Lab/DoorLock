from flask import Flask, request
import json
import csv
from datetime import datetime
from PushMessageManager import sendMessage
from DeviceManager import doorOpen

app = Flask(__name__)

def saveCSV(user, csvPath='output.csv'):
	f = open(csvPath, 'a', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user])
	f.close()

def readCSV(csvPath='output.csv'):
	ret = []
	try:
		f = open(csvPath, 'r', encoding='utf-8', newline='')
		wr = csv.reader(f)
		for line in wr:
			ret.append({'date':line[0], 'user':line[1]})
		f.close()
	except Exception as e:
		print(e)
	finally:
		return ret

@app.route('/history', methods=['POST'])
def onHistory():
	ret = {'result': True, 'type':'history'}
	try:
		reqData = request.data.decode('utf-8')
		if reqData != '':
			data = json.loads(reqData)
		else:
			data = {}
		ret['data'] = data
	except Exception as e:
		ret['result'] = False
		ret['error'] = str(e)
	finally:
		ret['history'] = readCSV()
		return json.dumps(ret)

@app.route('/open', methods=['POST'])
def onOpen():
	ret = {'result': True, 'type':'open'}
	try:
		reqData = request.data.decode('utf-8')
		if reqData != '':
			data = json.loads(reqData)
		else:
			data = {}
		ret['data'] = data
		doorOpen()
	except Exception as e:
		ret['result'] = False
		ret['error'] = str(e)
	finally:
		saveCSV(data['user'])
		return json.dumps(ret)

@app.route('/warn', methods=['POST'])
def onwarn():
	ret = {'result': True, 'type':'warn'}
	try:
		reqData = request.data.decode('utf-8')
		if reqData != '':
			data = json.loads(reqData)
		else:
			data = {}
		ret['data'] = data
		sendMessage("warn", "미등록 사용자")
	except Exception as e:
		ret['result'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3004)
