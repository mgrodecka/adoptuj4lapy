# Generated by Django 2.2.2 on 2019-07-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adoptuj', '0002_animal_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='breed',
            field=models.CharField(default='x', max_length=64),
            preserve_default=False,
        ),
    ]
