import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# URL REAL QUE VOCÊ DESCOBRIU
AUTH_URL = "https://edusp-api.ip.tv/registration/edusp/token"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_e_buscar', methods=['POST'])
def login_e_buscar():
    dados = request.json
    ra = dados.get('ra')
    senha = dados.get('senha')
    
    # O MOTOR REAL: Falando com o servidor oficial do governo
    payload = {
        "login": ra,
        "senha": senha
    }
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://saladofuturo.educacao.sp.gov.br"
    }
    
    try:
        response = requests.post(AUTH_URL, json=payload, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            # Se logou, retornamos os dados REAIS vindos do governo
            return jsonify({
                "status": "sucesso", 
                "nome": res_data.get('DadosUsuario', {}).get('NAME', 'Usuário'),
                "token": res_data.get('token'),
                "tarefas": [] # Aqui buscaremos as tarefas reais no próximo passo
            })
        else:
            return jsonify({"status": "erro", "mensagem": "RA ou Senha incorretos no sistema oficial."})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": "Erro de conexão: " + str(e)})

if __name__ == '__main__':
    app.run()
