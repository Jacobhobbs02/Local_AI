#IMPORTS
from flask import render_template, redirect, session, request, flash, url_for
import requests
from flask_app import app
#from flask_app.models.user import User

OLLAMA_URL = "http://192.168.2.180:11434/api/generate"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods={'GET', 'POST'})
def chat():
    response_text = ""

    if request.method == "POST":
        user_input = request.form["prompt"]

        payload = {
            "model": "qwen3.5:latest",
            "prompt": user_input,
            "stream": False
        }

        r = requests.post(OLLAMA_URL, json=payload)
        data = r.json()

        response_text = data.get("response", "No response")

    return render_template("index.html", response = response_text)