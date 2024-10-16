# Generated by Django 5.1 on 2024-09-12 13:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0004_alter_appointment_options_alter_schedule_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='duration',
            field=models.IntegerField(blank=True, default=60, help_text='По умолчанию 60 минут'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='reserved_for_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
