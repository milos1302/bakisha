# Generated by Django 3.0.3 on 2020-03-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200301_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(default='images/app/user/account/default.png', upload_to='images/user/account'),
        ),
    ]
