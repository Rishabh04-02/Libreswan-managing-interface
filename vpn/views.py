# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import GenerateCertificate, UserProfile
from .tokens import account_activation_token
from django.http import HttpResponse
from django.views import View
from .forms import SignUpForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import GenerateCertificate, UserProfile
from django.views.static import serve
import os

# Create your views here.


def index(request):
    return render(request, "vpn/index.html", {})


def login(request):
    username = str(request.POST['username'])
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        userid = User.objects.get(username=username)
        useractive = userid.is_active
        userid = userid.id
        email_verify = UserProfile.objects.get(username_id=userid)
        email_verify = email_verify.email_verified
        if userid and email_verify is True:
            CertPassword = GenerateCertificate.objects.get(username_id=userid)
            CertPassword = CertPassword.cert_password
            filepath = '/certs/' + username + '.p12' 
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            certlocation = BASE_DIR + os.path.join(BASE_DIR, filepath)
            
            return render(request, 'vpn/home.html', {
                'CertPassword': CertPassword,
                'username': username,
                'certificate': filepath,
                'certlocation': certlocation})
        else:
            return HttpResponse(
                '<center>Login Failed, have you activated your account?</center>')
    else:
        return HttpResponse(
            '<center>Login Failed<br><a href="/">Login again?</a></center>')


def logout(request):
    return HttpResponse(
            '<center>Logged out<br><a href="/">Login again?</a></center>')


def activate_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        user = request.POST['username']
        userid = User.objects.get(username=user).id
        current_site = get_current_site(request)
        subject = 'Activate Your Libreswan Account'
        message = render_to_string(
            'vpn/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userid)).decode(),
                'token': account_activation_token.make_token(user),
            })
        emailto = User.objects.get(username=user).email
        send_mail("Hello " + user + " - " + subject, message,
                  "noreply@libreswan.org", [emailto])

        return HttpResponse(
            '<center>Account activation link sent on your registered email id - '
            + emailto + "</center>")
    else:
        form = SignUpForm()
    return render(request, 'vpn/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # Creating/Updating entry to profile.email_verified, as to fetch and display it to the admin. Updating it as when user visits the same link more than once then it gives an error, so as to remove that error just added Update option along with Insert values.
        UserProfile.objects.filter(username_id=uid).update(email_verified=True)
        return HttpResponse(
            '<center>Thank you for your email confirmation. Now you can login your account.</center>'
        )
    else:
        return HttpResponse('<center>Invalid Token/Token has expired.</center>')
