from django.views.generic import CreateView, ListView, TemplateView
import crm.models as models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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

class OpportunityCreateView(LoginRequiredMixin, CreateView):
    model = models.Opportunity
    template_name = 'opportunity/create.html'
    fields = ['company', 'sales_manager', 'primary_contact', 'description', 'status']
    success_url = reverse_lazy('index')

class OpportunityListView(ListView):
    model = models.Opportunity
    template_name = 'opportunity/list.html'
    fields = ['company', 'sales_manager', 'primary_contact', 'description']