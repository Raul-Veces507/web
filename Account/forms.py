from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Ingrese Contraseña',
    }))

    Confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirmar Contraseña',
    }))
        # Widget personalizado para el campo "Sexo"
    Sexo = forms.ChoiceField(
        choices=[('', 'Seleccione Sexo '),(1, 'Masculino'), (2, 'Femenino'),(3, 'No especificado')],
        widget=forms.Select(attrs={'placeholder': 'Seleccione Sexo'}),
         required=True
    )

    # Widget personalizado para el campo "Fecha"
    FechaN = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Seleccione Fecha'}),
    )
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','Sexo','FechaN','password']

    def __init__(self,*args,**kwargs):
    
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Ingrese Nombre'
        self.fields['last_name'].widget.attrs['placeholder']='Ingrese Apellido'
        self.fields['phone_number'].widget.attrs['placeholder']='Ingrese Telefono'
        self.fields['email'].widget.attrs['placeholder']='Ingrese Email'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('Confirm_password')
        if password != confirm_password:
            
            raise forms.ValidationError(
                "El password no coincide"
            )

   