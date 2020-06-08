from django import forms
#import datetime
from BudCor.models import LogMessage

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class BudgetYearForm(forms.Form):
    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 

#class CostCentreForm(forms.Form):
#    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 
#    costcentre = forms.CharField (help_text='Cost centre to report on') 

#class ApplicationServerForm(forms.Form):
#    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 
#    servername = forms.CharField (help_text='Get this Server details') 

class AppServerBillingListForm(forms.Form):
    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 