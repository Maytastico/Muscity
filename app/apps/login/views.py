from flask import Blueprint, request, url_for, render_template, flash

login_blueprint = Blueprint('login_blueprint', __name__, template_folder="templates" )

@login_blueprint.route("/", methods=['POST', 'GET'])
def login():
    return render_template('index.html')
