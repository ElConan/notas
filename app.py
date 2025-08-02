from flask import Flask, render_template, request, redirect, session
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'secreto'

# Crear la base de datos
def init_db():
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE,
                        password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS notas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        contenido TEXT)''')
init_db()

# Página de inicio / login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('notas.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                return redirect('/notas')
            else:
                return "Credenciales incorrectas"
    return render_template('login.html')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('notas.db') as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn.commit()
                return redirect('/')
            except:
                return "Usuario ya existe"
    return render_template('register.html')

# Página de notas
@app.route('/notas', methods=['GET', 'POST'])
def notas():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            nota = request.form['nota']
            c.execute("INSERT INTO notas (user_id, contenido) VALUES (?, ?)", (user_id, nota))
            conn.commit()
        c.execute("SELECT contenido FROM notas WHERE user_id=?", (user_id,))
        mis_notas = c.fetchall()
    return render_template('notas.html', notas=mis_notas)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# regresar a la página de login
@app.route('/login')
def login_again():
    return redirect('/')



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
