# Generated by Django 4.2.7 on 2023-11-04 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_article_href_alter_article_src_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
    ]
