# Generated by Django 3.0.3 on 2020-06-05 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIXServer',
            fields=[
                ('srv_Name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('srv_OS', models.CharField(max_length=100)),
                ('srv_competency', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_application', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_serverdescription', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_sla', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_assetowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_client', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('srv_financialgroup', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_billingcc', models.CharField(blank=True, db_index=True, max_length=12, null=True)),
                ('srv_service', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_cpu', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('srv_ram', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('srv_phs_model', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_phs_serial_num', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_phs_name', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_primarytechowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_secondarytechowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_appowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_location', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_pht_tier', models.IntegerField(default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('bgt_year', models.IntegerField(primary_key=True, serialize=False)),
                ('bgt_dpre_AIX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_loi', models.DecimalField(decimal_places=2, max_digits=11)),
                ('bgt_mnt_AIX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_sfm_LINUX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_gti_AIX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_gti_LINUX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_esc_AIX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_esc_LINUX', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bgt_esc_LINUX_Santam', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_dpre_AIX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_mnt_AIX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_sfm_LINUX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_gti_AIX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_gti_LINUX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_esc_AIX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_esc_LINUX', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('bgt_inv_esc_LINUX_Santam', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Counters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt_AIX_app_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_T1_AIX_app_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_T2_AIX_app_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_AIX_svc_cc', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_T0_cpu_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_T1_cpu_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_T2_cpu_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_T0_ram_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_T1_ram_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_T2_ram_appsrv', models.DecimalField(decimal_places=3, default=0, max_digits=12, null=True)),
                ('cnt_app_HA_Processors', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_app_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_svc_cc', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_competency', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_Default', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_Santam', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_LINUX_SKY', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_Red_Hat_Default', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_Red_Hat_Santam', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_Red_Hat_SKY', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('cnt_SUSE', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FixedValue',
            fields=[
                ('fix_year', models.IntegerField(primary_key=True, serialize=False)),
                ('fix_interest', models.DecimalField(decimal_places=3, default=1.0, max_digits=7, null=True)),
                ('fix_depr_years', models.IntegerField(default=3)),
                ('fix_ext_svc_col', models.DecimalField(decimal_places=3, max_digits=7)),
                ('fix_vat', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_cpu_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_ram_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_AIX_growth', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_AIX_hwm_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_ha_mnt_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_AIX_sfm_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_RedHat_sub_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
                ('fix_SUSE_sub_shr', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LINUXServer',
            fields=[
                ('srv_Name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('srv_OS', models.CharField(max_length=100)),
                ('srv_competency', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_application', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_serverdescription', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_sla', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_assetowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_client', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('srv_financialgroup', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_billingcc', models.CharField(blank=True, db_index=True, max_length=12, null=True)),
                ('srv_service', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_cpu', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('srv_ram', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('srv_phs_model', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_phs_serial_num', models.CharField(blank=True, max_length=100, null=True)),
                ('srv_phs_name', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_primarytechowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_secondarytechowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_appowner', models.CharField(blank=True, max_length=50, null=True)),
                ('srv_location', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('log_date', models.DateTimeField(verbose_name='date logged')),
            ],
        ),
        migrations.CreateModel(
            name='PowerHardwareServer',
            fields=[
                ('phs_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('phs_tier', models.IntegerField(default=0)),
                ('phs_serial_num', models.CharField(max_length=50, null=True)),
                ('phs_model', models.CharField(max_length=50)),
                ('phs_cpu', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('phs_ram', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('phs_type', models.CharField(max_length=50)),
                ('phs_date_bought', models.DateField(max_length=10)),
                ('phs_price_bought', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('phs_asset_reg', models.CharField(max_length=50)),
                ('phs_eol', models.CharField(choices=[('y', 'Yes'), ('n', 'No')], max_length=1)),
                ('phs_location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PowerHardwareTier',
            fields=[
                ('pht_num', models.IntegerField(primary_key=True, serialize=False)),
                ('pht_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_budget', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_recovery_need', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_appl_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_cpu_alloc', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_ram_alloc', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_cpu_recovery_need', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_ram_recovery_need', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_recovered', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_num_servers', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_cpu', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_ram', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_hwm', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_sfm', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('pht_mnt_budget_shr', models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True)),
                ('pht_dpre_budget_shr', models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PowerHAServer',
            fields=[
                ('pha_mngd_syst_name', models.CharField(max_length=50)),
                ('pha_Serial_num', models.CharField(max_length=50)),
                ('pha_cluster_internal_name', models.CharField(max_length=50)),
                ('pha_cluster_name', models.CharField(max_length=100)),
                ('pha_type', models.CharField(max_length=100)),
                ('pha_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('pha_os', models.CharField(max_length=50)),
                ('pha_billing_cc', models.CharField(db_index=True, max_length=12)),
                ('pha_num_logical_procs', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SUSEServer',
            fields=[
                ('SUSE_name', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('SUSE_num_sockets', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Tariffs',
            fields=[
                ('tariff_year', models.IntegerField(primary_key=True, serialize=False)),
                ('tariff_AIX_cpu_pht1', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_cpu_pht2', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_ram_pht1', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_ram_pht2', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_hwm_pht1', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_hwm_pht2', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_sfm_pht1', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_sfm_pht2', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_powerHA', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_RedHat', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_SUSE', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_dc', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_arch', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_bmc', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_rental', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_pm', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_AIX', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_gti_LINUX', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_AIX_esc', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_LINUX_esc', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('tariff_LINUX_esc_Santam', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sls_year', models.IntegerField(default=2020)),
                ('sls_name', models.CharField(default='Ops', max_length=50)),
                ('sls_svc', models.CharField(max_length=50)),
                ('sls_opsys', models.CharField(max_length=50)),
                ('sls_date', models.DateField(max_length=50)),
                ('sls_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
            ],
            options={
                'unique_together': {('sls_year', 'sls_name')},
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('svc_year', models.IntegerField(default=2020)),
                ('svc_client', models.CharField(default='Default', max_length=25)),
                ('svc_name', models.CharField(max_length=25)),
                ('svc_provider', models.CharField(max_length=25)),
                ('svc_comp', models.CharField(max_length=25)),
                ('svc_manager', models.CharField(max_length=35)),
                ('svc_lead', models.CharField(max_length=35)),
                ('svc_platform_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
                ('svc_acnt_mgmt_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
                ('svc_cons_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
            ],
            options={
                'unique_together': {('svc_year', 'svc_name', 'svc_client')},
            },
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osy_year', models.IntegerField(default=2020)),
                ('osy_name', models.CharField(max_length=50)),
                ('osy_svc', models.CharField(max_length=50)),
                ('osy_hardware', models.CharField(max_length=50)),
                ('osy_desc', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('osy_year', 'osy_name')},
            },
        ),
        migrations.CreateModel(
            name='ClientDirectBilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdb_client', models.CharField(max_length=50)),
                ('cdb_service', models.CharField(max_length=25)),
                ('cdb_other_depr', models.CharField(max_length=1)),
                ('cdb_other_hwm', models.CharField(max_length=1)),
                ('cdb_other_sfm', models.CharField(max_length=1)),
                ('cdb_other_gti', models.CharField(max_length=1)),
                ('cdb_other_svc', models.CharField(max_length=1)),
            ],
            options={
                'unique_together': {('cdb_client', 'cdb_service')},
            },
        ),
        migrations.CreateModel(
            name='AppServerBilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asb_year', models.IntegerField(default=2020, null=True)),
                ('asb_name', models.CharField(max_length=50)),
                ('asb_service', models.CharField(max_length=15, null=True)),
                ('asb_client', models.CharField(max_length=25, null=True)),
                ('asb_esc', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_gti', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_hwm', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_sfm', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_ha', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_cpu', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_ram', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_stc', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('asb_AIXtier', models.IntegerField(default=0)),
                ('asb_billingcc', models.CharField(blank=True, db_index=True, max_length=12, null=True)),
            ],
            options={
                'unique_together': {('asb_year', 'asb_name')},
            },
        ),
    ]
