# Generated by Django 2.1.15 on 2020-02-26 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0002_auto_20200220_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form5_1', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_2', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_3', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_4', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_5', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_6', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_7', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_8', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_9', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_10', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_11', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_12', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_13', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_14', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_15', models.CharField(blank=True, max_length=3, null=True)),
                ('form5_setup_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csa_app.Setup')),
            ],
        ),
    ]