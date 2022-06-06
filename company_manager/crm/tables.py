import django_tables2 as tables
from crm.models import Opportunity


class OpportunityTable(tables.Table):
    company = tables.LinkColumn

    class Meta:
        model = Opportunity
        fields = ('company', 'sales_manager', 'status')