# Generated by Django 3.1.7 on 2021-03-07 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acionamentos', '0003_auto_20210307_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='acionamento',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='acionamento',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
