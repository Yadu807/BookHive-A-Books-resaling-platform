# Generated by Django 5.1 on 2024-10-21 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0010_order_amount_order_nstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p', to='My_app.user_table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l', to='My_app.user_table')),
            ],
        ),
    ]
