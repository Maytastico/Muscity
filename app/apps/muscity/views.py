from flask import Blueprint, request, url_for, render_template, flash
from flask_login import login_user, login_required
from werkzeug.utils import redirect
from database.handler import User, db

muscity_blueprint = Blueprint('muscity_blueprint', __name__, template_folder="templates" )

@muscity_blueprint.route("/muscity", methods=['GET'])
@login_required
def muscity():
    return render_template('index.html')

@muscity_blueprint.route("/manager", methods=['GET'])
@login_required
def manager():
    return render_template('manager.html')