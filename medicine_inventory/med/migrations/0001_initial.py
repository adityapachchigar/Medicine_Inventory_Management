# Generated by Django 4.1 on 2023-11-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doses', models.CharField(choices=[('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Liquid', 'Liquid'), ('Injection', 'Injection')], max_length=10)),
                ('med_name', models.CharField(max_length=30)),
                ('quantity', models.IntegerField()),
                ('mrp', models.IntegerField()),
                ('batch_no', models.CharField(max_length=10)),
                ('expiry_date', models.DateField()),
            ],
        ),
    ]