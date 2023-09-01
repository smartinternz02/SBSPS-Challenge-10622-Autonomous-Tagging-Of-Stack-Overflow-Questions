# app.py
from flask import Flask, request, render_template, jsonify
import requests
from application.loader import predict_tags, renew_token, process_data
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_tags', methods = ['POST'])
def predict():
	if request.is_json:
		data = request.get_json()
		question = data.get('title', '')
		description = data.get('body', '')
		selected_option = data.get('model', '')
		tags = predict_tags(question, description, selected_option)
		
	else:
		question = request.form["question"]
		description = request.form["describe"]
		selected_option = request.form.get('option')

		tags = predict_tags(question, description, selected_option)

	return tags


@app.route('/process_quora_form', methods=['POST'])
def process_quora_form():
		question = request.form['quora_question']
		description = request.form['quora_description']
		text = question+" "+description
		tags = process_data(text)
		return tags	
		

scheduler = BackgroundScheduler()
if __name__ == "__main__":
	
	scheduler.add_job(renew_token, 'interval', hours=0.967)
	scheduler.start()
	app.run(host="0.0.0.0", port=5000)


