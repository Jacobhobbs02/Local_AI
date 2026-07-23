from flask import render_template, redirect, session, request, flash, url_for, send_file
from flask_app import app
from flask_app.models.chat import Conversation
from flask_app.models.group import Group
import requests
import edge_tts
import asyncio
import tempfile
from langdetect import detect

OLLAMA_URL = "http://192.168.2.180:11434/api/generate"


@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/logout')

    if request.method == "POST":
        user_input = request.form["prompt"]

        group_id = request.form.get("group_id")

        if not group_id:
            group_number = Group.get_next_group_number(session['user_id'])

            group_id = Group.save_group({
            "user_id": session["user_id"],
            "group_number": group_number,
            "title": user_input
            })

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
            "user_id": session["user_id"],
            "group_id": group_id
        })

        return redirect(f'/chatroom/{group_id}')



@app.route('/rename-chat/<int:group_id>', methods=['POST'])
def rename_chat(group_id):

    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        "title": request.form["title"]
    }
   
    Group.rename_group(data,group_id)

    return redirect(request.referrer)
    

@app.route('/clear-chat/<int:group_id>', methods=['POST'])
def clear_chat(group_id):

    if 'user_id' not in session:
        return redirect('/logout')

    # Delete all conversations in this group
    Conversation.delete_by_group(group_id)

    # Delete the group
    Group.delete(group_id)

    return redirect(url_for("chatroom"))


@app.route('/tts', methods = ['POST'])
def tts():
    text = request.json.get("text", "")

    if not text:
        return {"error": "no text"}, 400

    try:
        lang = detect(text)
    except:
        lang ="en"

    voices = {
        "en": "en-US-AriaNeural",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "it": "it-IT-ElsaNeural",
        "pt": "pt-BR-FranciscaNeural",
        "ja": "ja-JP-NanamiNeural",
        "ko": "kp-KR-SunHiNeural",
        "zh-cn": "zh-CN-XiaoxiaoNeural",
        "ru": "ru-RU-SvetlanaNeural",
        "hi": "hi-IN-SwaraNeural",
        "ar": "ar-SA-ZariyahNeural"
    }
    voice = voices.get(lang, "en-US-AriaNeural")
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    filename = temp.name
    temp.close()

    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    asyncio.run(generate())
    return send_file(filename, mimetype="audio/mpeg")