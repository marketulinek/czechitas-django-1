import django_tables2 as tables
from crm.models import Employee


class EmployeeTable(tables.Table):
    last_name = tables.Column(accessor='user.last_name', verbose_name='Last Name')
    first_name = tables.Column(accessor='user.first_name', verbose_name='First Name')
    is_active = tables.Column(verbose_name='Active')
    actions = tables.TemplateColumn(verbose_name='', template_name='employee/list_action_column.html', orderable=False)

    class Meta:
        model = Employee
        fields = ('last_name', 'first_name', 'department', 'office_number', 'supervisor', 'is_active')
        attrs = {'class': "table table-hover django-table"}