# Generated by Django 5.1.5 on 2025-04-06 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0031_articlesection_quote_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='body',
            new_name='text',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
