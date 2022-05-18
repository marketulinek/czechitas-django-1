from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    street = models.CharField(_('Street'), max_length=200, blank=True, null=True)
    zip_code = models.CharField(_('Zip Code'), max_length=10, blank=True, null=True)
    city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Adresses')

class Company(models.Model):
    status_choices = (
        ('N', _('New')),
        ('L', _('Lead')),
        ('O', _('Opportunity')),
        ('C', _('Customer')),
        ('FC', _('Former Customer')),
        ('I', _('Inactive'))
    )
    
    name = models.CharField(_('Name'), max_length=50)
    status = models.CharField(max_length=2, default='N', choices=status_choices)
    phone_number = models.CharField(_('Phone number'), max_length=20, null=True, blank=True)
    email = models.CharField('E-mail', max_length=100, null=True, blank=True)
    identification_number = models.CharField(_('Identification number'), max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    www = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = _('Companies')

class Contact(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=20)
    email = models.CharField('E-mail', max_length=50)

class Opportunity(models.Model):
    status_choices = (
        ('1', _('Prospecting')),
        ('2', _('Analysis')),
        ('3', _('Proposal')),
        ('4', _('Negotiation')),
        ('5', _('Closed Won')),
        ('0', _('Closed Lost'))
    )

    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    sales_manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    primary_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    status = models.CharField(max_length=2, default='1', choices=status_choices)
    rating = models.DecimalField(_('Rating'), max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.description}"

    class Meta:
        verbose_name_plural = _('Opportunities')
        get_latest_by = "created_at"

class Employee(models.Model):

    def get_one_year_from_today():
        return  datetime.today() + timedelta(days=364)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(_('Department'), max_length=100, blank=True, null=True)
    office_number = models.CharField(_('Office Number'), max_length=20, blank=True, null=True)
    supervisor = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(_('Start Date'), auto_now_add=True)
    #start_date = models.DateField(default=django.utils.timezone.now)
    end_date = models.DateField(_('End Date'), default=get_one_year_from_today())

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=Opportunity)
def create_opportunity(sender, instance, created, **kwargs):
    if created:
        subject = 'New Opportunity - ' + instance.company.name
        message = 'Hello, new opportunity was created. Bye.'
        from_email = 'robot@cm.cz'
        recipient_list = ['sales_manager@czechitas.cz']
        send_mail(subject, message, from_email, recipient_list)
        