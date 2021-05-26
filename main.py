from firebase import Firebase
from flask import Flask, jsonify, send_file, render_template, request
import time 
from flask.helpers import send_from_directory

from werkzeug.utils import redirect, secure_filename
import io
import os 

app = Flask(__name__)


config = {
    "apiKey": "AIzaSyC5dGO29bQoHThL69OmQgYw9JGuzOqOu_E",
    "authDomain": "pyflask-auth.firebaseapp.com",
    "projectId": "pyflask-auth",
    "storageBucket": "pyflask-auth.appspot.com",
    "messagingSenderId": "903763832908",
    "appId": "1:903763832908:web:127b077e082c15088e84e9",
    "databaseURL": "https://pyflask-auth-default-rtdb.firebaseio.com/"
}

firebase = Firebase(config)
# Get a reference to the auth service
auth = firebase.auth()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = auth.sign_in_with_email_and_password(username, password)
        print(user)
        return redirect("/upload", code=302)
        # if account:
        # 	session['loggedin'] = True
        # 	session['id'] = account['id']
        # 	session['username'] = account['username']
        # 	msg = 'Logged in successfully !'
        # 	return render_template('index.html', msg = msg)
        # else:
        # 	msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/event')
def event():
    return render_template('event.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        #username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(auth.create_user_with_email_and_password(email, password))
        msg = 'You have successfully registered !'
        return 'Account created'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route('/upload')
def upload_file():
  if os.path.exists("/"):
    os.remove("out.mp4")
    os.remove("song.mp3")
  print("removed files")
  return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_get():
   if request.method == 'POST':
      f = request.files['filename']
      f.save(secure_filename(f.filename))
      os.system("ffmpeg -loop 1 -i images.jpeg -i song.mp3 -c:a copy -c:v libx264 -shortest out.mp4")
      print("DOne ")
      return redirect("/come", code=302)

@app.route('/come')
def videoplayer():
    print("here")
    time.sleep(1)
    return send_from_directory(directory="", path="out.mp4")

if __name__ == '__main__':
    app.run(debug=False, port=8090, host="0.0.0.0")