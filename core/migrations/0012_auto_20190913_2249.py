# Generated by Django 2.2.5 on 2019-09-14 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190910_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True),
        ),
    ]
