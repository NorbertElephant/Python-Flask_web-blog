from flask import Flask, render_template, flash , redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from data import Articles
from classes.RegisterForm import RegisterForm

#---------- Config  -------------#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#---------- Config SQL   -------------#
app.config['MYSQL_HOST'] ="localhost"
app.config['MYSQL_USER'] ="root"
app.config['MYSQL_PASSWORD'] =""
app.config['MYSQL_DB'] ="blog_python"
app.config['MYSQL_CURSORCLASS'] ="DictCursor"
# Init MYSQL 
mysql = MySQL(app)

# ALERT DO CONTROLLERS #
#---------- ROUTES  -------------#
@app.route('/')
def index() :
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/articles")
def articles():
    articles = Articles()
    return render_template('articles/index.html', articles=articles)

@app.route("/articles/<string:id>")
def article(id):
    return render_template('articles/show.html', id=id)

# Do a Controller Security 
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate() :
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        
        #Create cursor
        cur= mysql.connection.cursor()
        #Execute query
        cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s, %s, %s,%s)", (name, email, username, password) )
        #Commit to DB
        mysql.connection.commit()
        #Close Connection 
        cur.close()

        flash('Vous êtes maintenant enregister et vous pouvez vous connecter', 'success')
        return redirect(url_for('index'))
        

    return render_template('register/signin.html', form=form)

@app.route('/login', methods=['GET', 'POST'])







if __name__ == '__main__':
    app.run(debug=True)