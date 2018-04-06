from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth, messages
from accounts.models import Token
import sendgrid
from sendgrid.helpers.mail import *

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)

    url = request.build_absolute_uri(
        reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    )

    #url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    #url = request.build_absolute_uri(
    #    reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    #)
    message_body = f'Use this link to log in:\n\n{url}'

    send_mail('Your login link for Superlists', message_body,'noreply@superlists',[email])

    #messages.add_message(request,messages.SUCCESS,"Check your email, we've sent you a link you can use to log in.")
    messages.success(
        request,"Check your email, we've sent you a link you can use to log in.")
    return redirect('/')

def send_mail(link, message_body, fromemail, toemail):
    sg = sendgrid.SendGridAPIClient(apikey='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')

    from_email = Email(fromemail)
    to_email = Email(toemail)
    subject = link
    content = Content("text/plain",message_body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
