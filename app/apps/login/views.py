from flask import Blueprint, request, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, db

login_blueprint = Blueprint('login_blueprint', __name__, template_folder="templates" )

@login_blueprint.route("/login", methods=['GET'])
def login():
    #Redirects user to the muscity panel if already logged in
    if current_user:
        is_auth = current_user.is_authenticated
        if is_auth:
            return redirect(url_for('muscity_blueprint.muscity'))

    return render_template('index.html', mode='login')

@login_blueprint.route("/login/<string:email>/", methods=['GET'])
def login_with_username(email):
    return render_template('index.html', mode='login', email=email)


@login_blueprint.route("/login", methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    #Redirects when successful
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('muscity_blueprint.muscity'))

    #Redirects when not successful
    flash('Provided login credentials do not exist', 'alert')
    if email:
        return redirect(url_for('login_blueprint.login_with_username', email=email))
    return redirect(url_for('login_blueprint.login'))

@login_blueprint.route("/signup", methods=['GET'])
def signup():

    if request.args:
        content = {}
        user = request.args.get('username')
        email = request.args.get('email')
        if len(user) > 1:
           content["username"] = user
        if len(email) > 1:
            content["email"] = email

        return render_template('index.html', mode='signup', signup_data=content)

    return render_template('index.html', mode='signup', signup_data=None)



@login_blueprint.route("/signup", methods=['POST'])
def signup_post():
    """[summary] Handels the signup form and checks whether a user already exists

    Returns:
        str: Returns the rendered webpage
    """


    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    is_error = False
    if len(username) < 1:
        flash('No username provided', 'alert')
        is_error = True
    if len(password) < 8:
        flash('Password should be greater then 8 characters', 'alert')
        is_error = True
    try:
        # Validate.
        valid = validate_email(email)

        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        flash('The provided email address is not valid', 'alert')
        is_error = True

    #Checks whether a user alreadyexists
    user = User.query.filter_by(email=email).first()
    if(user):
        flash('User already exists', 'alert')
        is_error=True

    #Checks whether an error occured and directs to user to the signup page
    if is_error:
        return redirect(url_for('login_blueprint.signup', email=email, username=username))

    #Creates a new user and adds it the database
    new_user = User(username, email, password)
    db.session.add(new_user)
    db.session.commit()


    #If adding the user was successful the user will be redirected to the login form
    flash('Registered successful', 'success')
    return redirect(url_for('login_blueprint.login'))


@login_blueprint.route("/logout", methods=['GET'])
@login_required
def logout():
    """Will log the user out, if the user is logged in

    Returns:
        redirect: redirects the user to the login page
    """
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login_blueprint.login'))
