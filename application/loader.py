#loader.py

from application.config import deployment
import pickle
from flask import jsonify
import sklearn
import numpy as np
import requests
import spacy


def renew_token():
	print(" * Renewing token...")
	API_KEY = deployment()
	global mltoken
	token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
	API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
	mltoken = token_response.json()["access_token"]
	header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

renew_token()	
	
def svc(payload_scoring):
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d46ed297-5fe9-4e85-9aec-bd06b0000b2b/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
	return response_scoring
		

def pac(payload_scoring):
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0b1bc98d-ebb6-4ede-91d1-a6f14bd6a327/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
	return response_scoring

def mlpc(payload_scoring):
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a73d1dde-4375-4eab-9922-9f3ec2e6b227/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
	return response_scoring
	
def percep(payload_scoring):
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d2203452-dfe0-4fbf-98cc-2e4af676a0d3/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
	return response_scoring
	
def logistic(payload_scoring):
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e4432a94-807a-40e0-bc2d-6e9a3645d471/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
	return response_scoring
	
import re
from bs4 import BeautifulSoup
def clean_text(text):
	text = BeautifulSoup(text, features="html.parser").get_text()
	text = re.sub("[^a-zA-Z]", " ", text)
	text = text.lower()
	tokens = text.split()
	return " ".join(tokens)

multilabel = pickle.load(open("static/multi_label.pkl", 'rb'))
def choose_model(model, payload_scoring):
	if(model=="svc"):
		response_scoring = svc(payload_scoring)
	elif(model=="pac"):
		response_scoring = pac(payload_scoring)
	elif(model=="mlpc"):
		response_scoring = mlpc(payload_scoring)
	elif(model=="percep"):
		response_scoring = percep(payload_scoring)
	elif(model=="lr"):
		response_scoring = logistic(payload_scoring)
	else:
		return {"error": "Wrong 'model' parameter"}
	
	response_data = response_scoring.json()
	original_predictions = response_data
	values = original_predictions['predictions'][0]['values'][0][0]
	numpy_array = np.array(values)
	desired_shape = (1, -1)
	reshaped_array = numpy_array.reshape(desired_shape)
	output = multilabel.inverse_transform(reshaped_array)
	return output[0]
    
def predict_tags(question, description, model):
	question = clean_text(question)
	description = clean_text(description)

	
	x1 = [question]
	x2 = [question+" "+description]
		

	payload_scoring_que = {"input_data": [{"field": [x1], "values": [x1]}]}
	payload_scoring_desc = {"input_data": [{"field": [x2], "values": [x2]}]}
	
	
	tags = choose_model(model, payload_scoring_que)
	if description:
		tags2 = choose_model(model, payload_scoring_desc)
		tags = list(set(tags) | set(tags2))
		
	tags = jsonify(tags)
	return tags, 200
	
	

nlp = spacy.load('en_core_web_md')

def process_data(text):
	doc = nlp(text)
	tags = [token.text.lower() for token in doc if token.pos_ in ('NOUN', 'PROPN')]
	tags = list(set(tags))
	tags = tags[:5]
	print(tags)
	return jsonify(tags), 200
	
