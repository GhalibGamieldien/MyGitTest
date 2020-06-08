from django.urls import path
from django.conf.urls import url

from . import views
from BudCor.views import *
from BudCor.models import LogMessage
#
urlpatterns = [
    path("budgetdistribution/", views.budgetdistribution, name='budgetdistribution'),
    path("counters/", views.counters, name='counters'),
    path("tariffs/", views.tariffs, name='tariffs'),
    path("appsrvcost/", views.appsrvcost, name='appsrvcost'), 
    ]