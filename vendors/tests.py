import unittest
from django.test import TestCase, Client
from vendors.models import Vendor
from django.contrib.auth.models import User
from vendors.views import VendorForm,vendor_create
#from .forms import *
# Create your tests here.

class Setup_Class(TestCase):

    def setUp(self):
        user = User.objects.create(username="ecain1", password="July1616",is_superuser=1, first_name="ethan", is_staff=1,is_active=1)
        user.save()
class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = VendorForm(data={'name' : "test", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':1})
        if form.is_valid() == True:
            form.save()
        else:
            print("Form was not valid")

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = VendorForm(data={'name' : "test", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':"1"})
        self.assertFalse(form.is_valid())




class User_Views_Test(Setup_Class):

    def test_add_user_view(self):
        response = self.client.get("/vendors/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vendors/vendor_list.html")

    # Invalid Data
    def test_add_user_invalidform_view(self):
        response = self.client.post("vendors/new/",{'name' : "test", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':"1"})
        self.assertTrue('"error": true' in response.content)

    # Valid Data
    def test_addvendor_form_view(self):
        c = Client()
        response = c.post('/vendors/new/', {'name' : 'test', 'website_address': 'http://www.google.com', 'contact_name': 'Joe Shmoe', 'contact_email': 'loukleon2021@yahoo.com', 'contact_phone': '2148675309', 'physical_address_line_1': '1000 new', 'physical_address_line_2': 'apt 200', 'physical_address_city': 'terrell', 'physical_address_state': 'TX', 'physical_address_postal_code': '75160', 'physical_address_country': 'USA', 'mailing_address_line_1': '1000 New', 'mailing_address_line_2': 'apt 200', 'mailing_address_state': 'TX', 'mailing_address_postal_code':'75160',
                                                           'mailing_address_country':'USA','active':True})
        self.assertEqual(response.status_code, 200)

'''
class VendorTest(TestCase):
    def test_vendor_creation(self):
        "creating Vendor"
        vendor = Vendor(name = "test", website_address="http://www.google.com", contact_name="Joe Shmoe", contact_email="loukleon2021@yahoo.com", contact_phone="2148675309", physical_address_line_1="1000 new", physical_address_line_2="apt 200",physical_address_city="terrell", physical_address_state="TX", physical_address_postal_code="75160", physical_address_country="USA", mailing_address_line_1="1000 New", mailing_address_line_2="apt 200", mailing_address_state="TX", mailing_address_postal_code="75160",
mailing_address_country="USA", active="1")

        "Checking to see if Vendor was actually created by testing name field"
        self.assertEqual(str(vendor),vendor.name)

    def test_NewVendorForm(self):
        vendor = Vendor(name="test", website_address="http://www.google.com", contact_name="Joe Shmoe",
                        contact_email="loukleon2021@yahoo.com", contact_phone="2148675309",
                        physical_address_line_1="1000 new", physical_address_line_2="apt 200",
                        physical_address_city="terrell", physical_address_state="TX",
                        physical_address_postal_code="75160", physical_address_country="USA",
                        mailing_address_line_1="1000 New", mailing_address_line_2="apt 200", mailing_address_state="TX",
                        mailing_address_postal_code="75160",
                        mailing_address_country="USA", active="1")
        vendor_form = VendorForm({'name' : "test", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':1},instance=vendor)
        if self.assertEquals(vendor_form.is_valid(),True):
            vendor.save()
        else:
            pass
    print("Why isnt this crap working?")
    def test_UpdateVendorForm(self):
        self.client.post('/edit', {'name' : "testing2", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':1})

    def test_NewVendorFailForm(self):
        response = self.client.post('/new', {'name' : "testing", 'website_address':"http://www.google.com", 'contact_name':"Joe Shmoe", 'contact_email':"loukleon2021@yahoo.com", 'contact_phone':"2148675309", 'physical_address_line_1':"1000 new", 'physical_address_line_2':"apt 200",'physical_address_city':"terrell", 'physical_address_state':"TX", 'physical_address_postal_code':"75160", 'physical_address_country':"USA", 'mailing_address_line_1':"1000 New", 'mailing_address_line_2':"apt 200", 'mailing_address_state':"TX", 'mailing_address_postal_code':"75160",
'mailing_address_country':"USA", 'active':"yes"})
        response.status_code = 200

'''
