from import_export import resources

from .models import *

class AIXServerResource(resources.ModelResource):
    class Meta:
        model = AIXServer
        import_id_fields = ['srv_Name']
        skip_unchanged= True
        report_skipped = False
        exclude = ('Annotationfinancialgroup')

class LINUXServerResource(resources.ModelResource):
    class Meta:
        model = LINUXServer
        import_id_fields = ['srv_Name']
        skip_unchanged= True
        report_skipped = False
        exclude = ('Annotationfinancialgroup')

class FixedValueResource(resources.ModelResource):
    class Meta:
        model = FixedValue
        import_id_fields = ['fix_year']
        skip_unchanged= True
        report_skipped = False

class BudgetResource(resources.ModelResource):
    class Meta:
        model = Budget
        import_id_fields = ['bgt_year']
        skip_unchanged= True
        report_skipped = False

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        skip_unchanged= True
        report_skipped = False

class SoftwareResource(resources.ModelResource):
    class Meta:
        model = Software
        skip_unchanged= True
        report_skipped = False   

class SUSEServerResource(resources.ModelResource):
    class Meta:
        model = SUSEServer
        import_id_fields = ['SUSE_name']
        skip_unchanged= True
        report_skipped = False 

class PowerHAServerResource(resources.ModelResource):
    class Meta:
        model = PowerHAServer
        import_id_fields = ['pha_name']
        skip_unchanged= True
        report_skipped = False       

class ClientDirectBillingResource(resources.ModelResource):
    class Meta:
        model = ClientDirectBilling
        skip_unchanged= True
        report_skipped = False           

class OperatingSystemResource(resources.ModelResource):
    class Meta:
        model = OperatingSystem
        skip_unchanged= True
        report_skipped = False           

class PowerHardwareServerResource(resources.ModelResource):
    class Meta:
        model = PowerHardwareServer
        import_id_fields = ['phs_name']
        skip_unchanged= True
        report_skipped = False   

class PowerHardwareTierResource(resources.ModelResource):
    class Meta:
        model = PowerHardwareTier
        import_id_fields = ['pht_num']
        skip_unchanged= True
        report_skipped = False

class AppServerBillingResource(resources.ModelResource):
    class Meta:
        model = AppServerBilling
        report_skipped = False