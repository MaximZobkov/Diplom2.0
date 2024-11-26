from flask import Flask, redirect, render_template
from flask_login import logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import pyodbc

app = Flask(__name__)
app.config["SECRET_KEY"] = "4fe98061931b48142b52236b0df2dc25"

'''@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)'''


class LoginForm(FlaskForm):
    email = StringField("Логин", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


def main():
    # sessions = db_session.create_session()
    # sessions.close()
    app.run()


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    main()
