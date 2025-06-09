from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.orm import joinedload
from .decorators import rol_requerido
from flask_login import logout_user,current_user
from .forms import PacienteForm, OdontologoForm, TurnoForm, HistoriaClinicaForm,TratamientoForm,LoginForm,EditarUsuarioForm,EliminarUsuarioForm
from .models import Paciente, Odontologo, Turno, HistoriaClinica,Tratamiento,Usuario



from . import db, app


# RUTAS

from sqlalchemy import func



from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash




@app.route('/admin/usuarios')
@login_required
@rol_requerido(['admin'])
def administrar_usuarios():
    usuarios = Usuario.query.all()
    eliminar_forms = { usuario.id: EliminarUsuarioForm() for usuario in usuarios }
    return render_template('admin_usuarios.html', usuarios=usuarios, eliminar_forms=eliminar_forms)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

from flask import render_template, redirect, url_for, flash
from .models import Usuario
from .forms import RegistroForm
from . import db

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(username=form.username.data).first()
        if usuario_existente:
            flash('El usuario ya existe.', 'danger')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuario(
            username=form.username.data,
            rol=form.rol.data
        )
        nuevo_usuario.set_password(form.password.data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        logout_user()
        flash('Usuario registrado correctamente.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)




@app.route('/top_pacientes_turnos')
def top_pacientes_turnos():
    reporte = db.session.query(
        Paciente.nombre,
        Paciente.apellido,
        func.count(Turno.id)
    ).join(Turno).group_by(Paciente.id).order_by(func.count(Turno.id).desc()).limit(5).all()

    return render_template('top_pacientes.html', reporte=reporte)


@app.route('/reporte_turnos_por_odontologo')
def reporte_turnos_por_odontologo():
    reporte = db.session.query(
        Odontologo.nombre,
        Odontologo.apellido,
        func.count(Turno.id)
    ).join(Turno).group_by(Odontologo.id).all()

    return render_template('reporte_turnos_odontologo.html', reporte=reporte)


@app.route('/dashboard')
def dashboard():
    total_pacientes = db.session.query(func.count(Paciente.id)).scalar()
    total_odontologos = db.session.query(func.count(Odontologo.id)).scalar()
    total_turnos = db.session.query(func.count(Turno.id)).scalar()
    total_historias = db.session.query(func.count(HistoriaClinica.id)).scalar()
    total_tratamientos = db.session.query(func.count(Tratamiento.id)).scalar()

    return render_template(
        'dashboard.html',
        total_pacientes=total_pacientes,
        total_odontologos=total_odontologos,
        total_turnos=total_turnos,
        total_historias=total_historias,
        total_tratamientos=total_tratamientos
    )


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pacientes')
def pacientes():
    lista_pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=lista_pacientes)

@app.route('/nuevo_paciente', methods=['GET', 'POST'])
def nuevo_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        nuevo = Paciente(nombre=form.nombre.data, apellido=form.apellido.data)
        db.session.add(nuevo)
        db.session.commit()
        flash(f'Paciente {nuevo.nombre} {nuevo.apellido} agregado correctamente.', 'success')
        return redirect(url_for('pacientes'))
    return render_template('nuevo_paciente.html', form=form)

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

@app.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado correctamente.', 'success')
    return redirect(url_for('pacientes'))





# Listado de odontologos
@app.route('/odontologos')
@login_required
@rol_requerido(['admin', 'secretaria'])
def odontologos():
    lista_odontologos = Odontologo.query.all()
    return render_template('odontologos.html', odontologos=lista_odontologos)

# Crear odontólogo
@app.route('/nuevo_odontologo', methods=['GET', 'POST'])
def nuevo_odontologo():
    form = OdontologoForm()
    if form.validate_on_submit():
        nuevo = Odontologo(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            especialidad=form.especialidad.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash(f'Odontologo {nuevo.nombre} agregado correctamente.', 'success')
        return redirect(url_for('odontologos'))
    return render_template('nuevo_odontologo.html', form=form)

# Editar odontologo
@app.route('/editar_odontologo/<int:id>', methods=['GET', 'POST'])
def editar_odontologo(id):
    odontologo = Odontologo.query.get_or_404(id)
    form = OdontologoForm(obj=odontologo)
    if form.validate_on_submit():
        odontologo.nombre = form.nombre.data
        odontologo.apellido = form.apellido.data
        odontologo.especialidad = form.especialidad.data
        db.session.commit()
        flash('Odontologo actualizado correctamente.', 'success')
        return redirect(url_for('odontologos'))
    return render_template('editar_odontologo.html', form=form, odontologo=odontologo)

# Eliminar odontologo
@app.route('/eliminar_odontologo/<int:id>', methods=['POST'])
def eliminar_odontologo(id):
    odontologo = Odontologo.query.get_or_404(id)
    db.session.delete(odontologo)
    db.session.commit()
    flash('Odontologo eliminado correctamente.', 'success')
    return redirect(url_for('odontologos'))


@app.route('/editar_turno/<int:id>', methods=['GET', 'POST'])
def editar_turno(id):
    turno = Turno.query.get_or_404(id)
    form = TurnoForm(obj=turno)

    # Cargamos nuevamente las opciones de selects (muy importante)
    form.paciente.choices = [(p.id, f"{p.nombre} {p.apellido}") for p in Paciente.query.all()]
    form.odontologo.choices = [(o.id, f"{o.nombre} {o.apellido}") for o in Odontologo.query.all()]

    if form.validate_on_submit():
        turno.paciente_id = form.paciente.data
        turno.odontologo_id = form.odontologo.data
        turno.fecha = form.fecha.data
        db.session.commit()
        flash('Turno actualizado correctamente.', 'success')
        return redirect(url_for('turnos'))

    # Pre-cargar los valores seleccionados:
    form.paciente.data = turno.paciente_id
    form.odontologo.data = turno.odontologo_id

    return render_template('editar_turno.html', form=form, turno=turno)



@app.route('/nuevo_turno', methods=['GET', 'POST'])
def nuevo_turno():
    form = TurnoForm()

    # Cargamos dinámicamente los pacientes y odontólogos en el formulario
    form.paciente.choices = [(p.id, f"{p.nombre} {p.apellido}") for p in Paciente.query.all()]
    form.odontologo.choices = [(o.id, f"{o.nombre} {o.apellido}") for o in Odontologo.query.all()]

    if form.validate_on_submit():
        turno = Turno(
            paciente_id=form.paciente.data,
            odontologo_id=form.odontologo.data,
            fecha=form.fecha.data
        )
        db.session.add(turno)
        db.session.commit()
        flash('Turno registrado correctamente.', 'success')
        return redirect(url_for('turnos'))

    return render_template('nuevo_turno.html', form=form)


@app.route('/eliminar_turno/<int:id>', methods=['POST'])
def eliminar_turno(id):
    turno = Turno.query.get_or_404(id)
    db.session.delete(turno)
    db.session.commit()
    flash('Turno eliminado correctamente.', 'success')
    return redirect(url_for('turnos'))


@app.route('/turnos')
def turnos():
    lista_turnos = Turno.query.order_by(Turno.fecha).all()
    return render_template('turnos.html', turnos=lista_turnos)



@app.route('/historias_clinicas')
def historias_clinicas():
    lista_historias = HistoriaClinica.query.all()
    return render_template('historias_clinicas.html', historias=lista_historias)


@app.route('/nueva_historia_clinica', methods=['GET', 'POST'])
def nueva_historia_clinica():
    form = HistoriaClinicaForm()
    form.paciente.choices = [(p.id, f"{p.nombre} {p.apellido}") for p in Paciente.query.all()]

    if form.validate_on_submit():
        historia = HistoriaClinica(
            paciente_id=form.paciente.data,
            
            # 🔧 CORREGIDO: usamos el campo observaciones
            observaciones=form.observaciones.data
        )
        db.session.add(historia)
        db.session.commit()
        flash('Historia clínica registrada.', 'success')
        return redirect(url_for('historias_clinicas'))

    return render_template('nueva_historia_clinica.html', form=form)



@app.route('/tratamientos')
def tratamientos():
    lista_tratamientos = Tratamiento.query.all()
    return render_template('tratamientos.html', tratamientos=lista_tratamientos)



@app.route('/nuevo_tratamiento', methods=['GET', 'POST'])
def nuevo_tratamiento():
    form = TratamientoForm()
    form.historia_clinica.choices = [(h.id, f"{h.paciente.nombre} {h.paciente.apellido} - {h.fecha.strftime('%d/%m/%Y')}") for h in HistoriaClinica.query.all()]

    if form.validate_on_submit():
        tratamiento = Tratamiento(
            historia_clinica_id=form.historia_clinica.data,
            nombre=form.nombre.data,
            descripcion=form.descripcion.data
        )
        db.session.add(tratamiento)
        db.session.commit()
        flash('Tratamiento registrado correctamente.', 'success')
        return redirect(url_for('tratamientos'))

    return render_template('nuevo_tratamiento.html', form=form)



@app.route('/paciente/<int:id>/historia_clinica')
def detalle_historia(id):
    paciente = Paciente.query.options(
        joinedload(Paciente.historias_clinicas)
            .joinedload(HistoriaClinica.tratamientos)
    ).get_or_404(id)

    return render_template('detalle_historia.html', paciente=paciente, historias=paciente.historias_clinicas)



@app.route('/admin/editar_usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@rol_requerido(['admin'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = EditarUsuarioForm(obj=usuario)

    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.rol = form.rol.data
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('administrar_usuarios'))

    return render_template('editar_usuario.html', form=form, usuario=usuario)



@app.route('/admin/eliminar_usuario/<int:id>', methods=['POST'])
@login_required
@rol_requerido(['admin'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.username == 'admin':
        flash('No se puede eliminar al usuario administrador principal.', 'danger')
        return redirect(url_for('administrar_usuarios'))

    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('administrar_usuarios'))

