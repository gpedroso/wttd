from django.db import models
from hashlib import sha1
from random import SystemRandom
from uuid import uuid4
from eventex.subscriptions.validators import validate_cpf

char = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hash_(size=15, chars=char):
    word = ''.join(SystemRandom().choice(chars) for _ in range(size))
    salt = uuid4().hex
    key_hash = sha1(salt.encode() + word.encode()).hexdigest()
    #key_hash = uuid4().hex
    return key_hash

class Subscription(models.Model):
    name = models.CharField('Nome',max_length=100)
    cpf = models.CharField('CPF',max_length=11, validators=[validate_cpf])
    email = models.EmailField('e-mail', blank=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    paid = models.BooleanField('Pago', default=False)
    keyHash = models.CharField('hash',max_length=40, default=hash_)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering=('-created_at',)

    def __str__(self):
        return self.name