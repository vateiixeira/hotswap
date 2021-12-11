# Generated by Django 2.2.7 on 2021-05-17 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_configuracaoemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cargo',
            field=models.CharField(blank=True, choices=[('gerencia_ti', 'Gerência TI'), ('tecnico', 'Técnico')], max_length=20, null=True, verbose_name='Área de atuacao'),
        ),
    ]
