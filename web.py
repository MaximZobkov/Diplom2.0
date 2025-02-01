from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.booking import Booking
from data.services import Service
from data.users import User
from database import db
from static.forms.bookingform import BookingForm
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


@app.route('/', methods=['GET'])
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)


@app.route('/service/<int:service_id>', methods=['GET'])
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template('service.html', service=service)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        gender = form.gender.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Имя пользователя уже существует. Пожалуйста, выберите другое.', 'danger')
            return render_template('register.html', form=form,
                                   username_err="Имя пользователя уже существует. Пожалуйста, выберите другое.")

        if existing_email:
            flash('Email уже существует. Пожалуйста, выберите другой.', 'danger')
            return render_template('register.html', form=form,
                                   email_err="Email уже существует. Пожалуйста, выберите другой.")

        user = User(username=username, email=email, first_name=first_name, last_name=last_name,
                    date_of_birth=date_of_birth, gender=gender)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Пожалуйста, войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, username_err="OK", email_err="OK")


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
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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
        flash('Бронирование успешно!', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
