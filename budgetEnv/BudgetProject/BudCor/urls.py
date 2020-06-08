from django.urls import path
from django.conf.urls import url

from BudCor import views
from BudCor.views import *
from BudCor.models import LogMessage
#
#   variable for the MessageE List view/code
#
logmsg_list_view = views.LoggedMessagesView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:7],  #  limits the results to the Seven most recent
    context_object_name="message_list",
    template_name="BudCor/list_messages.html",
)

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
    path("list_messages/", logmsg_list_view, name="list_messages"),
    path("error.html/", views.error, name='error'),
    path("hello/<name>", views.hello_there, name="hello_there"),

]