# Generated by Django 2.2.7 on 2021-05-13 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210510_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='garantia',
            field=models.IntegerField(default=90, verbose_name='Dias de garantia'),
        ),
    ]
