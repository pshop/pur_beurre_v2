# Generated by Django 2.1 on 2018-09-06 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20180906_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='summation',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]