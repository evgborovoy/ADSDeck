# Generated by Django 4.2.9 on 2024-02-01 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_location_alter_ads_options_remove_ads_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
    ]
