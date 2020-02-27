# Generated by Django 3.0.3 on 2020-02-26 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.GameType'),
        ),
    ]