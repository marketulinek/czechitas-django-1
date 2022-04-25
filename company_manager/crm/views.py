from django.views.generic import CreateView, ListView, TemplateView, UpdateView
import crm.models as models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

class IndexView(TemplateView):
    template_name = 'index.html'

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Company
    template_name = 'company/create_company.html'
    fields = ['name', 'status', 'phone_number', 'email', 'identification_number']
    success_url = reverse_lazy('company_list')

class CompanyListView(ListView):
    model = models.Company
    template_name = 'company/list.html'
    fields = ['name', 'status', 'phone_number', 'email', 'address']

class OpportunityCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    model = models.Opportunity
    template_name = 'opportunity/create.html'
    fields = ['company', 'sales_manager', 'primary_contact', 'description', 'status']
    success_url = reverse_lazy('index')

class OpportunityListView(ListView):
    model = models.Opportunity
    template_name = 'opportunity/list.html'
    fields = ['company', 'sales_manager', 'primary_contact', 'description']

class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['department']
    template_name = 'employee/update_employee.html'
    success_url = reverse_lazy('index')
    success_message = 'Data was updated successfully'

    def get_object(self, queryset=None):
        return self.request.user.employee
