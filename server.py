from asyncore import read
from datetime import datetime
from flask import Flask, render_template_string,session,redirect,url_for,request,flash, render_template
import sqlite3
from checker import check_for_name_in_db
import uuid
import os
import shutil
import random

con = sqlite3.connect("db.sql")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT,Bio TEXT, perms TEXT)")
con.commit()
con.close()
blogs = []



app = Flask(__name__)
app.secret_key = '110322170707230807'

def get_blogs():
    blogs = []
    for filename in os.listdir("static/Homepage-blogs"):
        if filename.endswith(".txt"):
            blogs.append(filename)
    
    with open("static/Homepage-blogs/" + random.choice(blogs), "r") as f:
        blog1 = f.read()
    return blog1


#create a function that returns the current second
def get_current_second():
    return datetime.now().second




@app.route("/create_blog", methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        blog_author = session['username']
        blog_content = request.form["blog_content"] + "\r\n" +  "~ " + blog_author
        with open("static/Homepage-blogs/" + str(blog_author) + str(get_current_second()) + ".txt", "w") as f:
            f.write(blog_content)
        return redirect(url_for("home"))
    return render_template("create_new_blog.html")

@app.route('/',methods=["POST","GET"])
def index():
    if 'id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/home", methods = ["POST","GET"])
def home():
    session['blog'] = get_blogs()
    if request.method == 'POST':
        db = sqlite3.connect("db.sql")
        cursor = db.cursor()
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('login'))
    else:
        if 'id' in session:
            return render_template('hompage.html')
        else:
            return redirect(url_for('login'))
        

@app.route("/register",methods = ["POST","GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    username = request.form.get('username')
    psw = request.form.get('password')
    repsw = request.form.get('repassword')
    if psw != repsw or check_for_name_in_db(username) == True:
        flash("⚠️ Etwas stimmt hier nicht überprüfe deine Eingaben!",'error')
        return redirect(url_for('register'))
    else:
        id = uuid.uuid4()
        session['id'] = id
        session['username'] = username
        with sqlite3.connect("db.sql") as db:
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO users VALUES('{id}','{username}','{psw}','Ich bin neu!','User')")
            db.commit()
        os.system(f"cd static && cd user && mkdir {username} && cd {username} && mkdir blogs && mkdir pfp")
        os.system("exit")
        ori = r'static/default-pfp/images.jpg'
        dest = r'static/user/{0}/pfp/images.jpg'.format(username)
        shutil.copy(ori,dest)
        return redirect(url_for('home'))


@app.route("/login",methods = ['POST',"GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    username = request.form.get('username')
    psw = request.form.get('password')
    with sqlite3.connect("db.sql") as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{psw}'")
        user = cursor.fetchone()
        if user:
            session['id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route("/profile/<username>",methods = ['POST',"GET"])
def profile(username):
    if 'id' in session:
        #select bio from users where username = username
        with sqlite3.connect("db.sql") as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT Bio FROM users WHERE username = '{username}'")
            bio = cursor.fetchone()
            if bio:
                bio = bio[0]
            else:
                bio = "Ich bin neu!"
        return render_template_string(
        f'''
        <html>
        <head>
        <title>{username}</title>
        </head>
        <body>
        <h1>{username}</h1>
        <h2>{bio}</h2>
        


        </html>
        ''')
    

app.run(host="192.168.178.36",port=2308,debug=True)