# Generated by Django 5.1 on 2024-09-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_app', '0008_user_table_username_alter_user_table_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book_table',
            name='language',
        ),
        migrations.RemoveField(
            model_name='book_table',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='book_table',
            name='status',
        ),
        migrations.RemoveField(
            model_name='book_table',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='user_table',
            name='username',
        ),
        migrations.AlterField(
            model_name='user_table',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
