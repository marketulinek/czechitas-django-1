from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from crm.forms import CompanyForm, OpportunityForm, RegisterUserForm
import crm.models as models
import crm.tables as tables
import crm.filters as filters


class IndexView(TemplateView):
    template_name = 'index.html'

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CompanyForm
    template_name = 'company/create_company.html'
    success_url = reverse_lazy('company_list')
    success_message = _('Company successfully created')

class CompanyListView(ListView):
    model = models.Company
    template_name = 'company/list.html'
    fields = ['name', 'status', 'phone_number', 'email', 'address']

class OpportunityCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    form_class = OpportunityForm
    template_name = 'opportunity/create.html'
    success_url = reverse_lazy('opportunity_list')
    # Translators: This message is shown after successful creation of a company
    success_message = _('Opportunity successfully created')

class OpportunityListView(ListView):
    model = models.Opportunity
    template_name = 'opportunity/list.html'
    fields = ['company', 'sales_manager', 'primary_contact', 'description', 'created_at']
    ordering = '-created_at'

class EmployeeListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = models.Employee
    table_class = tables.EmployeeTable
    template_name = 'employee/list.html'
    filterset_class = filters.EmployeeFilter

class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['department', 'office_number', 'supervisor']
    template_name = 'employee/update_employee.html'
    success_url = reverse_lazy('index')
    success_message = _('Data was updated successfully')

    # The logged-in user can edit himself 
    def get_object(self, queryset=None):
        return self.request.user.employee

class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'