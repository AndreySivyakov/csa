# Generated by Django 2.2.5 on 2020-01-27 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filed1', models.CharField(max_length=100)),
                ('filed2', models.BigIntegerField()),
            ],
        ),
    ]
