# Generated by Django 2.2 on 2019-04-14 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20190414_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='label',
            field=models.ManyToManyField(blank=True, to='topics.Label'),
        ),
    ]
