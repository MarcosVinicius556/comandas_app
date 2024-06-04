from flask import Blueprint, render_template;
from mod_login.login import validaLogin;

bp_index = Blueprint("index", __name__, url_prefix="/home", template_folder="templates")

@bp_index.route("/")
@validaLogin
def index():
    return render_template('formIndex.html'), 200;