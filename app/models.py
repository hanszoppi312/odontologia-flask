from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------ PACIENTE ------------------
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)

    historias_clinicas = db.relationship(
        'HistoriaClinica',
        backref='paciente',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    turnos = db.relationship(
        'Turno',
        backref='paciente',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Paciente {self.nombre} {self.apellido}>'

# ------------------ HISTORIA CLÍNICA ------------------
class HistoriaClinica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete="CASCADE"), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)

    tratamientos = db.relationship(
        'Tratamiento',
        backref='historia_clinica',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<HistoriaClinica {self.id} - Paciente {self.paciente_id}>'

# ------------------ TRATAMIENTO ------------------
class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historia_clinica_id = db.Column(db.Integer, db.ForeignKey('historia_clinica.id', ondelete="CASCADE"), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tratamiento {self.nombre}>'

# ------------------ ODONTOLOGO ------------------
class Odontologo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    turnos = db.relationship(
        'Turno',
        backref='odontologo',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Odontologo {self.nombre} {self.apellido} - {self.especialidad}>'

# ------------------ TURNO ------------------
class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete="CASCADE"), nullable=False)
    odontologo_id = db.Column(db.Integer, db.ForeignKey('odontologo.id', ondelete="CASCADE"), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(100))

    def __repr__(self):
        return f'<Turno {self.id} - Paciente {self.paciente_id}>'


# ------------------ USUARIO ------------------
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='secretaria')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'
