#   Create your views here. 
#   BudCorRept : Reports
#

import re
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
#   from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
#   from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
#   import Application Models and Forms
#
from BudCor.views import add_logmsg
from BudCor.forms import  BudgetYearForm
from BudCorRept.forms import  CostCentreForm, CostCentreCompForm, ApplicationServerForm, AppServerBillingCompForm 
from BudCor.models import *
from BudCor.resource import AppServerBillingResource
#
#
#
def reptidx(request):
    return render(request, "BudCorRept/reptidx.html")
#
#   Budget Summary Report
#   
def budgetsummary(request):
#    
#   Which year we processing for? #   Default is current  
#   
    if request.method == "POST":
        MyBudgetform = BudgetYearForm(request.POST or None)
        if MyBudgetform.is_valid():
            wyear = request.POST.get('budgetyear')
        else:
            wtoday = str(timezone.now())
            wyear = int(wtoday[:4])    
    else:
        wtoday = str(timezone.now())
        wyear = int(wtoday[:4])    
#    
#   get Budget
#
    try:
        wBgt = Budget.objects.get(bgt_year=wyear)
    except ObjectDoesNotExist:
        wmsg = 'Budget Summary Module: No Budget Record for year: ' + wyear 
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
#
#   Restate budget to include interest repayments
#      
    try:
        wfix = FixedValue.objects.get(fix_year=wyear)
    except ObjectDoesNotExist:
        wmsg = 'Budget Summary Module: No Fixed Value Record for year: ' + wyear 
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")

    wbgt_dpre_AIX  = round(wBgt.bgt_dpre_AIX * wfix.fix_interest * wfix.fix_depr_years * 12, 2)
    wbgt_mnt_AIX = round(wBgt.bgt_mnt_AIX, 2)
    wbgt_gti_AIX = round(wBgt.bgt_gti_AIX, 2)
    wbgt_esc_AIX = round(wBgt.bgt_esc_AIX, 2)
    wbgt_inv_dpre_AIX = round(wBgt.bgt_inv_dpre_AIX, 2) 
    wbgt_inv_mnt_AIX = round(wBgt.bgt_inv_mnt_AIX, 2)
    wbgt_inv_gti_AIX = round(wBgt.bgt_inv_gti_AIX, 2)
    wbgt_inv_esc_AIX = round(wBgt.bgt_inv_esc_AIX, 2)

    wbgt_sfm_LINUX = round(wBgt.bgt_sfm_LINUX, 2)
    wbgt_gti_LINUX = round(wBgt.bgt_gti_LINUX, 2)   
    wbgt_esc_LINUX = round(wBgt.bgt_esc_LINUX, 2)
    wbgt_esc_LINUX_Santam = round(wBgt.bgt_esc_LINUX_Santam, 2)
    wbgt_inv_sfm_LINUX = round(wBgt.bgt_inv_sfm_LINUX, 2)
    wbgt_inv_gti_LINUX = round(wBgt.bgt_inv_gti_LINUX, 2)
    wbgt_inv_esc_LINUX = round(wBgt.bgt_inv_esc_LINUX, 2)
    wbgt_inv_esc_LINUX_Santam = round(wBgt.bgt_inv_esc_LINUX_Santam, 2)

    return render(request, "BudCorRept/budgetsummary.html", {"budgetyear" : wyear,
        "wbgt_dpre_AIX" : wbgt_dpre_AIX,
        "wbgt_mnt_AIX" : wbgt_mnt_AIX,
        "wbgt_sfm_LINUX" : wbgt_sfm_LINUX,
        "wbgt_gti_AIX" : wbgt_gti_AIX,
        "wbgt_gti_LINUX" : wbgt_gti_LINUX,
        "wbgt_esc_AIX" : wbgt_esc_AIX,
        "wbgt_esc_LINUX" : wbgt_esc_LINUX,
        "wbgt_esc_LINUX_Santam" : wbgt_esc_LINUX_Santam,
        "wbgt_inv_dpre_AIX" : wbgt_inv_dpre_AIX,
        "wbgt_inv_mnt_AIX" : wbgt_inv_mnt_AIX,
        "wbgt_inv_sfm_LINUX" : wbgt_inv_sfm_LINUX,
        "wbgt_inv_gti_AIX" : wbgt_inv_gti_AIX,
        "wbgt_inv_gti_LINUX" : wbgt_inv_gti_LINUX,
        "wbgt_inv_esc_AIX" : wbgt_inv_esc_AIX,
        "wbgt_inv_esc_LINUX" : wbgt_inv_esc_LINUX,
        "wbgt_inv_esc_LINUX_Santam" : wbgt_inv_esc_LINUX_Santam,
    })
#
#   Billing Report: Servers for Cost Centre
#    
def costcentrereport(request):
    #    
    #   Which year we processing for? #   Default is current  
    #   
    if request.method == "POST":
        MyCostCentreform = CostCentreForm(request.POST or None)
        if MyCostCentreform.is_valid():
            wyear = request.POST.get('budgetyear')
            wbcc = request.POST.get('costcentre')
            wbcc = wbcc.upper() # Make it upper case
        else:
            wbcc = 'BB9498'
            wtoday = str(timezone.now())
            wyear = int(wtoday[:4])    
    else:
        wbcc = 'BB9498'
        wtoday = str(timezone.now())
        wyear = int(wtoday[:4])    

#    
    wasb_tot_gti    = 0
    wasb_tot_sfm    = 0 
    wasb_tot_tin    = 0
    wasb_tot_ha     = 0
    wasb_tot_srv    = 0
#
    wasb_rows = []
    wASBs = AppServerBilling.objects.filter(asb_year=wyear, asb_billingcc=wbcc)
    wASBscnt = wASBs.count()
    if wASBscnt == 0:
        wmsg = 'Cost Centre Report Module: Cost Centre ' + wbcc +  ' has no Application Server financial records for year: ' + wyear 
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
    
    for wASB in wASBs:
        wasb_srv_tin = wASB.asb_cpu + wASB.asb_ram + wASB.asb_hwm 
        wasb_srv_sfm = wASB.asb_sfm 
        wasb_srv_ha =  wASB.asb_ha
        wasb_srv_gti = wASB.asb_gti + wASB.asb_esc + wASB.asb_stc
        wasb_tot_srv = wasb_srv_tin + wasb_srv_sfm +  wasb_srv_ha + wasb_srv_gti 
        
        wasb_cols = []
        wasb_cols.append(wASB.asb_service)
        wasb_cols.append(wASB.asb_name)
        wasb_cols.append('R{0:.2f}'.format(wasb_srv_tin ))
        wasb_cols.append('R{0:.2f}'.format(wasb_srv_sfm))
        wasb_cols.append('R{0:.2f}'.format(wasb_srv_ha))
        wasb_cols.append('R{0:.2f}'.format(wasb_srv_gti))
        wasb_cols.append('R{0:.2f}'.format(wasb_tot_srv))
           
        wasb_rows.append(wasb_cols)

        wasb_tot_tin = wasb_tot_tin + wasb_srv_tin
        wasb_tot_sfm = wasb_tot_sfm + wasb_srv_sfm
        wasb_tot_ha = wasb_tot_ha + wasb_srv_ha
        wasb_tot_gti = wasb_tot_gti + wasb_srv_gti
                    
    wasb_tot = wasb_tot_tin + wasb_tot_sfm + wasb_tot_ha + wasb_tot_gti
#
    return render(request, "BudCorRept/costcentrereport.html", {"budgetyear" : wyear,
        "costcentre"   : wbcc,
        "wasb_tot_tin" : wasb_tot_tin,
        "wasb_tot_sfm" : wasb_tot_sfm,
        "wasb_tot_ha"  : wasb_tot_ha,
        "wasb_tot_srv" : wasb_tot_srv,
        "wasb_tot_gti" : wasb_tot_gti,
        "wasb_tot"     : wasb_tot,
        "wASBscnt"     : wASBscnt,
        "wasb_rows"    : wasb_rows,
         })
#
#   Billing Report: Comparison Repiort for Cost Centre
#    
def costcentrecomp(request):
    #    
    #   Which year we processing for? #   Default is current  
    #   
    if request.method == "POST":
        MyCostCentreCompForm = CostCentreCompForm(request.POST or None)
        if MyCostCentreCompForm.is_valid():
            wyear1 = request.POST.get('budgetyear1')
            wyear2 = request.POST.get('budgetyear2')
            wbcc = request.POST.get('costcentre')
            wbcc = wbcc.upper() # Make it upper case
        else:
            wbcc = 'BB9498'
            wtoday = str(timezone.now())
            wyear1 = int(wtoday[:4])
            wyear2 = int(wtoday[:4]) + 1     
    else:
        wbcc = 'BB9498'
        wtoday = str(timezone.now())
        wyear1 = int(wtoday[:4])    
        wyear2 = int(wtoday[:4]) + 1  
#
#   get Year1 Dets for cost Centre
#     
    wasb1_tot_srv = 0
    wasb2_tot_srv = 0
    wasb1_tot = 0
    wasb2_tot = 0
    wasb_rows = []
    wASBs = AppServerBilling.objects.filter(asb_year=wyear1, asb_billingcc=wbcc)
    wASBscnt = wASBs.count()
    if wASBscnt == 0:
        wmsg = 'Cost Centre Report Module: Cost Centre ' + wbcc +  ' has no Application Server financial records for year: ' + wyear1 
        item = add_logmsg(wmsg)
    else:

        for wASB in wASBs:
            wasb1_tot_srv = wASB.asb_cpu + wASB.asb_ram + wASB.asb_hwm + wASB.asb_sfm + wASB.asb_ha + wASB.asb_gti + wASB.asb_esc + wASB.asb_stc
            wasb_cols = []
            wasb_cols.append(wASB.asb_service)
            wasb_cols.append(wASB.asb_name)
            wasb_cols.append('R{0:.2f}'.format(wasb1_tot_srv))
                       
            wASB2 = AppServerBilling.objects.get(asb_name=wASB.asb_name,asb_service=wASB.asb_service, asb_year=wyear2, asb_billingcc=wbcc)
            wasb2_tot_srv = wASB2.asb_cpu + wASB2.asb_ram + wASB2.asb_hwm + wASB2.asb_sfm + wASB2.asb_ha + wASB2.asb_gti + wASB2.asb_esc + wASB2.asb_stc
            wasb_cols.append('R{0:.2f}'.format(wasb2_tot_srv))

            if 'LINUX' in wASB.asb_service:
                try:
                    wSRV = LINUXServer.objects.get(srv_Name=wASB2.asb_name)
                except ObjectDoesNotExist:
                    wmsg = 'Cost Centre Report Module: LINUX Application Server does not exist: ' + wname  
                    item = add_logmsg(wmsg)
                    return render(request, "BudCor/error.html") 
            else:
                if 'AIX' in wASB.asb_service:    
                    try:
                        wSRV = AIXServer.objects.get(srv_Name=wASB2.asb_name) 
                    except ObjectDoesNotExist:
                        wmsg = 'Cost Centre Report Module: AIX Application Server does not exist: ' + wname  
                        item = add_logmsg(wmsg)
                        return render(request, "BudCor/error.html") 

            wasb_cols.append(wSRV.srv_application)
            wasb_cols.append(wSRV.srv_client)
            wasb_rows.append(wasb_cols)
            wasb1_tot = wasb1_tot + wasb1_tot_srv
            wasb2_tot = wasb2_tot + wasb2_tot_srv  
    
    return render(request, "BudCorRept/costcentrecomp.html", {"budgetyear1" : wyear1,
        "budgetyear2" : wyear2,
        "costcentre"  : wbcc,
        "wasb1_tot"   : wasb1_tot,
        "wasb2_tot"   : wasb2_tot,
        "wASBscnt"   : wASBscnt,
        "wasb_rows"  : wasb_rows,
         })
#
#   Billing Report: Server Details
#      
def appserverdetails(request):
#    
#   Which year we processing for? #   Default is current  
#   
    if request.method == "POST":
        MyApplicationServerform = ApplicationServerForm(request.POST or None)
        if MyApplicationServerform.is_valid():
            wyear = request.POST.get('budgetyear')
            wname = request.POST.get('servername')
        else:
            wmsg = 'Application Server Details Module: Invalid Data Form ' 
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
    else:
        wmsg = 'Application Server Details Module: Invalid Input Data'  
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
#
#   Get Cost details
#
    try:
        wASB = AppServerBilling.objects.get(asb_year=wyear,  asb_name=wname)
        wasb_srv_tin = wASB.asb_cpu + wASB.asb_ram + wASB.asb_hwm
        wasb_srv_sfm = wASB.asb_sfm
        wasb_srv_ha =  wASB.asb_ha
        wasb_srv_gti = wASB.asb_gti + wASB.asb_esc + wASB.asb_stc
        wasb_tot_srv = wasb_srv_tin + wasb_srv_sfm +  wasb_srv_ha + wasb_srv_gti
        
        if 'LINUX' in wASB.asb_service:
            try:
                wSRV = LINUXServer.objects.get(srv_Name=wname)
            except ObjectDoesNotExist:
                wmsg = 'Application Server Details Module: LINUX Application Server does not exist: ' + wname  
                item = add_logmsg(wmsg)
                return render(request, "BudCor/error.html") 
        else:
            if 'AIX' in wASB.asb_service:    
                try:
                    wSRV = AIXServer.objects.get(srv_Name=wname) 
                except ObjectDoesNotExist:
                    wmsg = 'Application Server Details Module: AIX Application Server does not exist: ' + wname  
                    item = add_logmsg(wmsg)
                    return render(request, "BudCor/error.html") 

        wsrv_appowner =  wSRV.srv_appowner
        wsrv_client =  wSRV.srv_client
        wsrv_billingcc =  wSRV.srv_billingcc
        wsrv_OS =  wSRV.srv_OS
        wsrv_primarytechowner =  wSRV.srv_primarytechowner
        wsrv_competency =  wSRV.srv_competency
        wsrv_application = wSRV.srv_application
        wsrv_serverdescription = wSRV.srv_serverdescription
        wsrv_phs_name = wSRV.srv_phs_name

    except ObjectDoesNotExist:
        wmsg = 'Application Server Details Module: Application Server has no cost recovery information: ' + wname  
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
#
    return render(request, "BudCorRept/applicationserverreport.html", {"budgetyear" : wyear,
        "wname" : wname,
        "wasb_srv_tin" : wasb_srv_tin,
        "wasb_srv_sfm" : wasb_srv_sfm,
        "wasb_srv_ha" : wasb_srv_ha,
        "wasb_srv_gti" : wasb_srv_gti,
        "wasb_tot_srv" : wasb_tot_srv,
        "wsrv_client" : wsrv_client,
        "wsrv_appowner" : wsrv_appowner,
        "wsrv_billingcc" : wsrv_billingcc,
        "wsrv_OS" : wsrv_OS,
        "wsrv_primarytechowner" : wsrv_primarytechowner,
        "wsrv_competency" : wsrv_competency,
        "wsrv_application" : wsrv_application,
        "wsrv_serverdescription" : wsrv_serverdescription,
        "wsrv_phs_name" : wsrv_phs_name,
 
         })
def appservercomp(request):
#    
#   Which year we processing for? #   Default is current  
#   
    if request.method == "POST":
        MyAppServerBillingCompForm = AppServerBillingCompForm(request.POST or None)
        if MyAppServerBillingCompForm.is_valid():
            wyear1 = request.POST.get('budgetyear1')
            wyear2 = request.POST.get('budgetyear2')
            wname = request.POST.get('servername')
        else:
            wmsg = 'Application Server comp Module: Invalid Data Form ' 
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
    else:
        wmsg = 'Application Server comp Module: Invalid Input Data'  
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
#
#   Get Cost details - Year 1
#
    try:
        wASB = AppServerBilling.objects.get(asb_year=wyear1,  asb_name=wname)
        wasb_srv_tin1 = wASB.asb_cpu + wASB.asb_ram + wASB.asb_hwm
        wasb_srv_sfm1 = wASB.asb_sfm
        wasb_srv_ha1 =  wASB.asb_ha
        wasb_srv_gti1 = wASB.asb_gti + wASB.asb_esc + wASB.asb_stc
        wasb_tot_srv1 = wasb_srv_tin1 + wasb_srv_sfm1 +  wasb_srv_ha1 + wasb_srv_gti1
    except ObjectDoesNotExist:
        wasb_srv_tin1 = 0
        wasb_srv_sfm1 = 0
        wasb_srv_ha1 =  0
        wasb_srv_gti1 = 0
        wasb_tot_srv1 = 0
#
#   Get Cost details - Year 2
#   
    try:
        wASB = AppServerBilling.objects.get(asb_year=wyear2,  asb_name=wname)
        wasb_srv_tin2 = wASB.asb_cpu + wASB.asb_ram + wASB.asb_hwm
        wasb_srv_sfm2 = wASB.asb_sfm
        wasb_srv_ha2 =  wASB.asb_ha
        wasb_srv_gti2 = wASB.asb_gti + wASB.asb_esc + wASB.asb_stc
        wasb_tot_srv2 = wasb_srv_tin2 + wasb_srv_sfm2 +  wasb_srv_ha2 + wasb_srv_gti2
    except ObjectDoesNotExist:
        wasb_srv_tin2 = 0
        wasb_srv_sfm2 = 0
        wasb_srv_ha2 =  0
        wasb_srv_gti2 = 0
        wasb_tot_srv2 = 0
#
#   Get Annotation details
#   
    wsrv_appowner =  ' '
    wsrv_client =  ' '
    wsrv_billingcc =  ' '
    wsrv_OS = ' '
    wsrv_primarytechowner =  ' '
    wsrv_competency =  ' '
    wsrv_application = ' '
    wsrv_serverdescription = ' '
    wsrv_phs_name = ' '

    if 'LINUX' in wASB.asb_service:
        try:
            wSRV = LINUXServer.objects.get(srv_Name=wname)
        except ObjectDoesNotExist:
            wmsg = 'Application Server comp Module: Costs but no Server Details for LINUX: ' + wname  
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html") 
    else:
        if 'AIX' in wASB.asb_service:    
            try:
                wSRV = AIXServer.objects.get(srv_Name=wname) 
            except ObjectDoesNotExist:
                wmsg = 'Application Server comp Module: Costs but no Server Details for AIX: ' + wname  
                item = add_logmsg(wmsg)
                return render(request, "BudCor/error.html") 

    wsrv_appowner =  wSRV.srv_appowner
    wsrv_client =  wSRV.srv_client
    wsrv_billingcc =  wSRV.srv_billingcc
    wsrv_OS =  wSRV.srv_OS
    wsrv_primarytechowner =  wSRV.srv_primarytechowner
    wsrv_competency =  wSRV.srv_competency
    wsrv_application = wSRV.srv_application
    wsrv_serverdescription = wSRV.srv_serverdescription
    wsrv_phs_name = wSRV.srv_phs_name
#
    return render(request, "BudCorRept/applicationservercomp.html", {"budgetyear1" : wyear1,
        "budgetyear2" : wyear2,
        "wname" : wname,
        "wasb_srv_tin1" : wasb_srv_tin1,
        "wasb_srv_sfm1" : wasb_srv_sfm1,
        "wasb_srv_ha1" : wasb_srv_ha1,
        "wasb_srv_gti1" : wasb_srv_gti1,
        "wasb_tot_srv1" : wasb_tot_srv1,
        "wasb_srv_tin2" : wasb_srv_tin2,
        "wasb_srv_sfm2" : wasb_srv_sfm2,
        "wasb_srv_ha2" : wasb_srv_ha2,
        "wasb_srv_gti2" : wasb_srv_gti2,
        "wasb_tot_srv2" : wasb_tot_srv2,
        "wsrv_client" : wsrv_client,
        "wsrv_appowner" : wsrv_appowner,
        "wsrv_billingcc" : wsrv_billingcc,
        "wsrv_OS" : wsrv_OS,
        "wsrv_primarytechowner" : wsrv_primarytechowner,
        "wsrv_competency" : wsrv_competency,
        "wsrv_application" : wsrv_application,
        "wsrv_serverdescription" : wsrv_serverdescription,
        "wsrv_phs_name" : wsrv_phs_name,
         })
#
#   List View of Application server with costs
#
def AppServerBillingList(request):
#    
#   Which year we processing for? #   Default is current  
#   
#    if request.method == "POST":
#        MyAppServerBillingListForm = AppServerBillingListForm(request.POST or None)
#        if MyAppServerBillingListForm.is_valid():
#            wyear = request.POST.get('budgetyear')
#        else:
#            wmsg = 'Application Server Billing list Module: Invalid Data Form ' 
#            item = add_logmsg(wmsg)
#            return render(request, "BudCor/error.html")
#    else:
#        pass
#        wmsg = 'Application Server Billing list Module: Invalid Input Data'  
#        item = add_logmsg(wmsg)
#        return render(request, "BudCor/error.html")

    AppServerBilling_list = AppServerBilling.objects.all().order_by('asb_service', 'asb_name')
    page = request.GET.get('page', 1)
    paginator = Paginator(AppServerBilling_list, 15)
    try:
        AppServerBillings = paginator.page(page)
    except PageNotAnInteger:
        AppServerBillingss = paginator.page(1)
    except EmptyPage:
        AppServerBillings = paginator.page(paginator.num_pages)
    return render(request, 'BudCorRept/asb_list.html', { 'AppServerBillings': AppServerBillings })
#
#   Export
#
def export_asb(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        AppServerBilling_resource = AppServerBillingResource()
        dataset = AppServerBilling_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response
        elif file_format == 'XLSX':
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            return response   
   
    return render(request, 'BudCorRept/asb_export.html')