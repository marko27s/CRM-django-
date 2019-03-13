from django.test import TestCase, Client
from cases.models import Case
from leads.models import Lead
from common.models import User, Comment, Attachments
from accounts.models import Account
from leads.tasks import *
from leads.forms import *


class TestLeadModel(object):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(
            username='jorge', email='j@mp.com', role="ADMIN")
        self.user.set_password('jorge2293')
        self.user.save()

        self.client.login(username='j@mp.com', password='jorge2293')

        self.account = Account.objects.create(name="account",
                                              email="account@gmail.com",
                                              phone="12345",
                                              billing_address_line="",
                                              billing_street="Arcade enclave colony",
                                              billing_city="NewTown",
                                              billing_state="California",
                                              billing_postcode="5009",
                                              billing_country="AD",
                                              website="account.com",
                                              industry="IT",
                                              description="account",
                                              created_by=self.user)

        self.lead = Lead.objects.create(title="LeadCreation",
                                        first_name="Alisa",
                                        last_name="k",
                                        email="Alisak1993@gmail.com",
                                        address_line="",
                                        street="Arcade enclave colony",
                                        city="NewTown",
                                        state="California",
                                        postcode="5079",
                                        country="AD",
                                        website="www.gmail.com",
                                        status="assigned",
                                        source="Call",
                                        opportunity_amount="700",
                                        description="Iam an Lead",
                                        created_by=self.user)
        self.case = Case.objects.create(
            name="Rose", case_type="Problem",
            status="New",
            account=self.account,
            priority="Low", description="something",
            created_by=self.user, closed_on="2016-05-04")
        self.comment = Comment.objects.create(
            comment='testikd', case=self.case, commented_by=self.user)
        self.attachment = Attachments.objects.create(
            attachment='image.png',
            case=self.case, created_by=self.user,
            account=self.account)


class LeadsPostrequestTestCase(TestLeadModel, TestCase):
    def test_valid_postrequesttestcase_date(self):
        data = {'title': 'LeadCreation', 'first_name': "micky",
                'last_name': "Alisa", 'email': "Alisamicky1993@gmail.com",
                'account': self.account,
                'address_line': "",
                'street': "Arcade enclave colony",
                'city': "NewTown",
                'state': "California",
                'postcode': "579",
                'country': "AD",
                'website': "www.gmail.com", "status ": "assigned",
                "source": "Call",
                'opportunity_amount': "700",
                'description': "Iam an Lead"}
        resp = self.client.post('/leads/create/', data)
        self.assertEqual(resp.status_code, 200)

    def test_leads_list(self):
        self.lead = Lead.objects.all()
        get_name = Lead.objects.get(first_name='Alisa')
        # print(get_name.first_name+get_name.last_name,str(get_name))
        self.assertEqual(get_name.first_name +
                         get_name.last_name, str(get_name))
        response = self.client.get('/leads/list/')
        self.assertEqual(response.status_code, 200)

    def test_leads_list_html(self):
        response = self.client.get('/leads/list/')
        self.assertTemplateUsed(response, 'leads.html')


class LeadsCreateUrlTestCase(TestLeadModel, TestCase):
    def test_leads_create_url(self):
        response = self.client.post('/leads/create/', {
                                    'title': 'LeadCreation',
                                    'first_name': "micky",
                                    'email': "Alisamicky1993@gmail.com",
                                    'account': self.account,
                                    'address_line': "",
                                    'street': "Arcade enclave colony",
                                    'city': "NewTown",
                                    'state': "California",
                                    'postcode': "579",
                                    'country': "AD",
                                    'website': "www.gmail.com",
                                    "status": "assigned",
                                    "source": "Call",
                                    'opportunity_amount': "700",
                                    'description': "Iam an Lead",
                                    'created_by': self.user})
        self.assertEqual(response.status_code, 200)

    def test_leads_create_html(self):
        response = self.client.post('/leads/create/', {
            'title': 'LeadCreation', 'name': "micky",
            'email': "Alisamicky1993@gmail.com", 'account': self.account,
            'address_line': "",
            'street': "Arcade enclave colony", 'city': "NewTown",
            'state': "California", 'postcode': "579", 'country': "AD",
            'website': "www.gmail.com", 'status': "assigned",
            "source": "Call", 'opportunity_amount': "700",
            'description': "Iam an Lead", 'created_by': self.user})
        # self.assertTemplateUsed(response, 'create_lead.html')
        self.assertEqual(response.status_code, 200)


class LeadsEditUrlTestCase(TestLeadModel, TestCase):
    def test_leads_editurl(self):
        response = self.client.get('/leads/' + str(self.lead.id) + '/edit/')
        self.assertEqual(response.status_code, 200)


class LeadsViewTestCase(TestLeadModel, TestCase):

    def test_leads_view(self):
        Lead.objects.create(title="LeadCreationbylead",
                            first_name="Alisa",
                            last_name="k",
                            email="Alisa@gmail.com",
                            address_line="",
                            street="Arcade enclave colony",
                            city="NewTown",
                            state="California",
                            postcode="579",
                            country="AD",
                            website="www.gmail.com",
                            status='converted',
                            source="Call",
                            opportunity_amount="900",
                            description="Iam an Opportunity",
                            created_by=self.user)
        response = self.client.get('/leads/' + str(self.lead.id) + '/view/')
        self.assertEqual(response.status_code, 200)


class LeadListTestCase(TestLeadModel, TestCase):

    def test_leads_list(self):
        self.lead = Lead.objects.all()
        response = self.client.get('/leads/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads.html')

    def test_leads_list_queryset(self):
        self.lead = Lead.objects.all()
        data = {'fist_name': "marphy", 'last_name': "racheal",
                'city': "hyd", 'email': "contact@gmail.com",
                'status': "Assigned"}
        response = self.client.post('/leads/list/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads.html')


class GetLeadsViewTestCase(TestLeadModel, TestCase):
    def test_get_lead(self):
        url = '/leads/get/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class LeadsRemoveTestCase(TestLeadModel, TestCase):

    def test_leads_remove(self):
        response = self.client.get('/leads/' + str(self.lead.id) + '/delete/')
        self.assertEqual(response['location'], '/leads/list/')

    def test_leads_remove_status(self):
        Lead.objects.filter(id=self.lead.id).delete()
        response = self.client.get('/leads/list/')
        self.assertEqual(response.status_code, 200)


class UpdateLeadTestCase(TestLeadModel, TestCase):

    def test_update_lead(self):
        url = '/leads/' + str(self.lead.id) + '/edit/'
        data = {
            'title': "Creation", 'first_name': "marphy", 'last_name': "k",
            'email': "meg@gmail.com", 'account': self.account,
            'address_line': "",
            'street': "Arcade enclave colony", 'city': "NewTown",
            'state': "California",
            'postcode': "579", 'country': "AD",
            'phone': "+917894563452",
            'website': "www.gmail.com", 'status': None,
            'source': "", 'opportunity_amount': "700",
            'description': "Iam an Lead", 'created_by': self.user}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class LeadDetailTestCase(TestLeadModel, TestCase):
    def test_lead_detail(self):
        url = '/leads/' + str(self.lead.id) + '/view/'
        response = self.client.get(url, {'status': ''})
        self.assertEqual(response.status_code, 200)


class CommentTestCase(TestLeadModel, TestCase):
    def test_comment_add(self):
        response = self.client.post(
            '/leads/comment/add/', {'leadid': self.lead.id})
        self.assertEqual(response.status_code, 200)

    def test_comment_edit(self):
        response = self.client.post(
            '/leads/comment/edit/', {'commentid': self.comment.id})
        self.assertEqual(response.status_code, 200)

    def test_comment_delete(self):
        response = self.client.post(
            '/leads/comment/remove/', {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)


class AttachmentTestCase(TestLeadModel, TestCase):
    def test_attachment_add(self):
        response = self.client.post(
            '/leads/attachment/add/', {'leadid': self.lead.id})
        self.assertEqual(response.status_code, 200)

    def test_attachment_delete(self):
        response = self.client.post(
            '/leads/attachment/remove/', {'attachment_id': self.attachment.id})
        self.assertEqual(response.status_code, 200)


class TestTemplates(TestLeadModel, TestCase):
    def test_lead_list_view(self):
        resp = self.client.post('/leads/list/', {'name': 'trevor',
                                                 'tag': "123",
                                                 'source': "call",
                                                 'assigned_to': '1',
                                                 'tab_status': 'Open'})
        self.assertEqual(resp.status_code, 200)
        # print(resp.name)
        # self.assertTrue(resp.name)

    # def test_lead_from_site(self):
    #     resp = self.client.get()


class TestConvertLeadView(TestLeadModel, TestCase):
    def test_get_fun(self):
        resp = self.client.get('/leads/' + str(self.lead.id) + '/convert/')
        self.assertEqual(resp.status_code, 302)
