# Generated by Django 2.2.7 on 2021-12-11 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('envios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recebimento',
            name='envio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recebimento', to='envios.EnvioBh'),
        ),
    ]