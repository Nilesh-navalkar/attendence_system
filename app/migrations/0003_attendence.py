# Generated by Django 4.1.2 on 2023-03-01 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_pp'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sap', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
