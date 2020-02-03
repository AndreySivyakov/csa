# Generated by Django 2.2.5 on 2020-01-26 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True)),
                ('user_name', models.CharField(max_length=50, null=True)),
                ('contract_type', models.CharField(max_length=100, null=True)),
                ('request_type', models.CharField(max_length=100, null=True)),
                ('paper_contr_type', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('sub_category', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_vendor_number', models.PositiveIntegerField(default=None, null=True)),
                ('parent_vendor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('parent_contr_name', models.CharField(blank=True, max_length=40, null=True)),
                ('parent_PGrp', models.CharField(blank=True, max_length=50, null=True)),
                ('parent_POrg', models.CharField(blank=True, max_length=50, null=True)),
                ('parent_contr_number', models.BigIntegerField(default=None, null=True)),
                ('parent_contract_setup_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csa_app.Setup')),
            ],
        ),
        migrations.CreateModel(
            name='ChildContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_vendor_number', models.PositiveIntegerField(default=None, null=True)),
                ('child_vendor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('child_contr_name', models.CharField(blank=True, max_length=100, null=True)),
                ('child_PGrp', models.CharField(blank=True, max_length=50, null=True)),
                ('child_POrg', models.CharField(blank=True, max_length=50, null=True)),
                ('child_parent_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csa_app.ParentContract')),
            ],
        ),
        migrations.CreateModel(
            name='AmendmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amendment_type', models.CharField(max_length=500, null=True)),
                ('setup_reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csa_app.Setup')),
            ],
        ),
    ]
