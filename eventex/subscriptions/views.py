from django.conf import settings
from django.core import mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',{'form': form})

    #send email
    _send_email('subscriptions/subscription_email.txt'
                ,form.cleaned_data
                ,'Confirmação Inscrição'
                ,settings.DEFAULT_FROM_EMAIL
                ,form.cleaned_data['email'] )

    Subscription.objects.create(**form.cleaned_data)

    #success feedback
    messages.success(request, 'Inscrição realizada com sucesso!')
    return HttpResponseRedirect('/inscricao/')

def _send_email(template, context, title, from_, to):
    body = render_to_string(template, context)
    mail.send_mail(title,
                   body,
                   from_,
                   [from_,to],)

def new(request):
    return render(request,'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})