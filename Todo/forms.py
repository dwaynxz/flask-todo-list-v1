from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=2, max=20), DataRequired(message="Name field cannot be empty")])
    email = StringField("Email", validators=[DataRequired(message="Email fiel cannot be empty"), Email()])
    password = PasswordField("Password", validators=[DataRequired(message="Password field cannot be empty"), EqualTo("confirm_password")])
    confirm_password = PasswordField("Confirm Passowrd", validators=[DataRequired(message="Confirm password field cannot be empty")])
    submit = SubmitField("Create Account")

