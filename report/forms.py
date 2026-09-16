from django import forms

from report.algorithms import nearest_police_station
from report.models import CrimeReport
from django.utils import timezone



class ReportCreationForm(forms.ModelForm):
    latitude = forms.CharField(widget=forms.HiddenInput(),required=False)
    longitude = forms.CharField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model = CrimeReport
        fields = ["name","email","title", "description", "crime_datetime", "proof_documents","phone_number","is_private","latitude","longitude"]
        widgets = {
            'crime_datetime': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': 'Check to keep this report private'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter report title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the incident in detail',
                'rows': 4
            }),
        }
        labels = {
            'is_private': 'Mark as private'
        }
        help_texts = {
            'is_private': 'Private reports will only be visible to you and administrators'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['crime_datetime'].required = True

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter your full name'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address'
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter your phone number'
        })
        self.fields['title'].widget.attrs.update({
            'placeholder': 'e.g., Theft at Main Street'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Provide detailed information about the incident...'
        })

        self.fields['name'].label = self.fields['name'].label or "Name"
        self.fields['name'].label += " *"
        self.fields['email'].label = self.fields['email'].label or "Email"
        self.fields['email'].label += " *"
        self.fields['phone_number'].label += " *"
        self.fields['title'].label += " *"
        self.fields['description'].label += " *"
        self.fields['crime_datetime'].label += " *"
        
        # Additional customization for the checkbox
        self.fields['is_private'].widget.attrs.update({
            'data-toggle': 'tooltip',
            'title': 'Check this to restrict visibility',
            'style': 'margin-right: 10px; cursor: pointer;'
        })

    def save(self,commit=True):
        latitude = self.cleaned_data.pop("latitude")
        longitude = self.cleaned_data.pop("longitude")
        police_station  = nearest_police_station(latitude,longitude)


        instance = CrimeReport.objects.create(**self.cleaned_data)
        instance.report_taken_by_station = police_station 
        instance.save()
        return instance
    
    def clean_crime_datetime(self):
        crime_date = self.cleaned_data.get("crime_datetime")
        if crime_date > timezone.now():
            raise forms.ValidationError("Crime date cannot be greater than today date")
        return crime_date


    def clean(self):
        return super().clean()

    

class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = ["title", "description", "crime_datetime", "proof_documents", "is_private"]
        widgets = {
            'crime_datetime': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': 'Check to keep this report private'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter report title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the incident in detail',
                'rows': 4
            }),
        }
        labels = {
            'is_private': 'Mark as private'
        }
        help_texts = {
            'is_private': 'Private reports will only be visible to you and administrators'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Additional customization for the checkbox
        self.fields['is_private'].widget.attrs.update({
            'data-toggle': 'tooltip',
            'title': 'Check this to restrict visibility',
            'style': 'margin-right: 10px; cursor: pointer;'
        })


class ContactDetailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your phone number'
    }))