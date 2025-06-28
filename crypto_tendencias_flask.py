from flask import Flask, render_template, request, redirect, url_for
import os, json
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
POSTS_FILE = 'posts.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        if image.filename != '':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_url = image_path

            posts = load_posts()
            posts.insert(0, {
                'title': title,
                'description': description,
                'image_url': image_url,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_posts(posts)
            return redirect(url_for('index'))

    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
