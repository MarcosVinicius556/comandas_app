from flask import Flask, render_template
from settings import HOST, PORT, DEBUG

# import blueprint criado
from mod_funcionario.funcionario import bp_funcionario
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto

app = Flask(__name__)
# registro das rotas do blueprint
app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)

@app.route('/')
def formIndex():
    return "<h1>Rota da página inicial da nossa WEB APP</h1>", 200

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
