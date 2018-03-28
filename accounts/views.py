import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from accounts.models import Token
import os
import sendgrid
from sendgrid.helpers.mail import *

def send_login_email(request):
    email = request.POST['email']
    #import ipdb; ipdb.set_trace()
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')

    #sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    sg = sendgrid.SendGridAPIClient(apikey='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')

    from_email = Email("raultr@gmail.com")
    to_email = Email(email)
    subject = "Your login link for Superlists"
    content = Content("text/plain", f"Use this link to log in:\n\n{url}")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    #send_mail('Subject here', 'Here is the message.', 'redgranatum@sendmail.com', ['raultr@gmail.com'], fail_silently=False)
    # send_mail(
    #     'Your login link for Superlists',
    #     f'Use this link to log in:\n\n{url}',
    #     'redgranatum@gmail.com',
    #     [email],
    # )
    return render(request, 'login_email_sent.html')


def login(request):
    import ipdb;ipdb.set_trace()
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import sendgrid
# import os
# from sendgrid.helpers.mail import *

# sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("test@example.com")
# to_email = Email("test@example.com")
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)
