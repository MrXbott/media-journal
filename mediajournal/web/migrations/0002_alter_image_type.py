# Generated by Django 5.1.5 on 2025-02-08 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='type',
            field=models.CharField(choices=[('default_user_photo', 'Default User Photo')], max_length=20),
        ),
    ]
