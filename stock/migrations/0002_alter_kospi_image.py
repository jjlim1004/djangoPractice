# Generated by Django 3.2.3 on 2021-05-20 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kospi',
            name='image',
            field=models.ImageField(default='/static/img/kospi.png', upload_to=''),
        ),
    ]