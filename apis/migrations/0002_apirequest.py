# Generated by Django 5.1 on 2024-09-18 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=10000)),
                ('nchars', models.IntegerField()),
                ('nwords', models.IntegerField()),
                ('output', models.CharField(blank=True, max_length=10000)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.apikey')),
            ],
        ),
    ]
