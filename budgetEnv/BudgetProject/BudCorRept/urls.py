from django.urls import path
from django.conf.urls import url

from . import views
#
urlpatterns = [
    path("reptidx/", views.reptidx, name='reptidx'),
    path("summary/", views.budgetsummary, name='summary'),
    path("costcentre/", views.costcentrereport, name='costcentre'),
    path("asbindex/", views.AppServerBillingList, name='asbindex'),
    path("export_asb/", views.export_asb, name='export_asb'),
    path("appsrvdets/", views.appserverdetails, name='appsrvdets'),
    path("appservercomp/", views.appservercomp, name='appservercomp'),
    path("costcentrecomp/", views.costcentrecomp, name='costcentrecomp'),
    ]