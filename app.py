# Importamos los módulos principales de Flask
from flask import Flask, render_template, request, redirect, url_for, session

# Importamos SQLAlchemy para gestionar la base de datos
from flask_sqlalchemy import SQLAlchemy

# Importamos os para verificar si la base de datos existe
import os

# Creamos la app Flask
app = Flask(__name__)

# Establecemos una clave secreta para manejar sesiones (login, etc.)
app.secret_key = "supersecreto"  # Puedes cambiar esto por algo más seguro

# Configuramos la URI de la base de datos, en este caso un archivo SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Creamos una instancia de SQLAlchemy conectada a nuestra app Flask
db = SQLAlchemy(app)

# Importamos los modelos definidos en otro archivo (por ejemplo: models.py)
from models import *

# ---------------------------------------------------
# RUTAS DE LA APLICACIÓN
# ---------------------------------------------------

# Ruta principal: redirecciona al login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para iniciar sesión (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí luego validaremos los datos del formulario de login (correo + contraseña)
        pass
    return render_template('login.html')  # Muestra el formulario de login

# Ruta para registrar a la "cabeza de familia" (admin)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Aquí luego crearemos un nuevo usuario administrador
        pass
    return render_template('register.html')  # Muestra el formulario de registro

# ---------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ---------------------------------------------------

if __name__ == '__main__':
    # Si el archivo database.db no existe, lo crea con las tablas definidas en models.py
    if not os.path.exists("database.db"):
        db.create_all()  # Crea todas las tablas
    # Inicia la app en modo debug (útil para desarrollo)
    app.run(debug=True)
