from flask import Blueprint, request, url_for, render_template, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash
from database.handler import User, db

login_blueprint = Blueprint('login_blueprint', __name__, template_folder="templates" )

@login_blueprint.route("/login", methods=['GET'])
def login():
    """Shows the login view if the user is not logged in. If the user is logged in, it will be redirected to the muscity view

    Returns:
        render_template: view with login form 
        redirect: redirct to muscity view, if authenticated
    """

    #Redirects user to the muscity panel if already logged in
    if current_user:
        is_auth = current_user.is_authenticated
        if is_auth:
            return redirect(url_for('muscity_blueprint.muscity'))

    return render_template('auth.html', mode='login')

@login_blueprint.route("/login/<string:email>/", methods=['GET'])
def login_with_username(email):
    """This will be executed when the login data which was put in by the user
    does not satisfy the condition e.q the password was not right

    Args:
        email (string): Contains the email that will be displayed inside the form

    Returns:
        string: returns the login view
    """
    return render_template('auth.html', mode='login', email=email)


@login_blueprint.route("/login", methods=['POST'])
def login_post():
    """Manages the authorization of a user, who has put its data into
    the login view. It checks whether the login information
    fullfils the conditions. These are fullfiled if the user exists and the 
    user has the same password as the selected user. Is this not the case the user 
    will be redirected to the login page.

    Returns:
        redirct(user login data is right): redirects to the muscity web client
        redirect(login data does not fullfil conditions): redirect to the login page
    """

    #Gets the data provided by the form
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    #Redirects when successful
    #Checks if the provided email exists inside the system
    if user:
        #Cehcks whether the password exists
        if check_password_hash(user.password, password):
            #Creates a jwt access token so the user can access the api
            response = make_response(redirect(url_for('muscity_blueprint.manager')))
            access_token = create_access_token(identity=user.email)
            set_access_cookies(response, access_token)
            #uses flask login to flag the user as authorized
            login_user(user)
            #redirect to the muscity web client
            return response

    #Redirects when not successful
    flash('Provided login credentials do not exist', 'alert')
    #Checks whether an email was provided
    if email:
        #redirects to the login page and sends the provided email with it
        return redirect(url_for('login_blueprint.login_with_username', email=email))
    #else no email was provided the a normal redirect is triggered
    return redirect(url_for('login_blueprint.login'))


@login_blueprint.route("/signup", methods=['GET'])
def signup():

    """Renders the signup page. If an email or an username is provided inside the 
    url the provided data is added to a dictionary and will be displayed with the login view.

    Returns:
        string(data was provided): rendered auth.html template with the provided data inside the form
        string(no data): rendered auth.html template with an empty form
    """
    if request.args:
        content = {}
        user = request.args.get('username')
        email = request.args.get('email')
        if len(user) > 1:
           content["username"] = user
        if len(email) > 1:
            content["email"] = email

        return render_template('auth.html', mode='signup', signup_data=content)

    return render_template('auth.html', mode='signup', signup_data=None)



@login_blueprint.route("/signup", methods=['POST'])
def signup_post():
    """[summary] Handels the signup form and checks whether a user email already exists
    and the provided password greater than 8 character is. 

    Returns:
        redirect(provided data satisfies conditions): Redirect to the login page with a flash massages that the regestration was successful
        redirect(provided data not fullfiled): Redirects to the signup page 

    """


    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    is_error = False

    #Checks whether a username was provided
    if len(username) < 1:
        flash('No username provided', 'alert')
        is_error = True

    #Checks whether the password contains more than 8 characters
    if len(password) < 8:
        flash('Password should be greater then 8 characters', 'alert')
        is_error = True

    #Validates the sent email whether it is a real email address
    try:
        # Validate.
        valid = validate_email(email)

        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        flash('The provided email address is not valid', 'alert')
        is_error = True

    #Checks whether a user already exists
    user = User.query.filter_by(email=email).first()
    if(user):
        flash('User already exists', 'alert')
        is_error=True

    #Checks whether an error occured and directs to the signup page were all flashed messages will be shown
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
    #Unsets the access token and makes it unavailable
    response = make_response(redirect(url_for('login_blueprint.login')))
    unset_jwt_cookies(response)
    #Removes the user from the flask login list
    logout_user()
    flash('Logout successful', 'success')
    return response
