# Generated by Django 3.0.3 on 2020-02-25 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20200225_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='users',
            new_name='members',
        ),
    ]
