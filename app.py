import csv
import os
import json
from datetime import date, datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_only_fallback_key')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivos de dados
CSV_ATLETAS   = os.path.join(BASE_DIR, 'inscricoes_semf.csv')
JSON_GASTOS   = os.path.join(BASE_DIR, 'data', 'gastos.json')
JSON_ANIVERSARIANTES = os.path.join(BASE_DIR, 'data', 'aniversariantes.json')

# Credenciais admin (configure no Render como variáveis de ambiente)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'semf2026')

# --------------------------------------------------------------------------
# Utilitários de dados
# --------------------------------------------------------------------------

def load_json(path, default):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.isfile(path):
        save_json(path, default)
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_gastos():
    default = [
        {"data": "02/05/2026", "descricao": "Material Esportivo e Coletes",  "valor": "R$ 1.250,00"},
        {"data": "10/05/2026", "descricao": "Manutenção da Sede / Campo",    "valor": "R$ 600,00"},
        {"data": "14/05/2026", "descricao": "Logística e Arbitragem",        "valor": "R$ 450,00"},
    ]
    return load_json(JSON_GASTOS, default)

def get_aniversariantes():
    default = [
        {"nome": "Carlos Silva",  "data_nasc": "1998-05-21", "modalidade": "Futebol"},
        {"nome": "Lucas Mendes",  "data_nasc": "2005-05-21", "modalidade": "Futsal"},
    ]
    return load_json(JSON_ANIVERSARIANTES, default)

def aniversariantes_hoje():
    hoje = date.today()
    todos = get_aniversariantes()
    result = []
    for a in todos:
        try:
            dt = datetime.strptime(a['data_nasc'], '%Y-%m-%d').date()
            if dt.month == hoje.month and dt.day == hoje.day:
                idade = hoje.year - dt.year
                result.append({**a, 'idade': idade})
        except Exception:
            pass
    return result

# --------------------------------------------------------------------------
# Proteção de rota admin
# --------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logado'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# --------------------------------------------------------------------------
# Rotas públicas
# --------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html', aniversariantes=aniversariantes_hoje())

@app.route('/transparencia')
def transparencia():
    return render_template('transparencia.html', gastos=get_gastos())

@app.route('/pagamentos')
def pagamentos():
    return render_template('pagamentos.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        campos = ['nome', 'cpf', 'whatsapp', 'data_nasc',
                  'responsavel', 'endereco', 'modalidade', 'categoria']
        dados = {c: request.form.get(c, '').strip() for c in campos}

        obrigatorios = ['nome', 'cpf', 'whatsapp', 'data_nasc', 'modalidade', 'categoria']
        for campo in obrigatorios:
            if not dados[campo]:
                return render_template('inscricao.html',
                                       erro="Preencha todos os campos obrigatórios.")

        file_exists = os.path.isfile(CSV_ATLETAS)
        with open(CSV_ATLETAS, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            if not file_exists:
                writer.writeheader()
            writer.writerow(dados)

            # Salva também em aniversariantes se ainda não existir
            anivs = get_aniversariantes()
            cpfs_existentes = [a.get('cpf') for a in anivs]
            if dados['cpf'] not in cpfs_existentes:
                anivs.append({
                    'nome': dados['nome'],
                    'cpf': dados['cpf'],
                    'data_nasc': dados['data_nasc'],
                    'modalidade': dados['modalidade']
                })
                save_json(JSON_ANIVERSARIANTES, anivs)

        return render_template('sucesso.html', nome=dados['nome'])

    return render_template('inscricao.html', erro=None)

# --------------------------------------------------------------------------
# Rotas Admin
# --------------------------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    erro = None
    if request.method == 'POST':
        user = request.form.get('usuario', '').strip()
        pwd  = request.form.get('senha', '').strip()
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['admin_logado'] = True
            return redirect(url_for('admin_dashboard'))
        erro = "Usuário ou senha incorretos."
    return render_template('admin/login.html', erro=erro)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logado', None)
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    atletas = []
    if os.path.isfile(CSV_ATLETAS):
        with open(CSV_ATLETAS, newline='', encoding='utf-8') as f:
            atletas = list(csv.DictReader(f))
    return render_template('admin/dashboard.html',
                           atletas=atletas,
                           gastos=get_gastos(),
                           aniversariantes=get_aniversariantes())

# --- Gastos ---
@app.route('/admin/gastos/adicionar', methods=['POST'])
@login_required
def admin_add_gasto():
    gastos = get_gastos()
    gastos.append({
        "data":     request.form.get('data', '').strip(),
        "descricao": request.form.get('descricao', '').strip(),
        "valor":    request.form.get('valor', '').strip(),
    })
    save_json(JSON_GASTOS, gastos)
    return redirect(url_for('admin_dashboard') + '#gastos')

@app.route('/admin/gastos/excluir/<int:idx>', methods=['POST'])
@login_required
def admin_del_gasto(idx):
    gastos = get_gastos()
    if 0 <= idx < len(gastos):
        gastos.pop(idx)
        save_json(JSON_GASTOS, gastos)
    return redirect(url_for('admin_dashboard') + '#gastos')

# --- Aniversariantes ---
@app.route('/admin/aniversariantes/adicionar', methods=['POST'])
@login_required
def admin_add_aniv():
    anivs = get_aniversariantes()
    anivs.append({
        "nome":       request.form.get('nome', '').strip(),
        "data_nasc":  request.form.get('data_nasc', '').strip(),
        "modalidade": request.form.get('modalidade', '').strip(),
    })
    save_json(JSON_ANIVERSARIANTES, anivs)
    return redirect(url_for('admin_dashboard') + '#aniversariantes')

@app.route('/admin/aniversariantes/excluir/<int:idx>', methods=['POST'])
@login_required
def admin_del_aniv(idx):
    anivs = get_aniversariantes()
    if 0 <= idx < len(anivs):
        anivs.pop(idx)
        save_json(JSON_ANIVERSARIANTES, anivs)
    return redirect(url_for('admin_dashboard') + '#aniversariantes')

if __name__ == '__main__':
    app.run(debug=True)