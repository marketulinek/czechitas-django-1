from django.forms import ModelForm, ValidationError
from crm.models import Company


class CompanyForm(ModelForm):

    def clean_identification_number(self):
        identification_number = self.cleaned_data['identification_number']

        if len(identification_number) != 8:
            raise ValidationError('Identification number has incorrect length!')
        
        return identification_number

    class Meta:
        model = Company
        fields = ['name', 'status', 'phone_number', 'email', 'identification_number']