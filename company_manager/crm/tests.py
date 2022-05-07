from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from crm.models import Company, Opportunity


class CRMViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('tester', 'tester@testing.cz', 'test')
        self.user.user_permissions.add(Permission.objects.get(codename='add_opportunity'))
        Company.objects.create(name='THE MAMA AI', phone_number='123', identification_number='87654321')

    def test_get_company_create(self):
        self.client.login(username='tester', password='test')
        response = self.client.get(reverse('company_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_company_create(self):
        self.client.login(username='tester', password='test')
        response = self.client.post(reverse('company_create'), data={
            'name': 'Test Company',
            'status': 'N',
            'identification_number': '12345678'
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Company.objects.count(), 2)

    def test_company_list_not_signed(self):
        response = self.client.get(reverse('company_list'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/company/')

    def test_company_list(self):
        self.client.login(username='tester', password='test')
        response = self.client.get(reverse('company_list'))
        self.assertContains(response, 'THE MAMA AI')

    def test_post_opportunity_create(self):
        self.client.login(username='tester', password='test')
        response = self.client.post(reverse('opportunity_create'), data={
            'company': '1',
            'sales_manager': '1',
            'status': '1'
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opportunity.objects.count(), 1)