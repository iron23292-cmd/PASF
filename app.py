import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# COLE ABAIXO a "URL de Solicitação" (Request URL) que apareceu no seu print do 'token'
URL_OFICIAL_TOKEN = "COLOQUE_AQUI_A_URL_DO_SEU_PRINT"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_e_buscar', methods=['POST'])
def login_e_buscar():
    dados = request.json
    ra = dados.get('ra', '').strip()
    senha = dados.get('senha', '').strip()
    
    # Motor Real: Conversando com o servidor oficial
    payload = {"login": ra, "senha": senha}
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://saladofuturo.educacao.sp.gov.br"
    }
    
    try:
        response = requests.post(URL_OFICIAL_TOKEN, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            res_data = response.json()
            # Retorna os dados REAIS vindos do governo
            return jsonify({
                "status": "sucesso", 
                "nome": res_data.get('DadosUsuario', {}).get('NAME', 'Usuário'),
                "token": res_data.get('token'),
                "tarefas": [] # Aqui o bot buscará a lista real no próximo passo
            })
        else:
            return jsonify({"status": "erro", "mensagem": "RA ou Senha inválidos no sistema oficial."})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro de conexão com a API."})

if __name__ == '__main__':
    app.run()
