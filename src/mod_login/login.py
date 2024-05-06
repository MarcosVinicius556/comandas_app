from flask import Blueprint, render_template, redirect, url_for, request;

bp_login = Blueprint("login", __name__, url_prefix="/", template_folder="templates")

@bp_login.route("/", methods=["GET", "POST"])
def formLogin():
    return render_template("formLogin.html");

@bp_login.route("/login", methods=["POST"])
def validaLogin():
    try:
        #Capturando dados do formulário
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        print(f"Senha -> {senha} Usuário -> {usuario}")
        
        if(usuario == "abc" and senha == "bBolinhas"):
            return redirect(url_for('index.index'))
        else:
            raise Exception("Falha ao realizar o login!")
    except Exception as e:
        return redirect(url_for('login.formLogin', msgErro=e.args[0]))