# Generated by Django 5.1 on 2024-09-08 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0005_remove_user_table_username'),
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
        migrations.AlterField(
            model_name='login_table',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='login_table',
            name='type',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='login_table',
            name='username',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user_table',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user_table',
            name='place',
            field=models.CharField(max_length=100),
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
                ('description', models.CharField(max_length=100)),
                ('photo', models.FileField(upload_to='')),
                ('status', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.user_table')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='My_app.category_table')),
            ],
        ),
    ]
