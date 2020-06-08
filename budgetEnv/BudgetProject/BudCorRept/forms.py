from django import forms

class CostCentreForm(forms.Form):
    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 
    costcentre = forms.CharField (help_text='Cost centre to report on') 

class ApplicationServerForm(forms.Form):
    budgetyear = forms.IntegerField (help_text='Select budget values associated with this year') 
    servername = forms.CharField (help_text='Get this Server details') 

class CostCentreCompForm(forms.Form):
    budgetyear1 = forms.IntegerField (help_text='Select Cost Centre costs associated with year 1') 
    budgetyear2 = forms.IntegerField (help_text='Select Cost Centre costs associated with year 2') 
    costcentre = forms.CharField (help_text='Cost centre to report on') 

class AppServerBillingCompForm(forms.Form):
    budgetyear1 = forms.IntegerField (help_text='Select Server costs associated with year 1') 
    budgetyear2 = forms.IntegerField (help_text='Select Server costs associated with year 2')
    servername = forms.CharField (help_text='Get this Server details') 