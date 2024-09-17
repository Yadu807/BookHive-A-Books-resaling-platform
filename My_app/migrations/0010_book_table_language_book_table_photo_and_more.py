# Generated by Django 5.1 on 2024-09-15 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0009_remove_book_table_language_remove_book_table_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_table',
            name='language',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book_table',
            name='photo',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book_table',
            name='status',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book_table',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='My_app.user_table'),
            preserve_default=False,
        ),
    ]