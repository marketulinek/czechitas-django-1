import django_filters
from crm.models import Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div


class EmployeeFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        Div(
            Div('last_name', css_class='col-2'),
            Div('first_name', css_class='col-2'),
            Div('department', css_class='col-2'),
            Div('office_number', css_class='col-2'),
            Div('supervisor', css_class='col-2'),
            Submit('submit', 'Filter', css_class='btn-company col-1'),
            css_class='row'
        )
    )

class EmployeeFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'department', 'office_number', 'supervisor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = EmployeeFilterFormHelper()