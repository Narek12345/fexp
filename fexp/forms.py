from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Sign In")


class EmployerForm(FlaskForm):
    first_name = StringField('First name: ', validators=[DataRequired()])
    last_name = StringField('Last name: ', validators=[DataRequired()])
    phone_number = IntegerField('Phone number: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])


class StudentForm(FlaskForm):
    first_name = StringField('First name: ', validators=[DataRequired()])
    last_name = StringField('Last name: ', validators=[DataRequired()])
    phone_number = IntegerField('Phone number: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])