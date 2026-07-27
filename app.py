import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capturar', methods=['POST'])
def capturar():
    data = request.json
    # Aqui o seu site recebe o token vindo do CMSP
    token = data.get('token')
    if token:
        print(f"TOKEN RECEBIDO!") 
        return jsonify({"status": "sucesso", "token_recebido": True})
    return jsonify({"status": "erro"}), 400

if __name__ == '__main__':
    # O Render configura a porta automaticamente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
