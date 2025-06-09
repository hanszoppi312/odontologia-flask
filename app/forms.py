from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, SelectField, DateTimeField, PasswordField
from datetime import datetime

class EliminarUsuarioForm(FlaskForm):
    submit = SubmitField('Eliminar')

class EditarUsuarioForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'),
        ('odontologo', 'Odontólogo'),
        ('secretaria', 'Secretaria')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

class RegistroForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'),
        ('odontologo', 'Odontólogo'),
        ('secretaria', 'Secretaria')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')

class TurnoForm(FlaskForm):
    paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    odontologo = SelectField('Odontólogo', coerce=int, validators=[DataRequired()])
    fecha = DateTimeField('Fecha del turno (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', default=datetime.utcnow, validators=[DataRequired()])
    submit = SubmitField('Guardar Turno')

class PacienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Agregar Paciente')

class OdontologoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    especialidad = StringField('Especialidad', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Guardar Odontólogo')

class HistoriaClinicaForm(FlaskForm):
    paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Guardar Historia Clínica')

class TratamientoForm(FlaskForm):
    historia_clinica = SelectField('Historia Clínica', coerce=int, validators=[DataRequired()])
    
    # 🔧 MODIFICADO: agregamos el campo nombre (coherente con el modelo)
    nombre = StringField('Nombre del Tratamiento', validators=[DataRequired(), Length(min=2, max=100)])
    
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Guardar Tratamiento')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
