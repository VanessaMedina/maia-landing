from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroMaIAForm, RegistroDocenteForm 

def registro_docente(request):
    """Vista pública para crear nueva cuenta de docente"""
    if request.method == 'POST':
        form = RegistroDocenteForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: loguear automáticamente al nuevo usuario
            from django.contrib.auth import login
            login(request, user)
            return redirect('dashboard_docente')
    else:
        form = RegistroDocenteForm()
    return render(request, 'core/registro.html', {'form': form})

@login_required
def dashboard_docente(request):
    """Dashboard principal para docentes autenticados"""
    return render(request, 'core/dashboard.html')

@login_required
def registro_maia(request):
    """Vista privada para registrar observaciones"""
    if request.method == 'POST':
        form = RegistroMaIAForm(request.POST, user=request.user)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.docente = request.user
            registro.save()
            return redirect('dashboard_docente')  # o donde se quiera redirigir
    else:
        form = RegistroMaIAForm(user=request.user)
    
     # Lista de campos para el template
    campos_variables = ['atencion', 'instrucciones', 'autorregulacion', 'participacion', 'interaccion_social']
    
    return render(request, 'core/registro_maia.html', {
        'form': form,
        'campos_variables': campos_variables
    })