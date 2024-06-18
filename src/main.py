from flask import Flask, session;
from settings import HOST, PORT, DEBUG, TEMPO_SESSION
import os;
from datetime import timedelta;

# import blueprint criado
from mod_index.index import bp_index
from mod_funcionario.funcionario import bp_funcionario
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
from mod_login.login import bp_login
from mod_report.report import bp_report


# Tratamento de exceções na aplicação
from mod_erro.erro import bp_erro

app = Flask(__name__)

# gerando uma chave randômica para secret_key
app.secret_key = os.urandom(12).hex()

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE='True'
)

@app.before_request
def before_request():
    session.permanent = True;
    session['tempo'] = int(TEMPO_SESSION);
    app.permanent_session_lifetime = timedelta( minutes=session['tempo'] )


# registro das rotas do blueprint
app.register_blueprint(bp_index)
app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_login)
app.register_blueprint(bp_report)
app.register_blueprint(bp_erro)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
