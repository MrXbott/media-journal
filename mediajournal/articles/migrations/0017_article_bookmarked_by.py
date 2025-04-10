# Generated by Django 5.1.5 on 2025-03-13 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_user_bookmarks'),
        ('articles', '0016_remove_article_bookmarked_by_delete_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='bookmarked_by',
            field=models.ManyToManyField(related_name='bookmarks', to='accounts.user'),
        ),
    ]
