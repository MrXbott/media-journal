# Generated by Django 5.1.5 on 2025-01-31 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_article_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='photo',
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category-images/'),
        ),
    ]
