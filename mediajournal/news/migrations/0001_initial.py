# Generated by Django 5.1.5 on 2025-04-16 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('text', models.TextField()),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Moderation', 'Moderation'), ('Published', 'Published'), ('Rejected', 'Rejected')], default='Moderation', max_length=20)),
                ('cover', models.ImageField(blank=True, default='default/default_news_cover.jpg', null=True, upload_to='images/')),
                ('enable_comments', models.BooleanField(default=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='accounts.user')),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
    ]
