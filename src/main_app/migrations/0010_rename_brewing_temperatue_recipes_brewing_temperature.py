# Generated by Django 3.2.3 on 2021-06-01 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_recipes_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipes',
            old_name='brewing_temperatue',
            new_name='brewing_temperature',
        ),
    ]