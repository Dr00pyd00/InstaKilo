# Generated by Django 5.1.7 on 2025-03-16 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='create_at',
            new_name='create_date',
        ),
    ]
