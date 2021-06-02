# Generated by Django 3.2.3 on 2021-06-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_rename_brewing_temperatue_recipes_brewing_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tea_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'teas',
            },
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ('-is_favourite', 'recipe_name')},
        ),
        migrations.AlterField(
            model_name='recipes',
            name='brewing_temperature',
            field=models.FloatField(default=80),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='brewing_time',
            field=models.FloatField(default=60),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='mixing_time',
            field=models.FloatField(default=15),
        ),
    ]
