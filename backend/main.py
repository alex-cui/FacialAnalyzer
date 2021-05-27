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
 
#test request
@app.route('/postdata', methods = ['POST']) 
def postdata(): 
    data = request.get_json() 
    print(data) 
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

    ret = [train.guess('age.json', b64) for b64 in data['imgs']]
    return json.dumps({"data" : ret}) 

@app.route('/guessGender', methods = ['POST']) 
def guessGender(): 
    data = request.get_json()
    data = json.dumps(data) #converts a Python object into a json string
    data = json.loads(data)

    ret = [train.guess('gender.json', b64) for b64 in data['imgs']]
    return json.dumps({"data" : ret}) 

@app.route('/guessCelebrity', methods = ['POST']) 
def guessCelebrity(): 
    data = request.get_json()
    data = json.dumps(data) #converts a Python object into a json string
    data = json.loads(data)

    ret = [train.guess('new_celeb.json', b64) for b64 in data['imgs']]
    return json.dumps({"data" : ret}) 

if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5000, debug=True) 