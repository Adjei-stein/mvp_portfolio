# Generated by Django 3.0.8 on 2021-08-18 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210818_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customization',
            name='customization',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]