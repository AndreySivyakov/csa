# Generated by Django 3.0.3 on 2020-03-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0007_form2_form2_plant_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='form2',
            name='form2_parent_field_ref',
            field=models.IntegerField(default=None, null=True),
        ),
    ]