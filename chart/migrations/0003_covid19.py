# Generated by Django 3.0.3 on 2020-06-26 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_auto_popuate'),
    ]

    operations = [
        migrations.CreateModel(
            name='covid19',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('france', models.FloatField()),
                ('germany', models.FloatField()),
                ('korea', models.FloatField()),
                ('us', models.FloatField()),
                ('uk', models.FloatField()),
            ],
        ),
    ]
