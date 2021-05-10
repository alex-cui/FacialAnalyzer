from flask import Flask, request 
from flask_cors import CORS, cross_origin
import json 

import test 
import json

 
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

    # print(data) #finally has img url
    print(data['img'][0:100]) #finally has img url

    success = test.detect(data['img'])
    print("DONE")

    # do something with this data variable that contains the data from the node server 
    return json.dumps({"newdata":"hereisthenewdatayouwanttosend"}) 
 
if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5000, debug=True) 