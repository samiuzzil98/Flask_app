from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length



app = Flask(__name__, template_folder="app/templates")
app.secret_key = "Hello"

class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=['POST', 'GET'])
def login():

    login_form = LoginForm() 

    if login_form.validate_on_submit():
            
            user_name = login_form.user_name.data
            password = login_form.password.data

            session['user_name'] = user_name
            
            
            # flash(f'You are successfully logged in as {user_name}')
            
            return redirect(url_for('user', user_name=user_name))
    
    else:
        if 'user_name' in session:
            return redirect(url_for('user', user_name =session['user_name']))   
        else:
             return render_template('login.html', form=login_form)    

@app.route("/user/<user_name>")
def user(user_name):
    if 'user_name' not in session:
         return redirect(url_for("login"))
    else:
        return render_template('user.html', userName = session['user_name'])
    
@app.route("/logout")
def logout():
    if 'user_name' in session:
        session.pop("user_name")
        flash()
        return redirect(url_for("login"))
    else:
        return redirect(url_for('login'))
    
if __name__=="__main__":
    app.run(debug=True)