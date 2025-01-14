# Generated by Django 4.2.18 on 2025-01-14 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='requested_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Requested By'),
            preserve_default=False,
        ),
    ]
