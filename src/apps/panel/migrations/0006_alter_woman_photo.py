# Generated by Django 4.2.7 on 2023-11-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_woman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woman',
            name='photo',
            field=models.ImageField(unique=True, upload_to='woman/%Y/%m/%d'),
        ),
    ]
