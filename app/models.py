from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='secretaria')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)





class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)

    turnos = db.relationship('Turno', backref='paciente', lazy=True)

class Odontologo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    turnos = db.relationship('Turno', backref='odontologo', lazy=True)

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    odontologo_id = db.Column(db.Integer, db.ForeignKey('odontologo.id'), nullable=False)

    def __repr__(self):
        return f"<Turno {self.fecha} - Paciente {self.paciente_id} - Odontólogo {self.odontologo_id}>"


class HistoriaClinica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    paciente = db.relationship('Paciente', backref=db.backref('historias_clinicas', lazy=True))

    def __repr__(self):
        return f'<HistoriaClinica {self.id} - Paciente {self.paciente_id}>'


class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historia_clinica_id = db.Column(db.Integer, db.ForeignKey('historia_clinica.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    historia_clinica = db.relationship('HistoriaClinica', backref=db.backref('tratamientos', lazy=True))

    def __repr__(self):
        return f'<Tratamiento {self.nombre}>'

