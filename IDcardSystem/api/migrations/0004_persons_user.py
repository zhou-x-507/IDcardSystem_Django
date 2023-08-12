# Generated by Django 4.2.3 on 2023-08-08 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_remove_register_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户（管理员）'),
            preserve_default=False,
        ),
    ]
