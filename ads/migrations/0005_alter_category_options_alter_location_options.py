# Generated by Django 4.2.9 on 2024-02-01 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['name'], 'verbose_name': 'Место', 'verbose_name_plural': 'Места'},
        ),
    ]