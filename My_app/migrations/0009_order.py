# Generated by Django 5.1 on 2024-10-13 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0008_searchkeyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderDate', models.DateField(auto_now_add=True)),
                ('Status', models.CharField(default='Requested', max_length=100)),
                ('BookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.book_table')),
                ('BuyerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.user_table')),
            ],
        ),
    ]