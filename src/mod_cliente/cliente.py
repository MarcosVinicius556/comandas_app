from flask import Blueprint, render_template
import requests
from settings import getHeadersAPI, ENDPOINT_CLIENTE
from mod_login.login import validaLogin;

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/', methods=["GET", "POST"])
@validaLogin
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()
        print(result) # para teste
        print(response.status_code) # para teste
        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])


@bp_cliente.route('/new', methods=["GET"])
@validaLogin
def formNovoCliente():
    return render_template('formNovoCliente.html'), 200