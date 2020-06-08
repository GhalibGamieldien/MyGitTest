from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#
#   Users can log messages and by app to log some errors
#
class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"   

    def get_absolute_url(self):
        return reverse('list_messages')
#
#   Application DB
#
#   Server: Import this data
#
class ApplicationServer(models.Model):
    srv_Name = models.CharField (max_length=50, primary_key=True)
    srv_OS = models.CharField (max_length=100)
    srv_competency = models.CharField (max_length=50, blank=True, null=True)
    srv_application = models.CharField (max_length=100, blank=True, null=True)
    srv_serverdescription = models.CharField (max_length=100, blank=True, null=True)
    srv_sla = models.CharField (max_length=50, blank=True, null=True)
    srv_assetowner = models.CharField (max_length=50, blank=True, null=True)
    srv_client = models.CharField (max_length=50, db_index=True, blank=True, null=True)
    srv_financialgroup = models.CharField (max_length=50, blank=True, null=True)
    srv_billingcc = models.CharField (max_length=12, db_index=True, blank=True, null=True)
    srv_service = models.CharField (max_length=50, blank=True, null=True)
    srv_cpu = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    srv_ram = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    srv_phs_model = models.CharField (max_length=50, blank=True, null=True)
    srv_phs_serial_num = models.CharField (max_length=100, blank=True, null=True)
    srv_phs_name = models.CharField (max_length=50, blank=True, null=True)
    srv_primarytechowner = models.CharField (max_length=50, blank=True, null=True)
    srv_secondarytechowner = models.CharField (max_length=50, blank=True, null=True)
    srv_appowner = models.CharField (max_length=50, blank=True, null=True)
    srv_location = models.CharField (max_length=50, blank=True, null=True)

    class Meta:
        abstract=True 
                  
    def __str__(self):
        return '{0:<20} {1:<20}: CPU: {2:^12} RAM: {3:<12}'.format(
        self.srv_OS,
        self.srv_Name, 
        self.srv_cpu, 
        self.srv_ram, 
        )
    
class AIXServer(ApplicationServer):
    srv_pht_tier = models.IntegerField (null=True, default=0)
    pass

class LINUXServer(ApplicationServer):
    pass
#
#   Fixed Values:   Import this data  
#
class FixedValue(models.Model):
    fix_year = models.IntegerField (primary_key=True)
    fix_interest = models.DecimalField (max_digits=7, decimal_places=3, null=True, default=1.0)
    fix_depr_years = models.IntegerField (default=3)
    fix_ext_svc_col = models.DecimalField (max_digits=7, decimal_places=3)
    fix_vat = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_cpu_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_ram_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_AIX_growth = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_AIX_hwm_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_ha_mnt_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_AIX_sfm_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_RedHat_sub_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
    fix_SUSE_sub_shr = models.DecimalField (max_digits=5, decimal_places=3, null=True, default=1.0)
       
    def __str__(self):
        return 'Year {0:<20}: CPU Factor: {1:<20} RAM Factor: {2:^12}'.format(
        self.fix_year,
        self.fix_cpu_shr, 
        self.fix_ram_shr, 
        )
# 
#   Budget Values:  Import this data
#
class Budget(models.Model):
    bgt_year = models.IntegerField (primary_key=True)
    bgt_dpre_AIX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_loi = models.DecimalField (max_digits=11, decimal_places=2)
    bgt_mnt_AIX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_sfm_LINUX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_gti_AIX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_gti_LINUX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_esc_AIX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_esc_LINUX = models.DecimalField (max_digits=15, decimal_places=2)
    bgt_esc_LINUX_Santam = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_dpre_AIX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_mnt_AIX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_sfm_LINUX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_gti_AIX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_gti_LINUX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_esc_AIX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_esc_LINUX = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    bgt_inv_esc_LINUX_Santam = models.DecimalField (max_digits=15, decimal_places=2, null=True, default=0)
    
    def __str__(self):
        return 'Year: {0:<20}'.format(
        self.bgt_year,
        )
#
#   Sub-Services Provided:  Import this data
# 
class Service(models.Model):
    svc_year = models.IntegerField (default=2020)
    svc_client = models.CharField (max_length=25, default='Default') 
    svc_name = models.CharField (max_length=25)
    svc_provider = models.CharField (max_length=25)
    svc_comp = models.CharField (max_length=25)
    svc_manager = models.CharField (max_length=35)
    svc_lead = models.CharField (max_length=35)
    svc_platform_cost = models.DecimalField (max_digits=15, decimal_places=2, blank=True, default=0)
    svc_acnt_mgmt_cost = models.DecimalField (max_digits=15, decimal_places=2, blank=True, default=0)
    svc_cons_cost = models.DecimalField (max_digits=15, decimal_places=2, blank=True, default=0)

    class Meta:
        unique_together = [['svc_year', 'svc_name', 'svc_client']]
    
    def __str__(self):
        return 'Year:{0:<4}, Service: {1:<12}, Client: {2:<20}, Provider: {3:<20}, Competency: {4:<12}'.format(
        self.svc_year,
        self.svc_name,
        self.svc_client,
        self.svc_provider,
        self.svc_comp, 
        )
#
#   Server List for SUSE License Cost: Import  this data
#
class SUSEServer(models.Model):
    SUSE_name = models.CharField (max_length=60, primary_key=True)
    SUSE_num_sockets = models.IntegerField (default=2)

    def __str__(self):
        return 'Server: {}, # Sockets: {}'.format(
        self.SUSE_name,
        self.SUSE_num_sockets,
        )
#
#   Server List for Systen Mirror (PowerHA) License Cost: Import  this data
#
class PowerHAServer(models.Model):
    pha_mngd_syst_name = models.CharField (max_length=50)
    pha_Serial_num = models.CharField (max_length=50)
    pha_cluster_internal_name = models.CharField (max_length=50)
    pha_cluster_name = models.CharField (max_length=100)
    pha_type = models.CharField (max_length=100)
    pha_name = models.CharField (max_length=50, primary_key=True)
    pha_os = models.CharField (max_length=50)
    pha_billing_cc = models.CharField (max_length=12, db_index=True)
    pha_num_logical_procs = models.IntegerField (null=True, default=0)
       
    def __str__(self):
        return 'Server: {0:<20} Logical Procs: {1:<5} Cluster: {2:<25}'.format(
        self.pha_name,
        self.pha_num_logical_procs, 
        self.pha_cluster_name
        )
#
#   Clients wo do not take all of shared (Sub)services, i.e. non-Default
#
class ClientDirectBilling(models.Model):
    cdb_client = models.CharField (max_length=50)
    cdb_service = models.CharField (max_length=25)
    cdb_other_depr = models.CharField (max_length=1)
    cdb_other_hwm = models.CharField (max_length=1)
    cdb_other_sfm = models.CharField (max_length=1)
    cdb_other_gti = models.CharField (max_length=1)
    cdb_other_svc = models.CharField (max_length=1)
    
    class Meta:
        unique_together = [['cdb_client', 'cdb_service']]
        
    def __str__(self):
        return 'Client: {0:^30} Service: {1:<5}'.format(
        self.cdb_client,
        self.cdb_service,
        )
#
#   Operating systems 
#
class OperatingSystem(models.Model):
    osy_year = models.IntegerField (default=2020)
    osy_name = models.CharField (max_length=50)
    osy_svc = models.CharField (max_length=50)
    osy_hardware = models.CharField (max_length=50)
    osy_desc = models.CharField (max_length=50)
    
    class Meta:
        unique_together = [['osy_year', 'osy_name']]

    def __str__(self):
        return 'Operating System: {0:<20}'.format(
        self.osy_name,
        )
#
#   Software License List
#
class Software(models.Model):
    sls_year = models.IntegerField (default=2020)
    sls_name = models.CharField (max_length=50, default='Ops')
    sls_svc = models.CharField (max_length=50)
    sls_opsys = models.CharField (max_length=50)
    sls_date = models.DateField (max_length=50)
    sls_cost = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
   
    class Meta:
        unique_together = [['sls_year', 'sls_name']]

    def __str__(self):
        return 'Year: {0}, Name: {1:<10}, Date Due: {2}, Operating System: {3:<30}'.format(
            self.sls_year,
            self.sls_name,
            self.sls_date,
            self.sls_opsys, 
        )
#
#   Grouping of Power Hardware Servers
#
class PowerHardwareTier(models.Model):
    pht_num = models.IntegerField (primary_key=True)
    pht_price = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0);
    pht_budget = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_recovery_need = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_appl_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_cpu_alloc = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_ram_alloc = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_cpu_recovery_need = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_ram_recovery_need = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_recovered = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_num_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_cpu = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_ram = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_hwm = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_sfm = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    pht_mnt_budget_shr = models.DecimalField (max_digits=6, decimal_places=3, null=True, default=0) # Share for HWM and SFM
    pht_dpre_budget_shr = models.DecimalField (max_digits=6, decimal_places=3, null=True, default=0) # Share for Depreciation
    
    def __str__(self):
        return 'Tier: {0:<10}'.format(
        self.pht_num,
        )
#
#   Power Hardware Servers
#
class PowerHardwareServer(models.Model):
    phs_name = models.CharField (max_length=50, primary_key=True)
    phs_tier = models.IntegerField (default=0)
    phs_serial_num = models.CharField (max_length=50, null=True)
    phs_model = models.CharField (max_length=50)
    phs_cpu = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0) 
    phs_ram = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    phs_type = models.CharField (max_length=50)
    phs_date_bought = models.DateField (max_length=10)
    phs_price_bought = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    phs_asset_reg = models.CharField (max_length=50)
    phs_eol_choices = (
        ("y", "Yes"),
        ("n", "No"),
    )
    phs_eol = models.CharField (max_length=1, choices=phs_eol_choices)
    phs_location = models.CharField (max_length=50)
        
    def __str__(self):
        return 'Server Name: {0:<40} Serial Number: {1}'.format(
            self.phs_name,
            self.phs_serial_num,
            )
#
#   From here data is application generated
#
#   Counters and Splits to create tariffs
#
class Counters(models.Model):
    cnt_AIX_app_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_T1_AIX_app_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_T2_AIX_app_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_AIX_svc_cc = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_T0_cpu_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_T1_cpu_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_T2_cpu_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_T0_ram_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_T1_ram_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_T2_ram_appsrv = models.DecimalField (max_digits=12, decimal_places=3, null=True, default=0)
    cnt_app_HA_Processors = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_app_servers = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_svc_cc = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_competency = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_Default = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_Santam = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_LINUX_SKY = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_Red_Hat_Default = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_Red_Hat_Santam = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_Red_Hat_SKY = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    cnt_SUSE = models.DecimalField (max_digits=12, decimal_places=2, null=True, default=0)
    
    def __str__(self):
        pass
#
#   Tariffs for (sub)Services
#    
class Tariffs(models.Model):
    tariff_year = models.IntegerField (primary_key=True)  
    tariff_AIX_cpu_pht1 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0) 
    tariff_AIX_cpu_pht2 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_ram_pht1 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_ram_pht2 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_hwm_pht1 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_hwm_pht2 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_sfm_pht1 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_sfm_pht2 = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_powerHA = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_RedHat = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_SUSE = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_dc = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_arch = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_bmc = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_rental = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_pm = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_AIX = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_gti_LINUX = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_AIX_esc = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_LINUX_esc = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0)
    tariff_LINUX_esc_Santam = models.DecimalField (max_digits=9, decimal_places=3, null=True, default=0) 

    def __str__(self):
        pass
#
#   Costing table for original Server List
#
class AppServerBilling(models.Model):
    asb_year = models.IntegerField (null=True, default=2020)
    asb_name = models.CharField (max_length=50)
    asb_service = models.CharField (max_length=15, null=True)
    asb_client = models.CharField (max_length=25, null=True)
    asb_esc = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_gti = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_hwm = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_sfm = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0) 
    asb_ha = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_cpu = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_ram = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_stc = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    asb_AIXtier = models.IntegerField (default=0)
    asb_billingcc = models.CharField (max_length=12, db_index=True, blank=True, null=True)
#                
    class Meta:
        unique_together = [['asb_year', 'asb_name']] 
#