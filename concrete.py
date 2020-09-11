from flask import Flask, render_template, request, redirect, url_for,session, jsonify
import urllib
import json
import logging
import ast

url = 'https://ussouthcentral.services.azureml.net/workspaces/94ada53799214ed7b2fb687409803d11/services/417b8891fcd64cb9a8b9d6dee3fd76ed/execute?api-version=2.0&details=true'
api_key = 'GnVciB6/whhhahJmrOg2BiRqOzkguZkJRSJ3DNS1E8rWjXSsxJTTGrT2DQMIdWPEVsMfwscikWgBV7ccfcaueA=='
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

request_data = {
  "Inputs": {
    "input1": {
      "ColumnNames": [
        "Cement (component 1)(kg in a m^3 mixture)",
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)",
        "Fly Ash (component 3)(kg in a m^3 mixture)",
        "Water  (component 4)(kg in a m^3 mixture)",
        "Superplasticizer (component 5)(kg in a m^3 mixture)",
        "Coarse Aggregate  (component 6)(kg in a m^3 mixture)",
        "Fine Aggregate (component 7)(kg in a m^3 mixture)",
        "Age (day)",
        "Concrete compressive strength(MPa, megapascals)"
      ],
      "Values": [
        [
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ]
      ]
    }
  },
  "GlobalParameters": {}
}

app=Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    raw_response = request.form.items()
    response = get_values_from_form_response(raw_response)
    body = str.encode(json.dumps(set_values_for_azure_request(response)))
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        data = json.loads(result.decode("UTF-8")) 
        grade = get_grade_from_response(data)
        return render_template('home.html', grade = grade)
    except urllib.error.HTTPError as error: 
        logging.warning("The request failed with status code: " + str(error.code))
        logging.warning(error.info())
        logging.warning(json.loads(error.read())) 
    return ""

def get_values_from_form_response(response):
    cement_characteristics = {}
    i = 0
    for item in response:
        if i == 0:
            cement_characteristics["Cement"] = item[1]
        if i == 1:
            cement_characteristics["Blast Furnace Slag"] = item[1]
        if i == 2:
            cement_characteristics["Fly Ash"] = item[1]
        if i == 3:
            cement_characteristics["Water"] = item[1]
        if i == 4:
            cement_characteristics["Superplasticizer"] = item[1]
        if i == 5:
            cement_characteristics["Coarse Aggregate"] = item[1]
        if i == 6:
            cement_characteristics["Fine Aggregate"] = item[1]
        if i == 7:
            cement_characteristics["Age"] = item[1]
        if i == 8:
            cement_characteristics["Concrete compressive strength"] = item[1]
        i = i + 1
    return cement_characteristics
        
def get_grade_from_response(response):
    raw_grade = response['Results']['output1']['value']['Values']
    return raw_grade[0][0]

def set_values_for_azure_request(data):
    request_data["Inputs"]["input1"]["Values"][0][0] = data["Cement"]
    request_data["Inputs"]["input1"]["Values"][0][1] = data["Blast Furnace Slag"]
    request_data["Inputs"]["input1"]["Values"][0][2] = data["Fly Ash"]
    request_data["Inputs"]["input1"]["Values"][0][3] = data["Water"]
    request_data["Inputs"]["input1"]["Values"][0][4] = data["Superplasticizer"]
    request_data["Inputs"]["input1"]["Values"][0][5] = data["Coarse Aggregate"]
    request_data["Inputs"]["input1"]["Values"][0][6] = data["Fine Aggregate"]
    request_data["Inputs"]["input1"]["Values"][0][7] = data["Age"]
    request_data["Inputs"]["input1"]["Values"][0][8] = data["Concrete compressive strength"]
    return request_data

if __name__ == "main":
    app.run()