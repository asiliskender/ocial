# Generated by Django 2.2 on 2019-04-13 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_auto_20190413_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
