# Generated by Django 3.0.8 on 2021-08-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210818_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customization',
            name='order',
        ),
        migrations.RemoveField(
            model_name='customization',
            name='product',
        ),
        migrations.AddField(
            model_name='customization',
            name='productname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
