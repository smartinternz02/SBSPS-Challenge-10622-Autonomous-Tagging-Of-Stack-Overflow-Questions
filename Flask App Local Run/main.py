import numpy as np
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import pickle
import requests

import spacy

nlp = spacy.load('en_core_web_md')

def process_data(text):
	doc = nlp(text)
	tags = [token.text.lower() for token in doc if token.pos_ in ('NOUN', 'PROPN')]
	tags = list(set(tags))
	tags = tags[:5]
	print(tags)
	return jsonify(tags), 200
	
	
import re
def clean_text(text):
	text = text.lower()
	text = re.sub(r"what's", "what is ", text)
	text = re.sub(r"\'s", " ", text)
	text = re.sub(r"\'ve", " have ", text)
	text = re.sub(r"can't", "can not ", text)
	text = re.sub(r"n't", " not ", text)
	text = re.sub(r"i'm", "i am ", text)
	text = re.sub(r"\'re", " are ", text)
	text = re.sub(r"\'d", " would ", text)
	text = re.sub(r"\'ll", " will ", text)
	text = re.sub(r"\'scuse", " excuse ", text)
	text = re.sub(r"\'\n", " ", text)
	text = re.sub(r"\'\xa0", " ", text)
	text = re.sub('\s+', ' ', text)
	text = text.strip(' ')
	return text
    
    

tfidf = pickle.load(open('models/tf_idf.pkl', 'rb'))
multilabel = pickle.load(open('models/multi_label.pkl', 'rb'))   
def predict_tags(question, description, model):
	
	if(model=="svc"):
		model = pickle.load(open('models/svcclf2.pkl', 'rb'))
	elif(model=="pac"):
		model = pickle.load(open('models/pacclf.pkl', 'rb'))
	elif(model=="mlpc"):
		model = pickle.load(open('models/mlpc.pkl', 'rb'))
	elif(model=="percep"):
		model = pickle.load(open('models/percep.pkl', 'rb'))
	elif(model=="lr"):
		model = pickle.load(open('models/logistic.pkl', 'rb'))
	else:
		return {"error": "Wrong 'model' parameter"}

	question = clean_text(question)

	describe = clean_text(description)


	x = [question]
	output = model.predict(tfidf.transform(x))
	output = multilabel.inverse_transform(output)
	tags1 = output[0]

	x = [question+" "+describe]
	output = model.predict(tfidf.transform(x))
	output = multilabel.inverse_transform(output)
	tags2 = output[0]

	tags = list(set(tags1) | set(tags2))
	
	return tags



@app.route('/')
def home():
    return render_template('index.html')
 
 
@app.route('/get_tags', methods = ['GET', 'POST'])
def predict():
	if request.method == 'GET':
		question = request.args.get("question")
		description = request.args.get("description")
		selected_option = request.args.get('model')
		if question is None:
		    return jsonify({"error": "Missing 'question' parameter"}), 400
		if description is None:
			description = ""
		if selected_option is None:
			selected_option = 'svc'
		tags = predict_tags(question, description, selected_option)

		return tags
		

	elif request.method == 'POST':
		question = request.form["question"]
		description = request.form["describe"]
		selected_option = request.form.get('option')

		tags = predict_tags(question, description, selected_option)

		return tags


@app.route('/process_quora_form', methods=['GET', 'POST'])
def process_quora_form():
	if request.method == 'GET':
		question = request.args.get('question')
		description = request.args.get('description')
		if question is None:
		    return jsonify({"error": "Missing 'question' parameter"}), 400
		if description is None:
			description = ""
		text = question + " " + description
		tags = process_data(text)
		return tags
	elif request.method == 'POST':
		question = request.form['quora_question']
		description = request.form['quora_description']
		text = question+" "+description
		tags = process_data(text)
		return tags	
	

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
