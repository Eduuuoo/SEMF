# SEMF - Sociedade Esportiva Mais Futuro ⚽

Portal institucional e sistema de matrículas desenvolvido para a Associação Esportiva de Campo Novo de Rondônia - RO. O projeto conta com uma identidade visual moderna em *Dark Mode*, destacando as cores oficiais da organização (Turquesa, Laranja, Roxo e Vermelho).

---

## 🚀 Funcionalidades

- **Página Inicial Dinâmica:** Apresentação da associação e dos pilares do projeto (Competição, Disciplina e Futuro).
- **Ficha de Inscrição Online:** Formulário digital para captação de novos atletas.
- **Armazenamento Automatizado:** Os dados coletados no formulário de matrícula são salvos diretamente em um arquivo estruturado (`inscricoes_semf.csv`), ideal para integração com o Excel ou sincronização com o Google Drive.
- **Portal da Transparência:** Área dedicada à prestação de contas e lançamentos financeiros para a comunidade.
- **Módulo de Pagamentos:** Estrutura pronta para recebimento de mensalidades via PIX ou futura integração de boleto bancário.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Python 3](https://www.python.org/) / [Flask](https://flask.palletsprojects.com/)
- **Frontend:** HTML5, CSS3 (Customizado) e [Bootstrap 5](https://getbootstrap.com/)
- **Persistência de Dados:** Arquivo CSV (Manipulação nativa com a biblioteca `csv` do Python)

---

## 📂 Estrutura do Projeto

```text
├── app.py                  # Arquivo principal do servidor Flask
├── requirements.txt        # Dependências do projeto para instalação
├── README.md               # Manual de instruções do repositório
├── static/
│   ├── logo.jpg            # Imagem oficial da logo da SEMF
│   └── style.css           # Estilização geral (Visual Dark)
└── templates/
    ├── base.html           # Estrutura e menu de navegação padrão
    ├── home.html           # Tela principal do portal
    ├── inscricao.html      # Formulário de matrícula de atletas
    ├── pagamentos.html     # Painel financeiro institucional
    ├── sucesso.html        # Confirmação de dados recebidos
    └── transparencia.html  # Tabela de prestação de contas