from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
# from mod_login.login import validaLogin
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO

from funcoes import Funcoes;

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=["GET", "POST"])
# @validaLogin TODO FIXME Verificar....
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()
        print(result) # para teste
        print(response.status_code) # para teste
        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/new', methods=["GET"])
def formNovoFuncionario():
    return render_template('formNovoFuncionario.html'), 200

@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['codigo']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        print(request.form)
        senha = Funcoes.get_password_hash(request.form['senha'])
        
        # monta o JSON para envio a API
        payload = {'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        result = response.json()
       
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
            
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
        
    except Exception as e:
        print(e);
        return render_template('formListaFuncionario.html', msgErro=e.args[0])