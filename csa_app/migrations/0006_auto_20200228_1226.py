# Generated by Django 3.0.3 on 2020-02-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0005_auto_20200227_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form2',
            name='form2_target_value',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]