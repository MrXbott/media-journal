# Generated by Django 5.1.5 on 2025-04-08 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0032_rename_body_article_text_delete_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='cover_image',
            new_name='cover',
        ),
    ]
