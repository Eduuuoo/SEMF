from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Dados para a Transparência (Simulados)
gastos_lista = [
    {"data": "02/05/2026", "descricao": "Material Esportivo", "valor": "R$ 750,00"},
    {"data": "10/05/2026", "descricao": "Manutenção Campo", "valor": "R$ 600,00"}
]

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f"Erro ao carregar a página inicial: {e}"

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/transparencia')
def transparencia():
    return render_template('transparencia.html', gastos=gastos_lista)

@app.route('/doacao')
def doacao():
    return render_template('doacao.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        nome_atleta = request.form.get('nome')
        return render_template('sucesso.html', nome=nome_atleta)
    return render_template('inscricao.html')

if __name__ == '__main__':
    # O debug=True ajuda a ver o erro real se o site cair
    app.run(debug=True)