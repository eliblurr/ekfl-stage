from .models import Patient
from django import forms

from django.core.exceptions import ValidationError


class PatientForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(PatientForm, self).clean()
        if cleaned_data.get("email") is None and cleaned_data.get("cellphone_1") is None and cleaned_data.get("cellphone_2") is None:
            raise ValidationError("Fields Email, Cellphone 1 and Cellphone 2 cannot all be empty")
        return cleaned_data
    class Meta:
        model = Patient
        fields = '__all__'