#IMPORTS
from flask import render_template, redirect, session, request, flash, url_for
import requests
from flask_app import app
from flask_app.models.user import User
from flask_app.models.chat import Conversation
from flask_app.models.group import Group
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import threading
import random
import string
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# Serializer for generating secure tokens (e.g., email confirmation) 
s = URLSafeTimedSerializer(app.secret_key)

def send_email(to, subject, template):
    import smtplib, ssl
    from email.mime.text import MIMEText

    msg = MIMEText(template, "html")
    msg["Subject"] = subject
    msg["From"] = "skierschoice.ai@gmail.com"
    msg["To"] = to

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("skierschoice.ai@gmail.com", "keqb tqye bedx mpva")
        server.sendmail("skierschoice.ai@gmail.com", to, msg.as_string())



#Generating Temporary Passwords 
def generate_random_password(length=25):
    #Generate a random password
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/new_account', methods=['GET'])
def new_account():
    return render_template('registration.html')


# Registering Accounts to db
@app.route('/register', methods=['GET', 'POST'])
def register():
    # User Validation
    if not User.validate_user(request.form):
        return redirect('/new_account')

    if request.method == 'POST':
        email = request.form['email']

        #Grab randomly generated temporary password
        generated_password = generate_random_password()

        # Checks if User exists in db
        user = User.get_by_email({'email': email})
        if user:
            flash("This account already exists!")
            return redirect('/new_account')

        #Saving user data
        data = {
            "full_name": request.form['full_name'],
            "email": request.form['email'],
            "password": generated_password
        }

        # Saving User Data in db
        id = User.save(data)
        session['user_id'] = id

        #Generating Token for 'Confirm Email'
        token = s.dumps(email, salt='password-reset-salt')
        confirm_url = url_for('new_password_page', token=token, _external=True, _scheme='http')

        #Email Format
        html = render_template('Email/confirm_account_email.html', confirm_url=confirm_url)
        subject = 'Confirm Your Email'
        threading.Thread(target=send_email, args=(email, subject, html)).start()

        flash("Account created successfully! Check email to activate it!")
        return redirect('/')


#Login Code
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if user exists
        email = request.form['email']
        user = User.get_by_email({'email': email})

        if not user:
            flash("Invalid Email")
            return redirect('/')

        # Check if password matches
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Invalid Password")
            return redirect('/')

        # User session creation after successful login
        session['user_id'] = user.id
        return redirect('/chatroom')

    # If it's a GET request, show the login page
    return render_template('login.html')

#Chatroom Page 
@app.route('/chatroom', methods=['GET'])
def chatroom():

    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }
    #User who logged in
    user = User.get_one(data)

    #All groups linked to those conversations
    all_groups = Group.get_all_by_user(session['user_id'])
    return render_template("chat.html", user=user, groups=all_groups)

#Logout Method
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/chatroom/<int:group_id>')
def group_chat(group_id):

    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': session['user_id']
    }

    user = User.get_one(data)

    group = Group.get_one({
        "id": group_id
    })

    chats = Conversation.get_all_by_group(group_id)

    groups = Group.get_all_by_user(session['user_id'])

    return render_template("group.html",user=user,group=group,chats=chats,groups=groups)



@app.route('/update/<users_id>', methods=['POST'])
def update_user_information(users_id):

    if 'user_id' not in session:
        return redirect('/logout')
    
    # Validate user input
    if not User.validate_user(request.form):
        return redirect("/update/information")
    
    # Prepare data for updating the user
    data = {
        "full_name": request.form['full_name'],
        "email": request.form['email']
    }

    # Update user information in the database
    User.update_user(data, users_id)
    flash("Account Updated Successfully!")
    return redirect('/chatroom')

@app.route("/delete_account/<user_id>", methods=['POST'])
def delete_account(user_id):
    User.delete_account(user_id)
    return redirect("/")

#PASSWORD CODE ---------------------------------------------------------------------------->

#Forgot Password Page
@app.route('/forgot_password')
def forgot_password():
    return render_template("Password/forgot_password.html")

#Resetting Password Code
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    #Input what account password the user wants to reset
    if request.method == 'POST':
        #Check if the user exists
        email = request.form['email'] 
        user = User.get_by_email({'email': email})

        #If User exists, send email to their email
        if user:
            #Generate Token and Where User will go after clicking link
            token = s.dumps(user.email, salt='password-reset-salt')
            confirm_url = url_for('new_password_page', token=token, _external=True, _scheme='http')

            #Email Format
            html = render_template('Email/reset_password_email.html', confirm_url=confirm_url)
            subject = 'Reset Your Password'
            threading.Thread(target=send_email, args=(email, subject, html)).start()
            flash('A password reset link has been sent to your email!', 'info')
            return redirect(url_for('forgot_password'))

        
        #If User doesn't exist
        else:
            flash('No user found with that email address.', 'danger')
            return redirect(url_for('forgot_password'))
    return render_template('Password/forgot_password.html')

#New Password Page
@app.route('/new_password_page/<token>', methods=['GET'])
def new_password_page(token):
    # Render the password reset form
    return render_template('Password/new_password.html', token=token)


#New Password Code
@app.route('/new_password/<token>', methods=['POST'])
def new_password(token):
    #Password Validation
    if not User.validate_password(request.form):
        return render_template('Password/new_password.html', token=token)

    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired.')
        return redirect('/reset_password')
    except BadSignature:
        flash('Invalid password reset link.')
        return redirect('/reset_password')

    #If everything is good with form, update the user's password
    new_password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    #Get User
    user = User.get_by_email({'email': email})
    if user:
        User.update_password({'email': email, 'password': hashed_password})
        flash('Your password has been updated!', 'success')
        return redirect('/')

    #If something goes wrong, re-render the password form
    return render_template('Password/new_password.html', token=token)
