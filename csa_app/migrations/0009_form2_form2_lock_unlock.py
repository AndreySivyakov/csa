# Generated by Django 3.0.3 on 2020-03-04 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0008_form2_form2_parent_field_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='form2',
            name='form2_lock_unlock',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]