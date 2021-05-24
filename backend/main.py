from flask import Flask, request 
from flask_cors import CORS, cross_origin
import json 

import test 
import json
import train 

 
app = Flask(__name__) 
CORS(app, support_credentials=True)

@app.route('/') 
def index(): 
	return "Flask server" 
 
@app.route('/postdata', methods = ['POST']) 
def postdata(): 
    data = request.get_json() 
    print(data) 
    # do something with this data variable that contains the data from the node server 
    return json.dumps({"newdata":"hereisthenewdatayouwanttosend"}) 

@app.route('/detect', methods = ['POST']) 
def detect(): 
    data = request.get_json()
    data = json.dumps(data) #converts a Python object into a json string
    data = json.loads(data)

    b64Images = test.detect(data['img'])
    b64Images[:] = [i.decode("utf-8") for i in b64Images] #just takes out b' from string

    return json.dumps({"data" : b64Images}) 
 
@app.route('/guessAge', methods = ['POST']) 
def guessAge(): 
    data = request.get_json()
    data = json.dumps(data) #converts a Python object into a json string
    data = json.loads(data)

    # print(data['imgs'][0][-20])
    # print(data['imgs'][1][-20])
    # print(data['imgs'][2][-20])

    allAges = [train.guess('age.json', b64) for b64 in data['imgs']]
    return json.dumps({"data" : allAges}) 

@app.route('/guessGender', methods = ['POST']) 
def guessGender(): 
    data = request.get_json()
    data = json.dumps(data) #converts a Python object into a json string
    data = json.loads(data)

    allAges = [train.guess('gender.json', b64) for b64 in data['imgs']]
    return json.dumps({"data" : allAges}) 

if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5000, debug=True) 