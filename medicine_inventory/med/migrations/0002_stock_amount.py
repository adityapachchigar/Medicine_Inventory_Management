# Generated by Django 4.1 on 2023-11-18 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
