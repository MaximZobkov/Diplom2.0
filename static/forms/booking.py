from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField

class BookingForm(FlaskForm):
    service = SelectField('Service', validators=[DataRequired()], coerce=int)
    booking_date = DateField('Booking Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Book')
