#IMPORTS
from flask import render_template, redirect, session, request, flash, url_for
import requests
from flask_app import app
#from flask_app.models.user import User

OLLAMA_URL = "http://192.168.2.180:11434/api/generate"

messages = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    
    if request.method == "POST":
        user_input = request.form["prompt"]

        messages = session.get("messages", [])

        messages.append({"role": "user", "text": user_input})

        payload = {
            "model": "qwen3.5:latest",
            "prompt": user_input,
            "stream": False,
            "think": False
        }

        r = requests.post(OLLAMA_URL, json=payload)
        data = r.json()

        response_text = data.get("response", "No response")
        messages.append({"role": "ai", "text": response_text})
        session["messages"] = messages

        return redirect(url_for("chat"))

    return render_template("index.html", messages=session.get("messages", []))