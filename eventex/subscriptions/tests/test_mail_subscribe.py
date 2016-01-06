from django.core import mail
from django.test import TestCase


class SubscribePost(TestCase):
    def setUp(self):
        data = dict(name="Gabriel Pedroso", cpf="12345678912", email="gpedroso@gmail.com", phone="11-98822-6571")
        self.resp = self.client.post('/inscricao/',data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação Inscrição'
        self.assertEqual(expect,self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect,self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br','gpedroso@gmail.com']
        self.assertEqual(expect,self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Gabriel Pedroso',
            '12345678912',
            'gpedroso@gmail.com',
            '11-98822-6571',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

