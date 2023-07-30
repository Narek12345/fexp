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


class JobVacansyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    salary = IntegerField('Salary', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    necessary_skills = StringField('Necessary skills', validators=[DataRequired()])


class SummaryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    salary = IntegerField('Salary', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])