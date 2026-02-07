# importing required modueles
import email
from flask import Flask, render_template, redirect, request,url_for, session, flash
import random
from database.tables import create_tables
from database.utility import addUser
from database.utility import checkUserStatus, getPasswordFromDB, updatePassword
from emailsend import emailSend
from database.utility import addNotesInDB, getNoteById, updateNoteInDB, deleteNoteFromDB
from database.utility import getNotesFromDB

from itsdangerous import URLSafeTimedSerializer
from itsdangerous import SignatureExpired, BadSignature

from werkzeug.security import check_password_hash, generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# create flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'this_is_a_secret_key'

create_tables()

# secure time based url serializer
serializer = URLSafeTimedSerializer(app.secret_key)


#home route
@app.route('/')
def home():
    return render_template('home.html')

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("EMAIL:", email)
        print("HASH FROM DB:", getPasswordFromDB(email))
        print("ENTERED PASSWORD:", password)


        if checkUserStatus(email=email):
            if check_password_hash(getPasswordFromDB(email=email), password):
                token = serializer.dumps(email, salt='login-auth')

                session['token'] = token   # ✅ STORE TOKEN
                return redirect(url_for('dashboard'))

            return render_template('login.html', msg="Invalid credentials")

        return render_template('login.html', msg="User not found")

    return render_template('login.html')



# getnerate otp token
def generate_otp_token(email):
    otp = random.randint(1000,9999)
    token = serializer.dumps(
        {"email":email, "otp":otp},
        salt = "register_otp"
    )
    return otp, token

from flask import Flask, render_template, request, session, redirect, url_for
from emailsend import emailSend  # updated SendGrid version

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['email'] = request.form['email']

        if not checkUserStatus(session['email']):
            # generate otp and token
            otp, token = generate_otp_token(session['email'])
            print("Register_otp token:", token)
            session['register_otp_token'] = token

            # Email body
            body = f"""
                Dear {session['username']},

                Welcome to Notes Management App! Please use the OTP below to verify your account:

                Verification OTP: {otp}

                This OTP expires within 2 minutes.
                Do not reply to this email.

                Best Regards,
                Notes App
                """
                            # Send OTP via SendGrid
            result = emailSend(
                to_email=session['email'],
                subject="Notes Management OTP Verification",
                body=body
            )
            print(result)  # logs success/failure

            return redirect(url_for('verifyOTP', token=session['register_otp_token']))

        return render_template('register.html', msg="Email already exists!")

    return render_template('register.html')

# verifyOTP route
@app.route("/register/verifyotp", methods=['GET','POST'])
def verifyOTP():
    if 'register_otp_token' not in session:
        return redirect(url_for('register'))
    if request.method == "POST":
        try:
            entered_otp = int(request.form['otp'])
            data = serializer.loads(
                session['register_otp_token'],
                salt = "register_otp",
                max_age = 120 # 2 mins
            )
            # verify otp
            print(data)
            print("entered otp: ", entered_otp)
            print("entered otp type: ", type(entered_otp))
            print("data otp type: ", type(data['otp']))
            print("data otp: ",data['otp'])
            print("otp match status: ", entered_otp == data['otp'])
            
            if entered_otp == data['otp']:
                # add new user to table
                
                add_user = addUser(
                    username=session['username'],
                    email= session['email'],
                    password = generate_password_hash(session['password'])

                )
                print('user added status: ', add_user)
                
                if add_user:
                    
                    session.pop('username')
                    session.pop('email')
                    session.pop('password')        
                    session.pop('register_otp_token', None)
                    return render_template('login.html', msg ='User registred successfully')
        except SignatureExpired:
            return redirect(url_for("verifyOTP", msg ='OTP Expired'))
        except BadSignature:
            return redirect(url_for("verifyOTP", msg ='Invalid OTP URL'))
        return redirect(url_for("verifyOTP", msg ='Invalid otp'))
        

    return render_template('verifyotp.html')





# -----------------------forgot password-----------------------------------
@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if checkUserStatus(email= email):
            # generating forgot password token
            token = serializer.dumps(email, salt = 'forgot-password')
            

            # generate reset link
            # reset_link = url_for('reset_password', token= token, _external = True)
            reset_link = url_for('reset_password', token=token, _external=True)

            # send reset password link via email
            body = f"""
                    Dear customer ,
                    This mail is to update notes management app password !
                    
                    Password reset link:{reset_link}

                    This link expires within 10 mins.
                    Don't replay to this email.

                    Best Regards
                    Notes App. 
                    """

            emailSend(
                to_email= email,
                subject="Notes App password reset request!",
                body = body
            )
            return redirect(url_for('login', msg = "check you email! Successfully \
                                    Password reset link send"))
        
        return redirect(url_for('login', msg = "User Email not found!!!"))

    return render_template('forgot_password.html')

@app.route('/resetPassword/<token>', methods=['GET','POST'])
def reset_password(token):
   
    # get email from token
    try:
        email = serializer.loads(token,
                             salt = 'forgot-password',
                             max_age=600)
    except SignatureExpired:
        return redirect(url_for('forgot_password', msg = "Link Expired"))
    except BadSignature:
        return redirect(url_for('forgot_password', msg = "Incorret url"))
    
    # get data from form
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)

        if updatePassword(email=email, new_password=hashed_password):
            return redirect(url_for('login', msg="Password reset successfully"))

        return redirect(url_for('login', msg = "Password not updated"))
    return render_template('reset_password.html', token=token)

# ------------------------------------


# get email from login-auth token
def verify_login_token(token):
    try:
        email = serializer.loads(
            token,
            salt = 'login-auth',
            max_age=7200
        )
        return email
    except:
        return None
    

#dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    token = session.get('token')
    if not token:
        return redirect(url_for('login', msg="Please login first"))
    email = verify_login_token(token)
    if not email:
        session.clear()
        return redirect(url_for('login', msg="Session expired"))

    # get notes from DB
    notes = getNotesFromDB(email=email) or []

    return render_template('dashboard.html', token=token, username = email, notes= notes)

## add new notes route
@app.route('/dashboard/addnotes', methods=['GET', 'POST'])
def add_notes():
    token = session.get('token')
    if not token:
        return redirect(url_for('login', msg="Please login first"))
    email = verify_login_token(token)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']


        # add notes in database
        if addNotesInDB(email=email, title=title, content=content):
        
        
            #redirect to dashboard
            return redirect(url_for("dashboard",token=token, msg = "Notes added"))
        else:
            return redirect(url_for("add_notes", msg = "Notes not updated"))

    return render_template('add_notes.html', token=token)


# update content route
@app.route('/dashboard/update/note_id=<int:note_id>', methods=['GET','POST'])
def edit_note( note_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login',msg = "Please login first"))
    email = verify_login_token(token)
    
    # get new content from app
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # update new content in DB
        updateNoteInDB(note_id=note_id,
                       email=email,
                       title=title,
                       content=content)
        return redirect(url_for('dashboard', token=token))

    # get old content from DB usinf note_id
    note = getNoteById(note_id=note_id, email=email)
    return render_template('edit_note.html', note= note, token=token)

# update content route
@app.route('/dashboard/delete/note_id=<int:note_id>/', methods=['GET','POST'])
def delete_note( note_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login',msg = "Please login first"))
    email = verify_login_token(token)
    
        # delete notes in DB
    deleteNoteFromDB(note_id=note_id, email=email)
    return redirect(url_for('dashboard', token=token))

# logout route
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login', msg = "Logged out successfully"))

if __name__ == '__main__':
    create_tables()
    app.run(debug = True, port =5004 )