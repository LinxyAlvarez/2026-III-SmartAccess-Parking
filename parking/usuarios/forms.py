from django import forms
from django.contrib.auth.models import User
from parking.models import Acreditacion


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])

        if commit:
            usuario.save()

        return usuario


class AcreditacionForm(forms.ModelForm):
    class Meta:
        model = Acreditacion
        fields = [
            "usuario",
            "tipo",
            "documento",
            "fecha_validacion",
            "estado",
        ]
        widgets = {
            "fecha_validacion": forms.DateInput(
                attrs={"type": "date"}
            ),
        }