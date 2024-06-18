from flask import Blueprint, send_file
import requests
from settings import getHeadersAPI, ENDPOINT_RELATORIOS
from mod_login.login import validaLogin;
import os

bp_report = Blueprint('report', __name__, url_prefix="/report", template_folder='templates')


@bp_report.route('/export/<int:type>')
@validaLogin
def exportPDF(type: int):
    response = requests.get(f"{ENDPOINT_RELATORIOS}{type}", headers=getHeadersAPI())
    
    if response.status_code == 200:
        pdf_path = os.path.join(os.getcwd(), "relatorio.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.content)
    
    return send_file(pdf_path, as_attachment=True)

