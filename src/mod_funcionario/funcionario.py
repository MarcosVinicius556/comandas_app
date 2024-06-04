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
    return render_template('formFuncionario.html', result={}), 200

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
        senha = Funcoes.get_password_hash(request.form['senha'])
        
        # monta o JSON para envio a API
        payload = {'codigo': '', 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
       
        print('chegou aqui 1') 
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        print('chegou aqui 1/2')
        # executa o verbo POST da API e armazena seu retorno
        print(response)
        # result = response.json()
        print('chegou aqui 2')
        # if (response.status_code != 200 or result[1] != 200):
            # raise Exception(result)
        
        print('chegou aqui 3')
            
        # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
        return redirect(url_for('funcionario.formListaFuncionario'))
    except Exception as e:
        print(e);
        print('chegou aqui 5')
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
    
@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
def formEditFuncionario():
    try:
        # ID enviado via FORM
        id_funcionario = request.form['id']
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        
        print(result)
        # renderiza o form passando os dados retornados
        return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/edit', methods=['POST'])
def edit():
    try:
        print('Chegou aqui 1')
        # dados enviados via FORM
        id_funcionario = request.form['codigo']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        # senha = Funcoes.cifraSenha(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'codigo': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo':
        grupo, 'senha': 'senha'}
        
        print('Chegou aqui 1')
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        print('Chegou aqui 2')
        result = response.json()
        print('Chegou aqui 3')
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        print('Chegou aqui 4')
        # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
        return redirect(url_for('funcionario.formListaFuncionario'))
    except Exception as e:
        print(e)
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/delete', methods=['POST'])
def delete():
    try:
        id_funcionario = request.form['id']
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()

        # print(response)
        # print(response.status_code)
        # print(result)
        # print(result[0])

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=f"Registro {id_funcionario} removido com sucesso!")
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])