# Generated by Django 2.2 on 2019-05-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0030_glossary_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='image',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]