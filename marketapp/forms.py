from django import forms
from .models import *
from datetime import date, timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio','stock', 'categoria', 'imagen', 'envase']
        

class OrdenForm(forms.ModelForm):
    direccion_nueva = forms.CharField(required=True, label="Dirección", widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Escribe tu dirección...'}))
    ciudad_nueva = forms.CharField(required=True, max_length=100, label="Ciudad")
    distrito_nuevo = forms.CharField(required=True, max_length=100, label="Distrito")
    codigo_postal_nuevo = forms.CharField(required=False, max_length=10, label="Código Postal")
   
    class Meta:
        model = Orden
        fields = [ 'first_name','last_name', 'email', 'telefono', 'fecha_entrega_deseada']
        
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
        }
        
        hoy = datetime.today()
        dias_hasta_domingo = (6 - hoy.weekday()) % 7 or 7
        fecha_domingo = hoy + timedelta(days=dias_hasta_domingo)
        fecha_max = fecha_domingo + timedelta(days=1)
        
        widgets = {
            'last_name': forms.TextInput(attrs={'required': 'required'}),
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'email': forms.EmailInput(attrs={'required': 'required'}),
            'telefono': forms.TextInput(attrs={'required': 'required'}),
            'fecha_entrega_deseada': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': fecha_domingo.strftime('%Y-%m-%d'), 
                    'max': fecha_max.strftime('%Y-%m-%d'), 
                    'class': 'bg-white p-2 rounded border',
                    'value': fecha_domingo.strftime('%Y-%m-%d'),
                }),
        }
    
class ElementoOrdenForm(forms.ModelForm):
    class Meta:
        model = ElementoOrden
        fields = ['producto', 'cantidad']
        
class OrdenEditForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'fecha_entrega_deseada']
        
    
ElementoOrdenFormSet = inlineformset_factory(
    Orden, 
    ElementoOrden, 
    form=ElementoOrdenForm, 
    extra=1,
    can_delete=True
)


class RegistroUsuariosForm(UserCreationForm):
    email = forms.EmailField(label="Email Usuario")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        

    
class UserEditForm(forms.ModelForm):
    imagen = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'ciudad', 'distrito', 'codigo_postal', 'imagen']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(username=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("El email ya está en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

        
class UserAdminEditForm(forms.ModelForm):
    imagen = forms.ImageField(required=False, label="Avatar")
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'ciudad', 'distrito', 'codigo_postal', 'imagen', 'tipo_usuario']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Usuario.objects.filter(username=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("El email ya está en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        UserModel = get_user_model()

        if '@' in username:  
            try:
                user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
                return user.username
            except UserModel.DoesNotExist:
                pass

        return username