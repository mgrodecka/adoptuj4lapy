# Generated by Django 2.2.2 on 2019-07-22 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('type', models.IntegerField(choices=[(1, 'dog'), (2, 'cat')])),
                ('sex', models.IntegerField(choices=[(1, 'M'), (2, 'F'), (3, 'unknown')])),
                ('age', models.CharField(max_length=64)),
                ('age_years', models.IntegerField()),
                ('color', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('vaccination', models.BooleanField(default=False)),
                ('deworming', models.BooleanField(default=False)),
                ('sterilization', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=64)),
                ('shelter', models.CharField(max_length=64)),
                ('shelter_group', models.IntegerField(choices=[(1, 'Warszawa'), (2, 'Kraków'), (3, 'Wrocław'), (4, 'Trójmiasto'), (5, 'Poznań'), (6, 'Łódź'), (7, 'Katowice'), (8, 'Lublin')])),
                ('address', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('image', models.CharField(max_length=256)),
                ('virtual_adoption', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(1, 'czeka na adopcje'), (2, 'zaadoptowany'), (3, 'za tęczowym mostem')])),
                ('trained', models.BooleanField(default=False)),
                ('accept_dogs', models.BooleanField(default=False)),
                ('accept_cats', models.BooleanField(default=False)),
                ('accept_children', models.BooleanField(default=False)),
                ('added_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
