from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from settings import getHeadersAPI, ENDPOINT_CLIENTE
from mod_login.login import validaLogin;

from funcoes import Funcoes;

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
    return render_template('formCliente.html', result={}), 200

@bp_cliente.route('/insert', methods=['POST'])
@validaLogin
def insert():
    try:
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        
        payload = {'codigo': '', 'nome': nome, 'cpf': cpf, 'telefone': telefone}
       
        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        return redirect(url_for('cliente.formListaCliente', msg=f"Registro inserido com sucesso!"))
    except Exception as e:
        print('Caiu na exceção!')
        print(e)
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
    
@bp_cliente.route("/form-edit-cliente", methods=['POST'])
@validaLogin
def formEditCliente():
    try:
        id_cliente = request.form['id']
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/edit', methods=['POST'])
@validaLogin
def edit():
    try:
        #TODO Alterar os campos para se adequar ao cliente
        id_cliente = request.form['codigo']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']

        payload = {'codigo': id_cliente, 
                   'nome': nome, 
                   'cpf': cpf, 
                   'telefone': telefone
                   }
        
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI(), json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return redirect(url_for('cliente.formListaCliente', msg=f"Registro {id_cliente} atualizado com sucesso!"))
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/delete', methods=['POST'])
@validaLogin
def delete():
    try:
        id_cliente = request.form['id']
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json();

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result);
        return jsonify(erro=False, msg=f"Registro {id_cliente} removido com sucesso!");
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0]);