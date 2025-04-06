# Generated by Django 5.1.5 on 2025-04-06 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0012_user_bio'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('object_id', models.PositiveBigIntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='accounts.user')),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('article', 'news')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answers', to='comments.comment')),
            ],
            options={
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='comments_co_content_cff8bd_idx')],
            },
        ),
    ]
