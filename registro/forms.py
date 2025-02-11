from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from clientes.models import InformacionCliente



STYLE = "inputs"

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar Contraseña",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": STYLE}),
            "email": forms.EmailInput(attrs={"class": STYLE}),
            "password1": forms.PasswordInput(attrs={"class": STYLE}),
            "password2": forms.PasswordInput(attrs={"class": STYLE}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum():
            raise forms.ValidationError(
                "El nombre de usuario solo puede contener letras y números."
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        perfil = InformacionCliente.objects.create(
            cliente=user,
            correo=self.cleaned_data.get("email"),
        )
        perfil.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
        labels = {
            "username": "Usuario",
            "password": "Contraseña",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Ingrese su usuario"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError("El usuario no existe.", code="username_not_found")
        elif not user.is_active:
            raise forms.ValidationError("Esta cuenta está inactiva.", code="inactive")
        return username
    
    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        user = User.objects.filter(username=username).first()

        if user and not user.check_password(password):
            raise forms.ValidationError(
                "La contraseña es incorrecta.", code="invalid_password"
            )
        return password

