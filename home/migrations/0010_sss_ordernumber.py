# Generated by Django 3.0.8 on 2020-08-13 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_sss_ordernumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='sss',
            name='ordernumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
