# Generated by Django 2.2 on 2019-04-29 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0023_auto_20190429_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='course',
            name='sectionorder',
        ),
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]