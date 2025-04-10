# Generated by Django 5.1.5 on 2025-03-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_user_bookmarks'),
        ('articles', '0014_rename_bookmarks_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='bookmarked_by',
            field=models.ManyToManyField(through='articles.Bookmark', to='accounts.user'),
        ),
    ]
