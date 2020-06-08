#
#   BudCor: Budget Distribution and Cost Recovery
#import re
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth.models import User, Group
from django.db import models
#
#   import Application Models and Forms
#
from BudCor.forms import LogMessageForm
from BudCor.models import *
# from BudCor.resource import AppServerBillingResource
#
#   Create your views / code here
#
def is_admin(wmenu):
    if wmenu.groups.filter(name='DCS').exists(): 
            return "home"
    else:
        if wmenu.groups.filter(name='Finance Admin').exists(): 
            return 'home'
        else:
            return 'rept' 

def home(request):
    wuser = request.user
    wmenu = is_admin(wuser)
    if 'home' in wmenu:
        return render(request, "BudCor/home.html")
    else:
        return render(request, "BudCorRept/reptidx.html")

def about(request):
    return render(request, "BudCor/about.html")

def contact(request):
    return render(request, "BudCor/contact.html")
#
#   Display 'Error' Page: Put some App Details
#
def error(request):
    return render(request, "BudCor/error.html")
#
#   Display Form/Page to allow user to log a message
#
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            wmessage = form.save(commit=False)
            wmsg = wmessage.message
            item = add_logmsg(wmsg)
            return redirect("home")
    else:
        return render(request, "BudCor/log_message.html", {"form": form})
#  
#   Callable routing to write a message to DB 
#       
def add_logmsg(wmsg):
    wLogdate = timezone.now()
    wMessage = LogMessage(
        message=wmsg,    
        log_date=wLogdate,
    )
    wMessage.save()
    return wMessage
#
#   log a message code end
#
#   List Messages and Errors Logged code
#
class LoggedMessagesView(ListView):
    """Renders the xxxx page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(LoggedMessagesView, self).get_context_data(**kwargs)
        return context
#
# Hello_there + name
#
def hello_there(request, name):
    return render(
        request,
        'BudCor/hello_there.html',
        {
            'name': name,
            'date': timezone.now()
        }
    )
#
#
#