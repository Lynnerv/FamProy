from app import db
from datetime import datetime

# -----------------------------
# TABLA: Usuario (cabeza de familia)
# -----------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    token_familiar = db.Column(db.String(50), unique=True, nullable=False)

    miembros = db.relationship('Miembro', backref='familia', lazy=True)

# -----------------------------
# TABLA: Miembro (hijos, esposas, parientes)
# -----------------------------
class Miembro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_cumple = db.Column(db.Date, nullable=False)
    parentesco = db.Column(db.String(50))  # Hijo, esposa, primo, etc.
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Relación con su familia

# -----------------------------
# (Opcional) TABLA: Registro de tokens generados
# -----------------------------
class TokenFamiliar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
