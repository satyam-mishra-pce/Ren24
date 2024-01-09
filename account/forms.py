from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    # define any extra fields or widgets here
    # for example, you can use a DateInput widget for the dob field
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        # specify the fields you want to include in the form
        fields = ['image', 'phone', 'dob', 'sem', 'college', 'address']
