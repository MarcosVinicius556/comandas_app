from flask import Blueprint, render_template
from mod_login.login import validaLogin;
bp_erro = Blueprint('erro', __name__, template_folder="templates");

@bp_erro.app_errorhandler(404)
@validaLogin
def erro404(error):
    return render_template("form404.html", erroHttp=error)

@bp_erro.app_errorhandler(500)
@validaLogin
def erro500(error):
    return render_template("form500.html", erroHttp=error)