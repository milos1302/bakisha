# Generated by Django 3.0.3 on 2020-02-23 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200223_0935'),
        ('game', '0006_game_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Organization'),
        ),
    ]
