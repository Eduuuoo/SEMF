from flask import Flask, render_template, request, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = "semf_production_key_2026"

# Lista do Portal da Transparência
gastos_lista = [
    {"data": "02/05/2026", "descricao": "Material Esportivo e Coletes", "valor": "R$ 1.250,00"},
    {"data": "10/05/2026", "descricao": "Manutenção da Sede / Campo", "valor": "R$ 600,00"},
    {"data": "14/05/2026", "descricao": "Logística e Arbitragem", "valor": "R$ 450,00"}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/transparencia')
def transparencia():
    return render_template('transparencia.html', gastos=gastos_lista)

@app.route('/pagamentos')
def pagamentos():
    return render_template('pagamentos.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        
        file_path = 'inscricoes_semf.csv'
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Nome Atleta', 'CPF', 'WhatsApp'])
            writer.writerow([nome, cpf, telefone])
            
        return render_template('sucesso.html', nome=nome)
    return render_template('inscricao.html')

if __name__ == '__main__':
    app.run(debug=True)