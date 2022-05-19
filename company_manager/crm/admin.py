from django.contrib import admin
import crm.models as models

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'phone_number', 'email', 'address', 'status', 'identification_number', 'www']
    readonly_fields = ['name', 'status', 'identification_number']
    list_display = ['name', 'status', 'email', 'www']
    list_filter = ['status', ['email', admin.EmptyFieldListFilter], ['www', admin.EmptyFieldListFilter]]
    search_fields = ['name', 'email', 'identification_number', 'opportunity__description', 'www']

class OpportunityAdmin(admin.ModelAdmin):
    fields = ['company', 'sales_manager', 'description', 'status', 'rating', 'created_at']
    readonly_fields = ['rating', 'rating', 'created_at']
    list_display = ['created_at', 'company', 'sales_manager', 'description', 'status', 'rating']
    list_filter = ['sales_manager', 'status']
    search_fields = ['company', 'sales_manager', 'description']

class EmployeeAdmin(admin.ModelAdmin):
    fields = ['user', 'card_number', 'department', 'supervisor']
    readonly_fields = ['user', 'card_number']
    list_display = ['__str__', 'card_number', 'department', 'supervisor', 'start_date', 'end_date']
    list_filter = ['department']
    search_fields = ['user__last_name', 'user__first_name', 'department']

admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Opportunity, OpportunityAdmin)
admin.site.register(models.Employee, EmployeeAdmin)