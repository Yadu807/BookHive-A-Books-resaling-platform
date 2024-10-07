# Generated by Django 5.1 on 2024-10-03 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='login_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField()),
                ('photo', models.FileField(upload_to='')),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.login_table')),
            ],
        ),
        migrations.CreateModel(
            name='book_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tittle', models.CharField(max_length=100)),
                ('Author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100)),
                ('price', models.BigIntegerField()),
                ('photo', models.FileField(upload_to='')),
                ('status', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.category_table')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.user_table')),
            ],
        ),
    ]
