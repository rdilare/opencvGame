import json
import datetime as dt
from os import path

def getScore():
	dirname = path.dirname(path.realpath(__file__))
	with open(path.join(dirname,"scores.txt"),"r") as f:
		f.seek(0)
		data = json.loads(f.read())
		f.close()
		data.sort(key = lambda i:i["score"], reverse=True)
	return data

	# dirname = path.dirname(path.realpath(__file__))
def saveScore(score):
	dirname = path.dirname(path.realpath(__file__))
	print(dirname)
	date = dt.datetime.now()
	with open(path.join(dirname,"scores.txt"),"r") as f:
		f.seek(0)
		x = json.loads(f.read())
		f.close()

		x.append({"date":date.strftime("%d-%b %Y"), "score":score})
		x.sort(key = lambda i:i["score"], reverse=True)

		if len(x)>5:x=x[:5]
		
		y = json.dumps(x)

		f = open(path.join(dirname,"scores.txt"),"w")
		f.write(y)
		f.close()
