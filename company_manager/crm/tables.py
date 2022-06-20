import django_tables2 as tables
from crm.models import Opportunity


class OpportunityTable(tables.Table):

    class Meta:
        model = Opportunity
        fields = ('created_at', 'company', 'sales_manager', 'primary_contact', 'description', 'status')
        attrs = {"class": "table table-hover"}