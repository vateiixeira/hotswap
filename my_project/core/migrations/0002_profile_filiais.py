# Generated by Django 2.2.7 on 2021-05-11 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='filiais',
            field=models.ManyToManyField(blank=True, to='core.Lojas'),
        ),
    ]