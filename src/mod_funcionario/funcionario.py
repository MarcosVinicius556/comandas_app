from flask import Blueprint, render_template

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=["GET", "POST"])
def formListaFuncionario():
    return render_template('formListaFuncionario.html'), 200

@bp_funcionario.route('/new', methods=["GET"])
def formNovoFuncionario():
    return render_template('formNovoFuncionario.html'), 200