# Generated by Django 4.1.6 on 2023-03-19 09:10

from django.db import migrations
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0014_alter_post_userlikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='c',
            field=tinymce.models.HTMLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]