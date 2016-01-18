from django.conf import settings
from django.core import mail
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import resolve_url as r
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)
    return empty_form(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',{'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    #send email
    _send_email('subscriptions/subscription_email.txt'
                ,{'subscription': subscription}
                ,'Confirmação Inscrição'
                ,settings.DEFAULT_FROM_EMAIL
                ,subscription.email )

    return HttpResponseRedirect(r('subscriptions:detail',subscription.pk))

def _send_email(template, context, title, from_, to):
    body = render_to_string(template, context)
    mail.send_mail(title,
                   body,
                   from_,
                   [from_,to],)

def empty_form(request):
    return render(request,'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})

def detail(request,pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})
