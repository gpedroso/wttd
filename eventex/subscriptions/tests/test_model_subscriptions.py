from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.obj = Subscription (
            name='Gabriel Pedroso',
            cpf='32445054818',
            email='gpedroso@gmail.com',
            phone='11-11111111'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """ Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Gabriel Pedroso', str(self.obj))