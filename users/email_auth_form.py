from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            self.cleaned_data['username'] = user.username
        except UserModel.DoesNotExist:
            raise forms.ValidationError('Correo electrónico o contraseña incorrectos.')
        return super().clean()
