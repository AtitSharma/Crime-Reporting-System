from django import forms

from user_management.models import User



class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255,min_length=8,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255,min_length=8,widget=forms.PasswordInput)

    class Meta :
        model = User
        fields = [
            "email","first_name","middle_name","last_name","police_station"
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Enter your email',
            'password1': 'Enter your password',
            'password2': 'Confirm your password',
            'first_name': 'First name',
            'last_name': 'Last name',
            'middle_name': 'Middle name',
            "police_station" : "Police Station"
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, ''),
                'class': 'your-input-class',
            })

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The provided email Already exits in our system")
        return email
    
    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1!=password2:
            raise forms.ValidationError("The provided password did'nt match with each other ")
        return self.cleaned_data
    

    def save(self):
        email = self.cleaned_data.get("email")
        password=self.cleaned_data.get("password2")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        middle_name = self.cleaned_data.get("middle_name")
        police_station = self.cleaned_data.get("police_station")
        user = User(email=email,first_name=first_name,last_name=last_name,middle_name=middle_name,police_station=police_station)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
    


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)