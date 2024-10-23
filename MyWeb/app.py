from flask import Flask, send_from_directory, send_file, render_template, request, redirect, url_for, session
import sqlite3
from prometheus_client import Counter, generate_latest


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
page_refresh_counter = Counter(
    'page_refresh_total', 'Total number of page refreshes across all users'
)


def create_database():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/')
def index():
    page_refresh_counter.inc()

    if 'refresh_count' not in session:
        session['refresh_count'] = 0
    
    # Increase the page refresh count for the current user
    session['refresh_count'] += 1

    return render_template('index.html', refresh_count=session['refresh_count'])

@app.route('/todo')
def todo():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('todo.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/download')
def download():
    path = 'file.txt'
    return send_file(path, as_attachment=True)

# Expose Prometheus metrics
@app.route('/metrics')
def metrics():
    # Expose the metrics in the Prometheus format
    return generate_latest(page_refresh_counter)


if __name__ == "__main__":
    create_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
