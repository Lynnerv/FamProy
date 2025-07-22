from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid  # Para generar token familiar único

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///familias_cumpleaños.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Modelo actualizado
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    token_familiar = db.Column(db.String(20), unique=True, nullable=False)

# Ruta principal
@app.route("/")
def index():
    return redirect(url_for("login"))

# ✅ Ruta de registro actualizada
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        celular = request.form["celular"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        # Verificar si correo ya existe
        existente = Usuario.query.filter_by(correo=correo).first()
        if existente:
            flash("Este correo ya está registrado.", "error")
            return redirect(url_for("registro"))

        # Generar token familiar
        token = str(uuid.uuid4())[:8]

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            celular=celular,
            correo=correo,
            contraseña=generate_password_hash(contraseña),
            token_familiar=token
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(f"Registro exitoso. Tu token familiar es: {token}", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login (sin cambios)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['user_id'] = usuario.id
            session['user_nombre'] = usuario.nombre
            session['user_token'] = usuario.token_familiar
            flash(f"Bienvenido {usuario.nombre}!", "success")
            return redirect(url_for("dashboard"))

        flash("Correo o contraseña incorrectos.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión primero.", "error")
        return redirect(url_for("login"))

    nombre = session.get('user_nombre')
    token = session.get('user_token')
    return f"Hola {nombre}, tu token familiar es: {token} <br><a href='/logout'>Cerrar sesión</a>"

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("login"))

# Crear base de datos
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
