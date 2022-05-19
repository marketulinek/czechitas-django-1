from django.forms import ModelForm, ValidationError
from crm.models import Company


class CompanyForm(ModelForm):

    def clean_identification_number(self):
        identification_number = self.cleaned_data['identification_number']

        if not identification_number.isdigit():
            raise ValidationError('Identification number has to contain only numbers!')
        if len(identification_number) != 8:
            raise ValidationError('Identification number has incorrect length!')
        
        return identification_number

    def clean_email(self):
        email = self.cleaned_data['email']

        if email and '@' not in email:
            raise ValidationError('E-mail has incorrect form!')

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if phone_number:
            if len(phone_number) == 9 and phone_number.isdigit():
                pass
            elif len(phone_number) == 13 and phone_number.startswith('+420') and phone_number[1:].isdigit():
                pass
            else:
                raise ValidationError('Format of phone number must be 123456789 or +420123456789.')

        return phone_number

    class Meta:
        model = Company
        fields = ['name', 'status', 'phone_number', 'email', 'identification_number']