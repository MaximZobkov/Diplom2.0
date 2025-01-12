from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.booking import Booking
from data.services import Service
from data.users import User
from diplom.database import db
from static.forms.booking import BookingForm
from static.forms.loginform import LoginForm
from static.forms.registerform import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/detail'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form, err="Username already exists. Please choose a different one.")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, err="OK")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/services', methods=['GET'])
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookingForm()
    form.service.choices = [(service.id, service.name) for service in Service.query.all()]
    if form.validate_on_submit():
        service_id = form.service.data
        booking_date = form.booking_date.data
        booking = Booking(user_id=current_user.id, service_id=service_id, booking_date=booking_date)
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
