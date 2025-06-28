from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os, json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_default_insegura')

POSTS_FILE = 'posts.json'

def carregar_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_post(post):
    posts = carregar_posts()
    posts.append(post)
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

@app.route('/')
def index():
    posts = carregar_posts()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.environ.get('ADMIN_USERNAME') and password == os.environ.get('ADMIN_PASSWORD'):
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('index'))

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if not session.get('logged_in'):
        flash('Acesso restrito.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        imagem = request.files['imagem']
        nome_imagem = secure_filename(imagem.filename)
        imagem.save(os.path.join('static', nome_imagem))

        if 'background' in request.files:
            bg = request.files['background']
            if bg and bg.filename:
                bg.save(os.path.join('static', 'background.jpg'))

        post = {
            'titulo': titulo,
            'descricao': descricao,
            'imagem': nome_imagem
        }
        salvar_post(post)
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('new.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
