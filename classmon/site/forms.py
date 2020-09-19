from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
	title = "Log in"

	username = StringField("Username", [DataRequired()])
	password = PasswordField("Password", [DataRequired()])
	submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
	title = "Register"

	username = StringField("Username", [DataRequired(), Length(min=3)])
	password1 = PasswordField("Password", [DataRequired(), Length(min=6)])
	password2 = PasswordField("Repeat password", [DataRequired(), EqualTo("password1")])
	submit = SubmitField("Register")

class ChangePasswordForm(FlaskForm):
	title = "Change password"
	
	current_password = PasswordField("Current password", [DataRequired()])
	new_password1 = PasswordField("New password", [DataRequired(), Length(min=6)])
	new_password2 = PasswordField("Repeat new password", [DataRequired(), EqualTo("new_password1")])
	submit = SubmitField("Register")

class DeleteAccountForm(FlaskForm):
	title = "Delete account"
	submit = SubmitField("Submit")