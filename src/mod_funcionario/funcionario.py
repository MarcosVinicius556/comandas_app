from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
# from mod_login.login import validaLogin
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO

from funcoes import Funcoes;

from mod_login.login import validaLogin;

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=["GET", "POST"])
@validaLogin
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
@validaLogin
def formNovoFuncionario():
    return render_template('formFuncionario.html', result={}), 200

@bp_funcionario.route('/insert', methods=['POST'])
@validaLogin
def insert():
    try:
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.get_password_hash(request.form['senha'])
        
        payload = {'codigo': '', 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
       
        requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
            
        return redirect(url_for('funcionario.formListaFuncionario', msg=f"Registro inserido com sucesso!"))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
    
@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
@validaLogin
def formEditFuncionario():
    try:
        id_funcionario = request.form['id']
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/edit', methods=['POST'])
@validaLogin
def edit():
    try:
        id_funcionario = request.form['codigo']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        # senha = Funcoes.cifraSenha(request.form['senha'])

        payload = {'codigo': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo':
        grupo, 'senha': 'senha'}
        
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return redirect(url_for('funcionario.formListaFuncionario', msg=f"Registro {id_funcionario} atualizado com sucesso!"))
    except Exception as e:
        print(e)
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/delete', methods=['POST'])
@validaLogin
def delete():
    try:
        id_funcionario = request.form['id']
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json();

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result);
        return jsonify(erro=False, msg=f"Registro {id_funcionario} removido com sucesso!");
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0]);