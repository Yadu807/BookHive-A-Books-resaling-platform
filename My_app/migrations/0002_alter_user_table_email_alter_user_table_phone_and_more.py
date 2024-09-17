# Generated by Django 5.1 on 2024-08-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_table',
            name='email',
            field=models.EmailField(default=0, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_table',
            name='phone',
            field=models.BigIntegerField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_table',
            name='photo',
            field=models.FileField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]