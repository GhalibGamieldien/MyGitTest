from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from .models import *
from .resource import * 

# Register your models here.
@admin.register(AIXServer)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = AIXServerResource
    pass

@admin.register(LINUXServer)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = LINUXServerResource
    pass

@admin.register(FixedValue)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = FixedValueResource
    pass

@admin.register(Budget)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = BudgetResource
    pass

@admin.register(Service)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource
    pass

@admin.register(SUSEServer)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = SUSEServerResource
    pass

@admin.register(PowerHAServer)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = PowerHAServerResource
    pass

@admin.register(ClientDirectBilling)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = ClientDirectBillingResource
    pass

@admin.register(OperatingSystem)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = OperatingSystemResource
    pass

@admin.register(Software)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = SoftwareResource
    pass

@admin.register(PowerHardwareServer)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = PowerHardwareServerResource
    pass

@admin.register(PowerHardwareTier)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = PowerHardwareTierResource
    pass