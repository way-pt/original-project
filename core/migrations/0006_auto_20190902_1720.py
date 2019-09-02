# Generated by Django 2.2.5 on 2019-09-02 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190901_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='name',
            field=models.CharField(blank=True, help_text='A name for the map.', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='data',
            field=models.FileField(upload_to='dataFiles'),
        ),
        migrations.AlterField(
            model_name='map',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos'),
        ),
    ]
