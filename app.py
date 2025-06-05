

from flask import Flask, render_template, request, redirect, url_for, flash
from forms import PacienteForm
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'miclaveultrasecreta123'  # después pondremos algo más seguro
# Configuración de la base de datos (archivo local SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'odontologia.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos el ORM
db = SQLAlchemy(app)


@app.route('/')
def home():
    usuario = "Juan Pablo"
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    return render_template('home.html', usuario=usuario, fecha_actual=fecha_actual)

@app.route('/pacientes')
def pacientes():
    lista_pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=lista_pacientes)


@app.route('/odontologos')
def odontologos():
    lista_odontologos = ["Dra. Laura Sánchez", "Dr. Gustavo Molina", "Dra. Mariana López"]
    return render_template('odontologos.html', odontologos=lista_odontologos)


class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Paciente {self.nombre} {self.apellido}>'


@app.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado correctamente.', 'success')
    return redirect(url_for('pacientes'))




@app.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)

    if form.validate_on_submit():
        paciente.nombre = form.nombre.data
        paciente.apellido = form.apellido.data
        db.session.commit()
        flash('Paciente actualizado correctamente.', 'success')
        return redirect(url_for('pacientes'))

    return render_template('editar_paciente.html', form=form, paciente=paciente)



@app.route('/nuevo_paciente', methods=['GET', 'POST'])
def nuevo_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        nuevo = Paciente(nombre=form.nombre.data, apellido=form.apellido.data)
        db.session.add(nuevo)
        db.session.commit()
        flash(f'Paciente {nuevo.nombre} {nuevo.apellido} agregado correctamente.', 'success')
        return redirect(url_for('home'))
    return render_template('nuevo_paciente.html', form=form)

if __name__ == '__main__':
   app.run(debug=True, port=3000)
