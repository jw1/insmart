from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from alert.models import Alert
from datetime import date

def index(request):
    return HttpResponse("Hello")

# the home page shall show alerts
def home(request):
    today = Alert.objects.filter(created_at__gte=date.today()).order_by('-created_at')
    today_count = len(today)
    older = Alert.objects.filter(created_at__lt=date.today()).order_by('-created_at')[:25]
    older_count = len(older)

    data = {}
    data['today'] = today
    data['today_count'] = today_count
    data['older'] = older
    data['older_count'] = older_count

    return render(request=request, template_name='home.html', context=data)



# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            pass # don't pass an error back to the home page
            # messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request=request, template_name='change_password.html', context={ 'form': form    })