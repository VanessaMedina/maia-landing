# core/models.py
from django.db import models
from django.contrib.auth.models import User

class PerfilDocente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    centro_educativo = models.CharField(max_length=200)
    codigo_centro = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.centro_educativo}"

class Estudiante(models.Model):
    docente = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_anonimo = models.CharField(max_length=10)
    grado_seccion = models.CharField(max_length=50)
    distintivo = models.CharField(
        max_length=100,
        blank=True,
        help_text="Rasgo observable (ej: 'camiseta rayada', 'usa lentes')"
    )

    class Meta:
        unique_together = ('docente', 'codigo_anonimo')

    def __str__(self):
        return f"{self.codigo_anonimo} ({self.distintivo or 'Sin distintivo'})"

class RegistroAula(models.Model):
    # === A. CONTEXTO (obligatorio) ===
    MATERIAS = [
        ('matematica', 'Números y Formas'),
        ('lenguaje', 'Comunicación'),
        ('ciencias', 'Ciencia y Tecnología'),
        ('sociales', 'Ciudadanía y Valores'),
        ('ingles', 'Inglés'),
        ('artistica', 'Expresión Artística'),
        ('otra', 'Otra'),
    ]
    TIPOS_ACTIVIDAD = [
        ('explicacion', 'Explicación oral'),
        ('individual', 'Trabajo individual'),
        ('grupal', 'Trabajo grupal'),
        ('evaluacion', 'Evaluación formativa'),
        ('practica', 'Actividad práctica'),
    ]
    MOMENTOS = [
        ('inicio', 'Inicio'),
        ('desarrollo', 'Desarrollo'),
        ('cierre', 'Cierre'),
    ]

    # === B. NIVEL DE REGISTRO ===
    NIVELES = [
        ('individual', 'Estudiante individual'),
        ('grupo', 'Grupo completo'),
        ('subgrupo', 'Subgrupo'),
    ]
    nivel_registro = models.CharField(max_length=20, choices=NIVELES)
    codigo_estudiante = models.CharField(max_length=10, blank=True)

    # === C. VARIABLES PRINCIPALES (0–3) ===
    atencion = models.IntegerField(choices=[(i, i) for i in range(4)])
    instrucciones = models.IntegerField(choices=[(i, i) for i in range(4)])
    autorregulacion = models.IntegerField(choices=[(i, i) for i in range(4)])
    participacion = models.IntegerField(choices=[(i, i) for i in range(4)])
    interaccion_social = models.IntegerField(choices=[(i, i) for i in range(4)])

    # === D. EVENTO PUNTUAL (opcional) ===
    EVENTOS = [
        ('conducta', 'Cambio abrupto de conducta'),
        ('conflicto', 'Conflicto con compañero'),
        ('abandono', 'Abandono de tarea'),
        ('ruido', 'Ruido ambiental intenso'),
        ('recurso', 'Falta de material didáctico'),
        ('otro', 'Otro'),
    ]
    

    class Meta:
        ordering = ['-fecha']


    # === E. OBSERVACIÓN BREVE (≤60 caracteres) ===
    observacion_breve = models.CharField(max_length=60, blank=True)

       #DEFINIENDO CAMPOS DE CONSTANTS
    evento_puntual = models.CharField(max_length=20, choices=EVENTOS, blank=True)
    evento_otro = models.CharField(max_length=60, blank=True)

    docente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    grado_seccion = models.CharField(max_length=50)
    centro_educativo = models.CharField(max_length=200, blank=True)
    materia = models.CharField(max_length=20, choices=MATERIAS)
    materia_otra = models.CharField(max_length=50, blank=True)
    tipo_actividad = models.CharField(max_length=20, choices=TIPOS_ACTIVIDAD)
    momento = models.CharField(max_length=20, choices=MOMENTOS)
    nivel_registro = models.CharField(max_length=20, choices=NIVELES)
    codigo_estudiante = models.CharField(max_length=10, blank=True)
    atencion = models.IntegerField(choices=[(i, i) for i in range(4)])
    instrucciones = models.IntegerField(choices=[(i, i) for i in range(4)])
    autorregulacion = models.IntegerField(choices=[(i, i) for i in range(4)])
    participacion = models.IntegerField(choices=[(i, i) for i in range(4)])
    interaccion_social = models.IntegerField(choices=[(i, i) for i in range(4)])
    evento_puntual = models.CharField(max_length=20, choices=EVENTOS, blank=True)
    evento_otro = models.CharField(max_length=60, blank=True)
    observacion_breve = models.CharField(max_length=60, blank=True)

    class Meta:
        verbose_name = "Registro MaIA"
        verbose_name_plural = "Registros MaIA"
        ordering = ['-fecha']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.nivel_registro == 'individual' and not self.codigo_estudiante:
            raise ValidationError("El código del estudiante es obligatorio para registros individuales.")
        if self.nivel_registro != 'individual':
            self.codigo_estudiante = ''
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
