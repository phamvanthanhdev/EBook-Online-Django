# Generated by Django 2.2 on 2023-09-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
