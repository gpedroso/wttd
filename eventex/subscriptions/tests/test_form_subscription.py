from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        expected = ['name','cpf','email','phone']
        form = SubscriptionForm()
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accpet digits."""
        form = self.make_validated_form(cpf='ABCD5678910')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')
        form = self.make_validated_form(cpf='123456789000000')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be cpitalizaed"""
        #GABRIEL Pedroso -> Gabriel Pedroso
        form = self.make_validated_form(name='GABRIEL Pedroso')
        self.assertEqual('Gabriel Pedroso', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and phone are optional, but one must be informed"""
        form = self.make_validated_form(email='',phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def test_must_inform_email_correct_or_phone(self):
        """Email and phone are optional, but one must be informed"""
        form = self.make_validated_form(email='456',phone='')
        self.assertListEqual(['__all__', 'email'], sorted(list(form.errors)))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        error_list = errors[field]
        exception = error_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self,**kwargs):
        valid = dict(name='Gabriel Pedorso', cpf='12345678910',
                email='gpedroso@gmail.com', phone='11-111111111')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
