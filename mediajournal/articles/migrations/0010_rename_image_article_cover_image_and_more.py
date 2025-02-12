# Generated by Django 5.1.5 on 2025-02-10 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_alter_article_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='image',
            new_name='cover_image',
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('Moderation', 'Moderation'), ('Rejected', 'Rejected'), ('Published', 'Published')], default='Moderation', max_length=20),
        ),
    ]
