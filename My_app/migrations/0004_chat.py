# Generated by Django 5.1 on 2024-10-03 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0003_favorites_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('FROMID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fromid', to='My_app.login_table')),
                ('TOID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Toid', to='My_app.login_table')),
            ],
        ),
    ]
