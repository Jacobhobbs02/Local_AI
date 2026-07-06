from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.chat import Conversation
import requests

OLLAMA_URL = "http://192.168.2.180:11434/api/generate"

messages = []
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/logout')

    if request.method == "POST":
        user_input = request.form["prompt"]

        payload = {
            "model": "qwen3.5:latest",
            "prompt": user_input,
            "stream": False,
            "think": False
        }

        r = requests.post(OLLAMA_URL, json=payload)
        data = r.json()

        response_text = data.get("response", "No response")

        Conversation.save_chat({
            "prompt": user_input,
            "response": response_text,
            "user_id": session["user_id"]
        })

        return redirect('/chatroom')

    chats = Conversation.get_all_by_user(session["user_id"])
    return render_template("chat.html", chats=chats)


@app.route('/clear-chat')
def clear_chat():
    session.pop("messages", None)
    return redirect(url_for("chatroom"))
