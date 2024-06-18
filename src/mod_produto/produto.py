from flask import Blueprint, render_template, request, jsonify
import requests
from settings import getHeadersAPI, ENDPOINT_PRODUTO
import base64
from mod_login.login import validaLogin;
from decimal import Decimal;

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=["GET", "POST"])
@validaLogin
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()
        print(result) # para teste
        print(response.status_code) # para teste
        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/new')
@validaLogin
def formNovoProduto():
    return render_template('formProduto.html', result={}), 200

@bp_produto.route("/form-edit-produto", methods=['POST','GET'])
@validaLogin
def formEditProduto():
    try:
        id_produto = request.form['codigo']

        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)

        return render_template('formProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/insert', methods=['POST'])
@validaLogin
def insert():
    try:
        id_produto = 0
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = Decimal(request.form['valor_unitario'])

        foto = request.files.get('foto')
        foto_data_uri = None
        if foto:
            foto_content_type = foto.content_type
            foto_base64 = base64.b64encode(foto.read()).decode('utf-8')
            foto_data_uri = f"data:{foto_content_type};base64,{foto_base64}"

        payload = {
            'id_produto': id_produto,
            'nome': nome,
            'descricao': descricao,
            'foto': foto_data_uri,
            'valor_unitario': str(valor_unitario)
        }

        print('DATA')
        print(payload)
        
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        print(e)
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_produto.route('/edit', methods=['POST'])
@validaLogin
def edit():
    try:
        id_produto = request.form['codigo']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']

        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")

        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}

        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_produto.route('/delete', methods=['POST'])
@validaLogin
def delete():
    try:
        id_produto = request.form['id_produto']

        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])