# Create your views here.
#
#   BudCorMidrange: Midrange: Budget Distribution and Cost Recovery
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
#   from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
#   import Application Models and Forms
#
from BudCor.forms import BudgetYearForm
from BudCor.models import *
from BudCor.views import add_logmsg
#
#
def counters(request):
#
#   AIX Service 
# 
#   Count Shared Technology Servers
# 
    BB9498 = AIXServer.objects.filter(srv_billingcc="BB9498")
    wcnt_BB9498 = BB9498.count()   
#
# Allocated CPU and RAM
#
    wcnt_T0_cpu = 0
    wcnt_T0_ram = 0
    wcnt_T1_cpu = 0
    wcnt_T1_ram = 0
    wcnt_T1_AIX = 0
    wcnt_T2_cpu = 0
    wcnt_T2_ram = 0
    wcnt_T2_AIX = 0
    wcnt_AIX = 0
    wAIXsrvs = AIXServer.objects.all()
    for wAIXsrv in wAIXsrvs:
        w_srv_Name = wAIXsrv.srv_Name
        try:
            wphs = PowerHardwareServer.objects.get(phs_serial_num=wAIXsrv.srv_phs_serial_num)
            wpht = PowerHardwareTier.objects.get(pht_num=wphs.phs_tier)
            if wpht.pht_num == 0:
                wcnt_T0_cpu = wcnt_T0_cpu + wAIXsrv.srv_cpu
                wcnt_T0_ram = wcnt_T0_ram + wAIXsrv.srv_ram 
            elif wpht.pht_num == 1:
                wcnt_T1_cpu = wcnt_T1_cpu + wAIXsrv.srv_cpu 
                wcnt_T1_ram = wcnt_T1_ram + wAIXsrv.srv_ram
                wcnt_T1_AIX = wcnt_T1_AIX + 1
            elif wpht.pht_num == 2:
                wcnt_T2_cpu = wcnt_T2_cpu + wAIXsrv.srv_cpu
                wcnt_T2_ram = wcnt_T2_ram + wAIXsrv.srv_ram 
                wcnt_T2_AIX = wcnt_T2_AIX + 1 
        
            wAIXsrv.srv_pht_tier = wpht.pht_num
            wAIXsrv.srv_phs_name = wphs.phs_name
        except ObjectDoesNotExist:
            wAIXsrv.srv_pht_tier = 0
        wAIXsrv.save()      
                     
#
#   AIX App Servers
#
    wcnt_AIX = wcnt_T1_AIX + wcnt_T2_AIX    
#    
#   HA: Logical Processors Total
#
    wcnt_PHA_Procs = 0
    wphas = PowerHAServer.objects.all()
    for wpha in wphas:
        wcnt_PHA_Procs = wcnt_PHA_Procs + wpha.pha_num_logical_procs
#------------------------------------------------------------------------------------------------------------
#
#   LINUX Service
#
#   LINUX App Servers
#    
    wcnt_LINUX = LINUXServer.objects.count()
    #
    BB8263 = LINUXServer.objects.filter(srv_billingcc='BB8263')
    wcnt_BB8263 = BB8263.count()      
    #   LINUX BCX support
    wBCXLINUX = LINUXServer.objects.filter(srv_competency='BCX OSS (Linux)')
    wcnt_BCX_LINUX = wBCXLINUX.count()
    
    wBCX_Default = wBCXLINUX.exclude(srv_client='SKY')
    wBCX_Default = wBCX_Default.exclude(srv_client='Santam')
    wcnt_LINUX_Default = wBCX_Default.count()  

    #   BCX LINUX Santam Servers
    wLINUXSantam = LINUXServer.objects.filter(srv_client='Santam', srv_competency='BCX OSS (Linux)'
    )
    wcnt_LINUX_Santam = wLINUXSantam.count()      
        
    #   BCX LINUX SKY  
    wLINUXSKY = LINUXServer.objects.filter(srv_client='SKY', srv_competency='BCX OSS (Linux)'
    )
    wcnt_LINUX_SKY = wLINUXSKY.count()      
    
    #  Santam REd Hat
    wRed_Hat_Santam = LINUXServer.objects.filter(srv_client='Santam', 
    srv_OS__contains='Red Hat',
    )
    wcnt_RedHat_Santam = wRed_Hat_Santam.count()      

    #   SKY Red Hat 
    wRed_Hat_SKY = LINUXServer.objects.filter(srv_client="SKY", 
    srv_OS__contains='Red Hat',
    )
    wcnt_RedHat_SKY = wRed_Hat_SKY.count()      
    
    #   Default: Non-Santam non-SKY
    wRed_Hat_Default = LINUXServer.objects.filter(srv_OS__contains='Red Hat')
    wRed_Hat_Default = wRed_Hat_Default.exclude(srv_client='SKY').exclude(srv_client='Santam')
    wcnt_RedHat_Default = wRed_Hat_Default.count()
   
    #   SUSE Servers
    wcnt_SUSE_sockets = 0
    wsuses = SUSEServer.objects.all()
    for wsuse in wsuses:
        wcnt_SUSE_sockets = wcnt_SUSE_sockets + wsuse.SUSE_num_sockets
    wcnt_SUSE = SUSEServer.objects.count()
    #
    #Loop thru 10 at a time
    #Entry.objects.all()[:10]
    #Entry.objects.all()[10:10]
    #       
    #   Get  the Counter Record and Update or if none then Save for 1st time
    #
    try:
        wCounter = Counters.objects.get(id=1)
        wCounter.cnt_AIX_app_servers=wcnt_AIX
        wCounter.cnt_T1_AIX_app_servers=wcnt_T1_AIX
        wCounter.cnt_T2_AIX_app_servers=wcnt_T2_AIX
        wCounter.cnt_LINUX_app_servers=wcnt_LINUX
        wCounter.cnt_AIX_svc_cc=wcnt_BB9498
        wCounter.cnt_LINUX_svc_cc=wcnt_BB8263
        wCounter.cnt_T0_cpu_appsrv=wcnt_T0_cpu
        wCounter.cnt_T1_cpu_appsrv=wcnt_T1_cpu
        wCounter.cnt_T2_cpu_appsrv=wcnt_T2_cpu
        wCounter.cnt_T0_ram_appsrv=wcnt_T0_ram
        wCounter.cnt_T1_ram_appsrv=wcnt_T1_ram
        wCounter.cnt_T2_ram_appsrv=wcnt_T2_ram
        wCounter.cnt_app_HA_Processors=wcnt_PHA_Procs
        wCounter.cnt_LINUX_competency=wcnt_BCX_LINUX
        wCounter.cnt_LINUX_Default=wcnt_LINUX_Default
        wCounter.cnt_LINUX_Santam=wcnt_LINUX_Santam
        wCounter.cnt_LINUX_SKY=wcnt_LINUX_SKY
        wCounter.cnt_Red_Hat_Default=wcnt_RedHat_Default
        wCounter.cnt_Red_Hat_Santam=wcnt_RedHat_Santam
        wCounter.cnt_Red_Hat_SKY=wcnt_RedHat_SKY
        wCounter.cnt_SUSE = wcnt_SUSE_sockets
    except ObjectDoesNotExist:
        wCounter = Counters(
        cnt_AIX_app_servers=wcnt_AIX,
        cnt_T1_AIX_app_servers=wcnt_T1_AIX,
        cnt_T2_AIX_app_servers=wcnt_T2_AIX,
        cnt_LINUX_app_servers=wcnt_LINUX,
        cnt_AIX_svc_cc=wcnt_BB9498,
        cnt_LINUX_svc_cc=wcnt_BB8263,
        cnt_T0_cpu_appsrv=wcnt_T0_cpu,
        cnt_T1_cpu_appsrv=wcnt_T1_cpu,
        cnt_T2_cpu_appsrv=wcnt_T2_cpu,
        cnt_T0_ram_appsrv=wcnt_T0_ram,
        cnt_T1_ram_appsrv=wcnt_T1_ram,
        cnt_T2_ram_appsrv=wcnt_T2_ram,
        cnt_app_HA_Processors=wcnt_PHA_Procs,
        cnt_LINUX_competency=wcnt_BCX_LINUX,
        cnt_LINUX_Default=wcnt_LINUX_Default,  
        cnt_LINUX_Santam=wcnt_LINUX_Santam, 
        cnt_LINUX_SKY=wcnt_LINUX_SKY,
        cnt_Red_Hat_Default=wcnt_RedHat_Default, 
        cnt_Red_Hat_Santam=wcnt_RedHat_Santam, 
        cnt_Red_Hat_SKY=wcnt_RedHat_SKY,
        cnt_SUSE=wcnt_SUSE_sockets,
        )
    
    wCounter.save()
   
    wcnt_AIX = round(wcnt_AIX, 2)
    wcnt_BB9498 = round(wcnt_BB9498, 2)
    wcnt_T1_AIX = round(wcnt_T1_AIX, 2)  
    wcnt_T2_AIX = round(wcnt_T2_AIX, 2)
    wcnt_T1_cpu = round(wcnt_T1_cpu, 2)  
    wcnt_T2_cpu = round(wcnt_T2_cpu, 2)   
    wcnt_T1_ram = round(wcnt_T1_ram, 2)  
    wcnt_T2_ram = round(wcnt_T2_ram, 2) 
    wcnt_PHA_Procs = round(wcnt_PHA_Procs, 2)              
    wcnt_LINUX = round(wcnt_LINUX, 2)
    wcnt_BB8263 = round(wcnt_BB8263, 2)  
    wcnt_BCX_LINUX = round(wcnt_BCX_LINUX, 2) 
    wcnt_LINUX_Default = round(wcnt_LINUX_Default, 2)   
    wcnt_RedHat_Default = round(wcnt_RedHat_Default, 2) 
    wcnt_SUSE = round(wcnt_SUSE, 2)    
    wcnt_LINUX_Santam = round(wcnt_LINUX_Santam, 2)    
    wcnt_RedHat_Santam = round(wcnt_RedHat_Santam, 2)   
    wcnt_LINUX_SKY = round(wcnt_LINUX_SKY, 2) 
    wcnt_RedHat_SKY = round(wcnt_RedHat_SKY, 2)  

    return render(request, "BudCorMidrange/counters.html", {"wcnt_AIX" : wcnt_AIX, 
        "wcnt_BB9498" :  wcnt_BB9498,
        "wcnt_T1_AIX" : wcnt_T1_AIX,  
        "wcnt_T2_AIX" : wcnt_T2_AIX,
        "wcnt_T1_cpu" : wcnt_T1_cpu,  
        "wcnt_T2_cpu" : wcnt_T2_cpu,   
        "wcnt_T1_ram" : wcnt_T1_ram,  
        "wcnt_T2_ram" : wcnt_T2_ram, 
        "wcnt_PHA_Procs" : wcnt_PHA_Procs,              
        "wcnt_LINUX" : wcnt_LINUX,
        "wcnt_BB8263" : wcnt_BB8263,  
        "wcnt_BCX_LINUX" : wcnt_BCX_LINUX, 
        "wcnt_LINUX_Default" : wcnt_LINUX_Default,   
        "wcnt_RedHat_Default" : wcnt_RedHat_Default,  
        "wcnt_SUSE" : wcnt_SUSE_sockets,    
        "wcnt_LINUX_Santam" : wcnt_LINUX_Santam,    
        "wcnt_RedHat_Santam" : wcnt_RedHat_Santam,   
        "wcnt_LINUX_SKY" : wcnt_LINUX_SKY, 
        "wcnt_RedHat_SKY" : wcnt_RedHat_SKY, 
        } )
#
#   Allocated budgets appropriately 
#
def budgetdistribution(request):
#
#   Which year we processing for?
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
#   Default is current    
#    
#   Get the Budget Values 
#
    try:
        wfix = FixedValue.objects.get(fix_year=wyear)
        pass
    except ObjectDoesNotExist:
            wmsg = 'Budget Distribution Module: No Fixed Value data for Year:' + wyear
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
    try:
        wBgt = Budget.objects.get(bgt_year=wyear)
        pass
    except ObjectDoesNotExist:
            wmsg = 'Budget Distribution Module: No Budget data for Year:' + wyear
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
    try:
        wcnt = Counters.objects.get(id=1)
    except ObjectDoesNotExist:
            wmsg = 'Budget Distribution Module: No Counters Record'
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
      
#
#   Total the sub-services costs into Budget Table
#
    wBgt.bgt_gti_AIX = 0
    wBgt.bgt_gti_LINUX = 0
    wAIXRental = 0
    wsubsvc =  Service.objects.filter(svc_year=wyear)
    wsubsvcDefaults =  wsubsvc.filter(svc_client='Default')
    wsubsvcSantams =  wsubsvc.filter(svc_client='Santam')
    wsubsvcSKYs =  wsubsvc.filter(svc_client='SKY')
    
    for wsubsvcDefault in wsubsvcDefaults:

        if 'AIX' in wsubsvcDefault.svc_name:
            if 'GTI' in wsubsvcDefault.svc_provider:
                if 'AIX Host Rental' in wsubsvcDefault.svc_name:
                    wAIXRental = wsubsvcDefault.svc_platform_cost
                else:
                    wBgt.bgt_gti_AIX = wBgt.bgt_gti_AIX + wsubsvcDefault.svc_platform_cost
            elif 'BCX' in wsubsvcDefault.svc_provider:
                wBgt.bgt_esc_AIX = wsubsvcDefault.svc_platform_cost + wsubsvcDefault.svc_acnt_mgmt_cost + wsubsvcDefault.svc_cons_cost
        elif 'LINUX' in wsubsvcDefault.svc_name: 
            if 'GTI' in wsubsvcDefault.svc_provider:
                wBgt.bgt_gti_LINUX = wBgt.bgt_gti_LINUX + wsubsvcDefault.svc_platform_cost
            elif 'BCX' in wsubsvcDefault.svc_provider:
                wBgt.bgt_esc_LINUX = wsubsvcDefault.svc_platform_cost + wsubsvcDefault.svc_acnt_mgmt_cost + wsubsvcDefault.svc_cons_cost

    for wsubsvcSantam in wsubsvcSantams:
#   LINUX only External Service for Santam no GTI
#
        if 'AIX' in wsubsvcSantam.svc_name:
            if 'GTI' in wsubsvcSantam.svc_provider:
                wBgt.bgt_gti_AIX = wBgt.bgt_gti_AIX + wsubsvcSantam.svc_platform_cost
            elif 'BCX' in wsubsvcSantam.svc_provider:
                wBgt.bgt_esc_AIX = wsubsvcSantam.svc_platform_cost + wsubsvcSantam.svc_acnt_mgmt_cost + wsubsvcSantam.svc_cons_cost
        if 'LINUX' in wsubsvcSantam.svc_name: 
            if 'GTI' in wsubsvcSantam.svc_provider:
                wBgt.bgt_gti_LINUX = wBgt.bgt_gti_LINUX + wsubsvcSantam.svc_platform_cost
            if 'BCX' in wsubsvcSantam.svc_provider:
                wBgt.bgt_esc_LINUX_Santam = wsubsvcSantam.svc_platform_cost + wsubsvcSantam.svc_acnt_mgmt_cost + wsubsvcSantam.svc_cons_cost

#
#   SKY not catered for yet
#
#    for wsubsvcSKY in wsubsvcSKYs:
#
#        if 'AIX' in wsubsvcSKY.svc_name:
#            if 'GTI' in wsubsvcSKY.svc_provider:
#                wBgt.bgt_gti_AIX = wBgt.bgt_gti_AIX + wsubsvcSKY.svc_platform_cost
#            elif 'BCX' in wsubsvcSKY.svc_provider:
#                wBgt.bgt_esc_AIX = wsubsvcSKY.svc_platform_cost + wsubsvcSKY.svc_acnt_mgmt_cost + wsubsvcSKY.svc_cons_cost
#        elif 'LINUX' in wsubsvcSKY.svc_name: 
#            if 'GTI' in wsubsvcSKY.svc_provider:
#                wBgt.bgt_gti_LINUX = wBgt.bgt_gti_LINUX + wsubsvcSKY.svc_platform_cost
#            elif 'BCX' in wsubsvcSKY.svc_provider:
#                wBgt.bgt_esc_LINUX = wsubsvcSKY.svc_platform_cost + wsubsvcSKY.svc_acnt_mgmt_cost + wsubsvcSKY.svc_cons_cost
#   
#
#   restate GTI Budget to get equal share
#
    wcntAppServers = (wcnt.cnt_AIX_app_servers + wcnt.cnt_LINUX_Default)

    if wcntAppServers != 0:
        w_gti_AIX = (wcnt.cnt_AIX_app_servers / wcntAppServers) * (wBgt.bgt_gti_AIX + wBgt.bgt_gti_LINUX)
        w_gti_LINUX = (wcnt.cnt_LINUX_Default / wcntAppServers) * (wBgt.bgt_gti_AIX + wBgt.bgt_gti_LINUX)
    
    wBgt.bgt_gti_AIX = w_gti_AIX + wAIXRental
    wBgt.bgt_gti_LINUX = w_gti_LINUX

    wBgt.bgt_inv_dpre_AIX = 0
    wBgt.bgt_inv_mnt_AIX = 0
    wBgt.bgt_inv_gti_AIX = 0
    wBgt.bgt_inv_esc_AIX = 0
    wBgt.bgt_inv_esc_LINUX = 0    
    wBgt.bgt_inv_gti_LINUX = 0 
    wBgt.bgt_inv_sfm_LINUX = 0
    wBgt.bgt_inv_esc_LINUX_Santam = 0
    
    wBgt.save()

    w_gti_AIX = round(wBgt.bgt_gti_AIX, 2)
    w_gti_LINUX = round(wBgt.bgt_gti_LINUX, 2)
    w_esc_AIX = round(wBgt.bgt_esc_AIX, 2)
    w_esc_LINUX = round(wBgt.bgt_esc_LINUX, 2)
    w_esc_LINUX_Santam = round(wBgt.bgt_esc_LINUX_Santam, 2)
#
#   Recon Power Server Info into Power Server Tiers Table
#   as well as Hardware Maint 
#   
    wphts = PowerHardwareTier.objects.all()
    for wpht in wphts:
        wtiernum = wpht.pht_num
        wphss = PowerHardwareServer.objects.filter(phs_tier=wtiernum)

        wpht_cpu_tot = 0
        wpht_ram_tot = 0
        wpht_cost_tot = 0
        wpht_num_servers = 0 

        for wphs in wphss:
            wpht_cpu_tot = wpht_cpu_tot + wphs.phs_cpu
            wpht_ram_tot = wpht_ram_tot + wphs.phs_ram
            wpht_cost_tot = wpht_cost_tot + wphs.phs_price_bought
            wpht_num_servers = wpht_num_servers + 1
        
        wpht.pht_num_servers = wpht_num_servers
        wpht.pht_cpu = wpht_cpu_tot
        wpht.pht_ram = wpht_ram_tot
        wpht.pht_price = wpht_cost_tot
        wpht.pht_cpu_alloc = 0
        wpht.pht_ram_alloc = 0

        wpht.pht_hwm = wpht.pht_mnt_budget_shr * wfix.fix_AIX_hwm_shr * wBgt.bgt_mnt_AIX
        wpht.pht_sfm = wpht.pht_mnt_budget_shr * wfix.fix_AIX_sfm_shr * wBgt.bgt_mnt_AIX

        wpht.pht_budget = wpht.pht_dpre_budget_shr * wBgt.bgt_dpre_AIX
        wpht.pht_recovery_need = wpht.pht_budget * wfix.fix_interest * wfix.fix_depr_years
        wpht.pht_cpu_recovery_need =  wfix.fix_cpu_shr * wpht.pht_recovery_need
        wpht.pht_ram_recovery_need =  wfix.fix_ram_shr * wpht.pht_recovery_need 

        wpht.save()

        if wpht.pht_num == 1:
            w_t1_pht_budget = round(wpht.pht_budget, 2)
            w_t1_pht_cpu_recovery_need =  round(wpht.pht_cpu_recovery_need, 2) 
            w_t1_pht_ram_recovery_need =  round(wpht.pht_ram_recovery_need, 2) 
            w_t1_pht_hwm =  round(wpht.pht_hwm, 2)
            w_t1_pht_sfm = round(wpht.pht_sfm, 2)
        elif wpht.pht_num == 2:
            w_t2_pht_budget = round(wpht.pht_budget, 2)
            w_t2_pht_cpu_recovery_need =  round(wpht.pht_cpu_recovery_need, 2) 
            w_t2_pht_ram_recovery_need =  round(wpht.pht_ram_recovery_need, 2) 
            w_t2_pht_hwm =  round(wpht.pht_hwm, 2)
            w_t2_pht_sfm = round(wpht.pht_sfm, 2)
#
#   Distribute the Budget info to the Software Licenses and Subscription
#
    wslss = Software.objects.filter(sls_year=wyear);
    if wslss.count() == 0:
        w_RedHat_sls_mnt = 0
        w_PHA_sls_mnt = 0
        w_SUSE_sls_mnt = 0
    else:
        for wsls in wslss:
            if "PowerHA" in wsls.sls_name: 
                wsls.sls_cost = wfix.fix_ha_mnt_shr * wBgt.bgt_mnt_AIX
                w_PHA_sls_mnt = round(wsls.sls_cost, 2)
            elif "RedHat" in wsls.sls_name: 
                wsls.sls_cost = wfix.fix_RedHat_sub_shr * wBgt.bgt_sfm_LINUX
                w_RedHat_sls_mnt = round(wsls.sls_cost, 2)
            elif "SUSE" in wsls.sls_name: 
                wsls.sls_cost = wfix.fix_SUSE_sub_shr * wBgt.bgt_sfm_LINUX
                w_SUSE_sls_mnt = round(wsls.sls_cost, 2)
            wsls.save()    

    return render(request, "BudCorMidrange/budgetdistributed.html", {"budgetyear" : wyear,
        "w_t1_pht_cpu_recovery_need" : w_t1_pht_cpu_recovery_need,  
        "w_t1_pht_ram_recovery_need"  : w_t1_pht_ram_recovery_need, 
        "w_t1_pht_hwm" : w_t1_pht_hwm,
        "w_t2_pht_cpu_recovery_need" : w_t2_pht_cpu_recovery_need,  
        "w_t2_pht_ram_recovery_need"  : w_t2_pht_ram_recovery_need, 
        "w_t2_pht_hwm" : w_t2_pht_hwm,                            
        "w_t1_pht_sfm" : w_t1_pht_sfm,
        "w_t2_pht_sfm" : w_t2_pht_sfm,  
        "w_PHA_sls_mnt" : w_PHA_sls_mnt, 
        "w_gti_AIX" : w_gti_AIX,
        "w_gti_LINUX" : w_gti_LINUX,
        "w_esc_AIX" : w_esc_AIX,
        "w_esc_LINUX" : w_esc_LINUX,
        "w_esc_LINUX_Santam" : w_esc_LINUX_Santam,
        "w_RedHat_sls_mnt" : w_RedHat_sls_mnt,   
        "w_SUSE_sls_mnt" : w_SUSE_sls_mnt,     
        })
#
#   Loop thru 10 at a time
#   Entry.objects.all()[:10]
#   Entry.objects.all()[10:10]
#
#   Generate tariffs based on distribting dudget to Counters and splits 
#
def tariffs(request):
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
#   Get Counters
#
    try:
        wcnt = Counters.objects.get(id=1)
    except ObjectDoesNotExist:
            wmsg = 'Tariffs Module: No Counters Record'
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
       
    try:
        wBgt = Budget.objects.get(bgt_year=wyear)
    except ObjectDoesNotExist:
            wmsg = 'Tariffs Module: No Budget Record for year: ' + wyear
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
#
#   cpu/ram and maint tariffs
#

    try:
        wphts = PowerHardwareTier.objects.all()
        for wpht in wphts:
            if wpht.pht_num == 0:
                pass
            elif wpht.pht_num == 1:
                if wcnt.cnt_T1_cpu_appsrv != 0:
                    wtariff_AIX_cpu_pht1 = wpht.pht_cpu_recovery_need / wcnt.cnt_T1_cpu_appsrv
                else:
                    wtariff_AIX_cpu_pht1 = 0

                if wcnt.cnt_T1_ram_appsrv != 0:
                    wtariff_AIX_ram_pht1 = wpht.pht_ram_recovery_need / wcnt.cnt_T1_ram_appsrv
                else:
                    wtariff_AIX_ram_pht1 = 0

                if wcnt.cnt_T1_AIX_app_servers != 0:
                    wtariff_AIX_hwm_pht1 = wpht.pht_hwm / wcnt.cnt_T1_AIX_app_servers / 12
                    wtariff_AIX_sfm_pht1 = wpht.pht_sfm / wcnt.cnt_T1_AIX_app_servers / 12
                else:
                    wtariff_AIX_hwm_pht1 = 0 
                    wtariff_AIX_sfm_pht1 = 0

            elif wpht.pht_num == 2:
                if wcnt.cnt_T2_cpu_appsrv == 0:
                    wtariff_AIX_cpu_pht2 = 0
                else:
                    wtariff_AIX_cpu_pht2 = wpht.pht_cpu_recovery_need / wcnt.cnt_T2_cpu_appsrv

                if wcnt.cnt_T2_ram_appsrv == 0:
                    wtariff_AIX_ram_pht2 = 0
                else:
                    wtariff_AIX_ram_pht2 = wpht.pht_ram_recovery_need / wcnt.cnt_T2_ram_appsrv

                if wcnt.cnt_T2_AIX_app_servers == 0:
                    wtariff_AIX_hwm_pht2 = 0
                    wtariff_AIX_sfm_pht2 = 0 
                else:
                    wtariff_AIX_hwm_pht2 = wpht.pht_hwm / wcnt.cnt_T2_AIX_app_servers / 12
                    wtariff_AIX_sfm_pht2 = wpht.pht_sfm / wcnt.cnt_T2_AIX_app_servers / 12
                           
    except (ObjectDoesNotExist):
            wmsg = 'Tariffs Module: No PHT Records for year: ' + wyear 
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")
#
#   Divide all tariffs by 12 to get monthly rate, except cpu/ram already done        
#   Software Tariffs
#     
    wslss = Software.objects.filter(sls_year=wyear);
    if wslss.count() == 0:
        wtariff_AIX_powerHA = 0
        wtariff_RedHat = 0
        wtariff_SUSE =0
    else:
        for wsls in wslss:
            if "PowerHA" in wsls.sls_name:
                if wcnt.cnt_app_HA_Processors == 0:
                    wtariff_AIX_powerHA = 0
                else:
                    wtariff_AIX_powerHA = wsls.sls_cost / wcnt.cnt_app_HA_Processors / 12 
            elif "RedHat" in wsls.sls_name:
                if wcnt.cnt_Red_Hat_Default == 0:
                    wtariff_RedHat = 0
                else:
                    wtariff_RedHat = wsls.sls_cost / wcnt.cnt_Red_Hat_Default / 12
            elif "SUSE" in wsls.sls_name:
                if wcnt.cnt_SUSE == 0:
                    wtariff_SUSE =0
                else:
                    wtariff_SUSE = wsls.sls_cost / wcnt.cnt_SUSE / 12
#
#   gti Tariffs
#     
    wtariff_gti_dc = 0
    wtariff_gti_arch = 0
    wtariff_gti_bmc = 0
    wtariff_gti_rental = 0
    wtariff_gti_pm = 0
    wtariff_gti_AIX = 0
    wtariff_gti_LINUX = 0
    wtariff_AIX_esc = 0
    wtariff_LINUX_esc = 0
    wtariff_LINUX_esc_Santam = 0
  
    wcntAppServers = (wcnt.cnt_AIX_app_servers + wcnt.cnt_LINUX_Default)
#
    if wcnt.cnt_AIX_app_servers != 0:
        wtariff_gti_AIX = wBgt.bgt_gti_AIX / wcnt.cnt_AIX_app_servers / 12
        wtariff_AIX_esc = wBgt.bgt_esc_AIX / wcnt.cnt_AIX_app_servers / 12

    if wcnt.cnt_LINUX_Default != 0:
        wtariff_gti_LINUX = wBgt.bgt_gti_LINUX / wcnt.cnt_LINUX_Default / 12
        wtariff_LINUX_esc = wBgt.bgt_esc_LINUX / wcnt.cnt_LINUX_Default / 12
#
#   Data Centre External Service Provider 
#
    if wcnt.cnt_LINUX_Santam != 0:
        wtariff_LINUX_esc_Santam = wBgt.bgt_esc_LINUX_Santam / wcnt.cnt_LINUX_Santam / 12
#
#   Now save tariff in DB    
#      
    try:
        wTariff = Tariffs.objects.get(tariff_year=wyear)
        wTariff.tariff_AIX_cpu_pht1=wtariff_AIX_cpu_pht1
        wTariff.tariff_AIX_cpu_pht2=wtariff_AIX_cpu_pht2
        wTariff.tariff_AIX_ram_pht1=wtariff_AIX_ram_pht1
        wTariff.tariff_AIX_ram_pht2=wtariff_AIX_ram_pht2
        wTariff.tariff_AIX_hwm_pht1=wtariff_AIX_hwm_pht1
        wTariff.tariff_AIX_hwm_pht2=wtariff_AIX_hwm_pht2
        wTariff.tariff_AIX_esc=wtariff_AIX_esc
        wTariff.tariff_LINUX_esc=wtariff_LINUX_esc
        wTariff.tariff_LINUX_esc_Santam=wtariff_LINUX_esc_Santam
        wTariff.tariff_AIX_sfm_pht1=wtariff_AIX_sfm_pht1
        wTariff.tariff_AIX_sfm_pht2=wtariff_AIX_sfm_pht2
        wTariff.tariff_AIX_powerHA=wtariff_AIX_powerHA
        wTariff.tariff_RedHat=wtariff_RedHat
        wTariff.tariff_SUSE=wtariff_SUSE
        wTariff.tariff_gti_dc=wtariff_gti_dc
        wTariff.tariff_gti_arch=wtariff_gti_arch
        wTariff.tariff_gti_bmc=wtariff_gti_bmc
        wTariff.tariff_gti_rental=wtariff_gti_rental
        wTariff.tariff_gti_pm=wtariff_gti_pm
        wTariff.tariff_gti_AIX=wtariff_gti_AIX
        wTariff.tariff_gti_LINUX=wtariff_gti_LINUX
    
    except ObjectDoesNotExist:
        wTariff = Tariffs(
        tariff_year=wyear,    
        tariff_AIX_cpu_pht1=wtariff_AIX_cpu_pht1,
        tariff_AIX_cpu_pht2=wtariff_AIX_cpu_pht2,
        tariff_AIX_ram_pht1=wtariff_AIX_ram_pht1,
        tariff_AIX_ram_pht2=wtariff_AIX_ram_pht2,
        tariff_AIX_hwm_pht1=wtariff_AIX_hwm_pht1,
        tariff_AIX_hwm_pht2=wtariff_AIX_hwm_pht2,
        tariff_AIX_esc=wtariff_AIX_esc,
        tariff_LINUX_esc=wtariff_LINUX_esc,
        tariff_LINUX_esc_Santam=wtariff_LINUX_esc_Santam,
        tariff_AIX_sfm_pht1=wtariff_AIX_sfm_pht1,
        tariff_AIX_sfm_pht2=wtariff_AIX_sfm_pht2,
        tariff_AIX_powerHA=wtariff_AIX_powerHA,
        tariff_RedHat=wtariff_RedHat,
        tariff_SUSE=wtariff_SUSE,
        tariff_gti_dc=wtariff_gti_dc,
        tariff_gti_arch=wtariff_gti_arch,
        tariff_gti_bmc=wtariff_gti_bmc,
        tariff_gti_rental=wtariff_gti_rental,
        tariff_gti_pm=wtariff_gti_pm,
        tariff_gti_AIX=wtariff_gti_AIX,
        tariff_gti_LINUX=wtariff_gti_LINUX,
            )
    wTariff.save()

    wtariff_AIX_cpu_pht1 = round(wtariff_AIX_cpu_pht1, 2)
    wtariff_AIX_ram_pht1 = round(wtariff_AIX_ram_pht1, 2)
    wtariff_AIX_hwm_pht1 = round(wtariff_AIX_hwm_pht1, 2)
    wtariff_AIX_cpu_pht2 = round(wtariff_AIX_cpu_pht2, 2)
    wtariff_AIX_ram_pht2 = round(wtariff_AIX_ram_pht2, 2)
    wtariff_AIX_hwm_pht2 = round(wtariff_AIX_hwm_pht2, 2)
    wtariff_AIX_sfm_pht1 = round(wtariff_AIX_sfm_pht1, 2)
    wtariff_AIX_sfm_pht2 = round(wtariff_AIX_sfm_pht2, 2)
    wtariff_AIX_powerHA = round(wtariff_AIX_powerHA, 2)
    wtariff_AIX_esc = round(wtariff_AIX_esc, 2)
    wtariff_LINUX_esc = round(wtariff_LINUX_esc, 2)
    wtariff_gti_AIX = round(wtariff_gti_AIX, 2)
    wtariff_gti_LINUX = round(wtariff_gti_LINUX, 2)
    wtariff_RedHat = round(wtariff_RedHat, 2)
    wtariff_SUSE = round(wtariff_SUSE, 2)
    wtariff_LINUX_esc_Santam = round(wtariff_LINUX_esc_Santam, 2)
    
    return render(request, "BudCorMidrange/tariffs.html", {"budgetyear" : wyear,
        "wtariff_AIX_cpu_pht1" : wtariff_AIX_cpu_pht1,  
        "wtariff_AIX_ram_pht1" : wtariff_AIX_ram_pht1, 
        "wtariff_AIX_hwm_pht1" : wtariff_AIX_hwm_pht1,
        "wtariff_AIX_cpu_pht2" : wtariff_AIX_cpu_pht2,  
        "wtariff_AIX_ram_pht2" : wtariff_AIX_ram_pht2, 
        "wtariff_AIX_hwm_pht2" : wtariff_AIX_hwm_pht2,                            
        "wtariff_AIX_sfm_pht1" : wtariff_AIX_sfm_pht1,
        "wtariff_AIX_sfm_pht2" : wtariff_AIX_sfm_pht2,  
        "wtariff_AIX_powerHA" : wtariff_AIX_powerHA, 
        "wtariff_gti_AIX" : wtariff_gti_AIX,
        "wtariff_gti_LINUX" : wtariff_gti_LINUX,
        "wtariff_AIX_esc" : wtariff_AIX_esc,
        "wtariff_LINUX_esc" : wtariff_LINUX_esc,
        "wtariff_RedHat" : wtariff_RedHat,   
        "wtariff_SUSE" : wtariff_SUSE, 
        "wtariff_LINUX_esc_Santam" : wtariff_LINUX_esc_Santam,    
        })
#
#   Distribute Tariffs to Application Server 
#   
def appsrvcost(request):
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
#   Provide costs to app servers  
#   Get Counters
#
    try:
        wTariff = Tariffs.objects.get(tariff_year=wyear)
    except ObjectDoesNotExist:
        wmsg = 'Application Server Costing Module: No Tariff Record for year: ' + wyear 
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html")
    
    try:
        wcnt = Counters.objects.get(id=1)
    except ObjectDoesNotExist:
        wmsg = 'Application Server Costing Module: No Counters Record'  
        item = add_logmsg(wmsg)
        return render(request, "BudCor/error.html") 
#   
#   AIX Application Server Billing
#   To keep running total of Shared Services
#   
    wasb_asb_service = 'AIX'
    wbgt_inv_dpre_AIX = 0
    wbgt_inv_mnt_AIX = 0
    wbgt_inv_gti_AIX = 0
    wbgt_inv_esc_AIX = 0
    wnonBB9498cnt = wcnt.cnt_T1_AIX_app_servers + wcnt.cnt_T2_AIX_app_servers
    wtotBB9498 = 0
    wAIXsrvs = AIXServer.objects.all()
    for wAIXsrv in wAIXsrvs:

        wasb_asb_esc = 0 
        wasb_asb_gti = 0 
        wasb_asb_hwm = 0 
        wasb_asb_sfm  = 0 
        wasb_asb_ha = 0
        wasb_asb_cpu = 0 
        wasb_asb_ram = 0
        
        if wAIXsrv.srv_pht_tier == 0:
                pass
        else:
            wasb_asb_esc = wTariff.tariff_AIX_esc
            wasb_asb_gti = wTariff.tariff_gti_AIX 
            try:
                wPowerHA = PowerHAServer.objects.get(pha_name=wAIXsrv.srv_Name)
                wasb_asb_ha = wPowerHA.pha_num_logical_procs * wTariff.tariff_AIX_powerHA
            except ObjectDoesNotExist:
                pass 
        if wAIXsrv.srv_pht_tier == 1:
            wasb_asb_hwm = wTariff.tariff_AIX_hwm_pht1
            wasb_asb_sfm = wasb_asb_sfm + wTariff.tariff_AIX_sfm_pht1
            wasb_asb_cpu = wAIXsrv.srv_cpu * wTariff.tariff_AIX_cpu_pht1 
            wasb_asb_ram = wAIXsrv.srv_ram * wTariff.tariff_AIX_ram_pht1 
        elif wAIXsrv.srv_pht_tier == 2:
            wasb_asb_hwm = wTariff.tariff_AIX_hwm_pht2
            wasb_asb_sfm = wasb_asb_sfm + wTariff.tariff_AIX_sfm_pht2
            wasb_asb_cpu = wAIXsrv.srv_cpu * wTariff.tariff_AIX_cpu_pht2 
            wasb_asb_ram = wAIXsrv.srv_ram * wTariff.tariff_AIX_ram_pht2
#
#       Budget Income Totals 
#     
        wbgt_inv_dpre_AIX = wbgt_inv_dpre_AIX + wasb_asb_cpu + wasb_asb_ram 
        wbgt_inv_mnt_AIX = wbgt_inv_mnt_AIX + wasb_asb_sfm + wasb_asb_ha + wasb_asb_hwm
        wbgt_inv_gti_AIX = wbgt_inv_gti_AIX + wasb_asb_gti
        wbgt_inv_esc_AIX = wbgt_inv_esc_AIX + wasb_asb_esc
#        
#   Keep Shared technology billing running 
#
        if "BB9498" in wAIXsrv.srv_billingcc:
            wtotBB9498 = wasb_asb_hwm + wasb_asb_sfm + wasb_asb_cpu +  wasb_asb_ram + wasb_asb_gti + wasb_asb_esc + wtotBB9498
            wnonBB9498cnt = wnonBB9498cnt - 1 
#
#       GET Billing record for Server, if there
#
        try:
            wAppServerBilling = AppServerBilling.objects.get(asb_year=wyear, asb_name=wAIXsrv.srv_Name)
            wAppServerBilling.asb_service = wasb_asb_service
            wAppServerBilling.asb_client = wAIXsrv.srv_client
            wAppServerBilling.asb_hwm = wasb_asb_hwm
            wAppServerBilling.asb_sfm = wasb_asb_sfm
            wAppServerBilling.asb_ha = wasb_asb_ha
            wAppServerBilling.asb_cpu = wasb_asb_cpu 
            wAppServerBilling.asb_ram = wasb_asb_ram
            wAppServerBilling.asb_gti = wasb_asb_gti
            wAppServerBilling.asb_esc = wasb_asb_esc
            wAppServerBilling.asb_billingcc=wAIXsrv.srv_billingcc
            wAppServerBilling.asb_AIXtier=wAIXsrv.srv_pht_tier
        except ObjectDoesNotExist:
            wAppServerBilling = AppServerBilling(
            asb_name=wAIXsrv.srv_Name,
            asb_service = wasb_asb_service,
            asb_client = wAIXsrv.srv_client,
            asb_year=wyear,
            asb_hwm = wasb_asb_hwm,
            asb_sfm = wasb_asb_sfm,
            asb_ha = wasb_asb_ha,
            asb_cpu = wasb_asb_cpu, 
            asb_ram = wasb_asb_ram,
            asb_gti = wasb_asb_gti,
            asb_esc = wasb_asb_esc,
            asb_billingcc=wAIXsrv.srv_billingcc,
            asb_AIXtier=wAIXsrv.srv_pht_tier,
            ) 
        wAppServerBilling.save()  
#  
#       Shared Technology e.g. VIO App Services
#
    if wnonBB9498cnt == 0:
        pass
    else:
        wtariff_BB9498 = wtotBB9498 / wnonBB9498cnt
        wasbnonBB9498s = AppServerBilling.objects.exclude(asb_billingcc='BB9498').exclude(asb_AIXtier=0).exclude(asb_service='LINUX')
        for wasbnonBB9498 in wasbnonBB9498s:
            wasbnonBB9498.asb_stc = wtariff_BB9498
            wasbnonBB9498.save()
#
#   LINUX App Server Billing
#
    wasb_asb_service = 'LINUX'
    wbgt_inv_esc_LINUX = 0    
    wbgt_inv_gti_LINUX = 0 
    wbgt_inv_sfm_LINUX = 0
    wbgt_inv_esc_LINUX_Santam = 0
    wasb_asb_hwm = 0 
    wasb_asb_ha = 0
    wasb_asb_cpu = 0 
    wasb_asb_ram = 0
#
    wLINUXsrvs = LINUXServer.objects.all()
    wnonBB8263cnt = wLINUXsrvs.count()
    wtotBB8263 = 0
    for wLINUXsrv in wLINUXsrvs:
         
        wasb_asb_esc = 0
        wasb_asb_gti = 0 
        wasb_asb_sfm  = 0 
        try:
            wclient = ClientDirectBilling.objects.get(cdb_client=wLINUXsrv.srv_client,cdb_service=wasb_asb_service)
        except ObjectDoesNotExist:
            wclient = ClientDirectBilling.objects.get(cdb_client='Default',cdb_service=wasb_asb_service)

# 
        if 'y' in wclient.cdb_other_svc:
            pass
        else:
            if 'BCX OSS (Linux)' in wLINUXsrv.srv_competency:
                wasb_asb_esc = wTariff.tariff_LINUX_esc
                wbgt_inv_esc_LINUX = wbgt_inv_esc_LINUX + wasb_asb_esc
            else:
                wasb_asb_esc = 0  

        if 'y' in wclient.cdb_other_gti:
            pass
        else:
            if 'BCX OSS (Linux)' in wLINUXsrv.srv_competency:
                wasb_asb_gti = wTariff.tariff_gti_LINUX
                wbgt_inv_gti_LINUX = wbgt_inv_gti_LINUX + wasb_asb_gti
            else:
                wasb_asb_gti = 0
        
        if 'y' in wclient.cdb_other_sfm:
            pass
        else:
            if  'Red Hat' in wLINUXsrv.srv_OS:
                wasb_asb_sfm = wTariff.tariff_RedHat
                wbgt_inv_sfm_LINUX = wbgt_inv_sfm_LINUX + wasb_asb_sfm
            else:
                try:
                    wSUSE = SUSEServer.objects.get(SUSE_name=wLINUXsrv.srv_Name)
                    wasb_asb_sfm = wSUSE.SUSE_num_sockets * wTariff.tariff_SUSE
                    wbgt_inv_sfm_LINUX = wbgt_inv_sfm_LINUX + wasb_asb_sfm
                except ObjectDoesNotExist:
                    pass 

        if 'Santam' in wLINUXsrv.srv_client:
            if 'BCX OSS (Linux)' in wLINUXsrv.srv_competency:
                wasb_asb_esc = wTariff.tariff_LINUX_esc_Santam
                wbgt_inv_esc_LINUX_Santam = wbgt_inv_esc_LINUX_Santam + wasb_asb_esc
#        
#   Keep Shared technology billing running  
#
        if "BB8263" in wLINUXsrv.srv_billingcc:
            wtotBB8263 = wasb_asb_sfm + wasb_asb_gti + wasb_asb_esc + wtotBB8263
            wnonBB8263cnt = wnonBB8263cnt - 1 
#
#       GET Billing record for Server, if there
#
        try:
            wAppServerBilling = AppServerBilling.objects.get(asb_year=wyear, asb_name=wLINUXsrv.srv_Name)
            wAppServerBilling.asb_service = wasb_asb_service
            wAppServerBilling.asb_client = wLINUXsrv.srv_client
            wAppServerBilling.asb_sfm = wasb_asb_sfm
            wAppServerBilling.asb_gti = wasb_asb_gti
            wAppServerBilling.asb_esc = wasb_asb_esc
            wAppServerBilling.asb_billingcc=wLINUXsrv.srv_billingcc
            wAppServerBilling.asb_hwm = wasb_asb_hwm
            wAppServerBilling.asb_ha = wasb_asb_ha
            wAppServerBilling.asb_cpu = wasb_asb_cpu 
            wAppServerBilling.asb_ram = wasb_asb_ram
        except ObjectDoesNotExist:
            wAppServerBilling = AppServerBilling(
            asb_name=wLINUXsrv.srv_Name,
            asb_service = wasb_asb_service,
            asb_client = wLINUXsrv.srv_client,
            asb_year=wyear,
            asb_sfm = wasb_asb_sfm,
            asb_gti = wasb_asb_gti,
            asb_esc = wasb_asb_esc,
            asb_hwm = wasb_asb_hwm,
            asb_ha = wasb_asb_ha,
            asb_cpu = wasb_asb_cpu, 
            asb_ram = wasb_asb_ram,
            asb_billingcc=wLINUXsrv.srv_billingcc,
            ) 
        wAppServerBilling.save()  
#  
#       Shared Technology 
#
    if wnonBB8263cnt == 0:
        pass
    else:
        wtariff_BB8263 = wtotBB8263 / wnonBB8263cnt
        wasbnonBB8263s = AppServerBilling.objects.filter(asb_service='LINUX').exclude(asb_billingcc='BB8263')
        for wasbnonBB8263 in wasbnonBB8263s:
            wasbnonBB8263.asb_stc = wtariff_BB8263
            wasbnonBB8263.save()
#
#   Update Budget Invoice
#     
    try:
        wBgt = Budget.objects.get(bgt_year=wyear)
        pass
    except ObjectDoesNotExist:
            wmsg = 'Budget Distribution Module: No Budget data for Year:' + wyear
            item = add_logmsg(wmsg)
            return render(request, "BudCor/error.html")

    wBgt.bgt_inv_dpre_AIX = round(wbgt_inv_dpre_AIX,2) * 12
    wBgt.bgt_inv_mnt_AIX = round(wbgt_inv_mnt_AIX,2) * 12
    wBgt.bgt_inv_gti_AIX = round(wbgt_inv_gti_AIX,2) * 12
    wBgt.bgt_inv_esc_AIX = round(wbgt_inv_esc_AIX,2) * 12
    wBgt.bgt_inv_esc_LINUX = round(wbgt_inv_esc_LINUX,2) * 12  
    wBgt.bgt_inv_gti_LINUX = round(wbgt_inv_gti_LINUX,2) * 12
    wBgt.bgt_inv_sfm_LINUX = round(wbgt_inv_sfm_LINUX,2) * 12
    wBgt.bgt_inv_esc_LINUX_Santam = round(wbgt_inv_esc_LINUX_Santam,2) * 12
    wBgt.save()

    return render(request, "BudCorMidrange/appsrvcost.html", {"budgetyear" : wyear, })
#