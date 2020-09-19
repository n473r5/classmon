from flask import render_template, redirect, abort
from flask_login import current_user, login_user, logout_user, login_required
from . import app, db
from .forms import LoginForm, RegisterForm, ChangePasswordForm, DeleteAccountForm
from .models import User

@app.route("/index")
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.errorhandler(404)
def not_found(error):
	return render_template("404.html", error=error), 404

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			form.password.errors.append("Incorrect username or password.")
			return render_template("form.html", form=form)
		login_user(user)
		return redirect("/")
	return render_template("form.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect("/")
	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			user = User(username=form.username.data)
			user.set_password(form.password1.data)
			db.session.add(user)
			db.session.commit()
			return redirect("/login")
		else:
			form.password2.errors.append("A user with that username already exists.")
			return render_template("form.html", form=form)
		return render_template("form.html", form=form)
	return render_template("form.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("/")

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if not current_user.check_password(form.current_password.data):
			form.current_password.errors.append("Incorrect password.")
			return render_template("form.html", form=form)
		current_user.set_password(form.new_password1.data)
		db.session.commit()
		return redirect("/")
	return render_template("form.html", form=form)

@app.route("/delete-account", methods=["GET", "POST"])
def delete_account():
	form = DeleteAccountForm()
	if form.validate_on_submit():
		User.query.filter_by(id=current_user.id).delete()
		logout_user()
		db.session.commit()
		return redirect("/")
	return render_template("form.html", form=form)

@app.route("/~<username>")
@login_required
def profile(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template("user/profile.html", user=user)

@app.route("/settings")
@login_required
def settings():
	return render_template("user/settings.html")

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
	return render_template("user/dashboard.html")

@app.route("/explorer")
@login_required
def explorer():
	return render_template("user/explorer.html")

@app.route("/admin")
@login_required
def admin():
	if not current_user.is_admin:
		abort(404)
	tables = {"users": User.query.all()}
	return render_template("user/admin.html", tables=tables)