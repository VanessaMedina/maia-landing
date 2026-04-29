# core/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import RegistroAula, Estudiante, PerfilDocente

class RegistroDocenteForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Repetir contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': 'Tu nombre de usuario (ej: maria_maestra).',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            PerfilDocente.objects.create(user=user)
        return user

class RegistroMaIAForm(forms.ModelForm):
    class Meta:
        model = RegistroAula
        exclude = ['docente', 'fecha']
        widgets = {
            'grado_seccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2°A'
            }),
            'centro_educativo': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'materia_otra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la materia'
            }),
            'evento_otro': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 60
            }),
            'observacion_breve': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 60,
                'placeholder': 'Máx. 60 caracteres'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            try:
                perfil = self.user.perfildocente
                self.fields['centro_educativo'].initial = perfil.centro_educativo
            except PerfilDocente.DoesNotExist:
                pass
            
            estudiantes = Estudiante.objects.filter(docente=self.user)
            if estudiantes.exists():
                choices = [('', 'Seleccionar estudiante...')]
                for e in estudiantes:
                    label = f"{e.distintivo or e.codigo_anonimo} ({e.codigo_anonimo})"
                    choices.append((e.codigo_anonimo, label))
                self.fields['codigo_estudiante'] = forms.ChoiceField(
                    choices=choices,
                    required=False,
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
            else:
                self.fields['codigo_estudiante'].widget = forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: E07'
                })

    def clean(self):
        cleaned_data = super().clean()
        nivel_registro = cleaned_data.get('nivel_registro')
        codigo_estudiante = cleaned_data.get('codigo_estudiante')
        
        if nivel_registro == 'individual' and not codigo_estudiante:
            self.add_error('codigo_estudiante', 'Este campo es obligatorio para registros individuales.')
        
        return cleaned_data