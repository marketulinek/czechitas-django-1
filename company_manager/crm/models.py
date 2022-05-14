from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from random import randrange


class Address(models.Model):
    street = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

class Company(models.Model):
    status_choices = (
        ('N', 'New'),
        ('L', 'Lead'),
        ('O', 'Opportunity'),
        ('C', 'Customer'),
        ('FC', 'Former Customer'),
        ('I', 'Inactive')
    )
    
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=2, default='N', choices=status_choices)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    identification_number = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    www = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Companies'

class Contact(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

class Opportunity(models.Model):
    status_choices = (
        ('1', 'Prospecting'),
        ('2', 'Analysis'),
        ('3', 'Proposal'),
        ('4', 'Negotiation'),
        ('5', 'Closed Won'),
        ('0', 'Closed Lost')
    )

    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    sales_manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    primary_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default='1', choices=status_choices)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.description}"

    class Meta:
        verbose_name_plural = 'Opportunities'
        get_latest_by = "created_at"

class Employee(models.Model):

    def get_one_year_from_today():
        return timezone.now() + timezone.timedelta(days=364)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=9, unique=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True, null=True)
    supervisor = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=get_one_year_from_today)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        card_number_exist = True
        while card_number_exist:

            new_card_number = ''
            for i in range(9):
                new_card_number += str(randrange(10))

            card_number_exist = Employee.objects.filter(card_number=new_card_number).exists()
        else:
            Employee.objects.create(user=instance, card_number=new_card_number)

@receiver(post_save, sender=Opportunity)
def create_opportunity(sender, instance, created, **kwargs):
    if created:
        subject = 'New Opportunity - ' + instance.company.name
        message = 'Hello, new opportunity was created. Bye.'
        from_email = 'robot@cm.cz'
        recipient_list = ['sales_manager@czechitas.cz']
        send_mail(subject, message, from_email, recipient_list)