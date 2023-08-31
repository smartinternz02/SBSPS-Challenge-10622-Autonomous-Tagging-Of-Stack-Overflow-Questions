# app.py
from flask import Flask, request, render_template, jsonify
import requests
from application.loader import predict_tags, renew_token, process_data
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


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

scheduler = BackgroundScheduler()
if __name__ == "__main__":
	
	scheduler.add_job(renew_token, 'interval', hours=0.967)
	scheduler.start()
	app.run(host="0.0.0.0", port=5000)


