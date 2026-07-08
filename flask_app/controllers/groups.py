#IMPORTS
from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.chat import Conversation
from flask_app.models.group import Group


#Group Pages
@app.route('/chatroom/<int:group_id>')
def groups(group_id):

    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }
    #User who logged in
    user = User.get_one(data)

    #All the conversation a user has had
    all_chats = Conversation.get_all_by_group(group_id)

    #All groups linked to those conversations
    all_groups = Group.get_all_by_user(session['user_id'])
    return render_template("chat.html", user=user, chats=all_chats, groups=all_groups)



