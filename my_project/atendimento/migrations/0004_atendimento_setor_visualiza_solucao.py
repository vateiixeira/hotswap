# Generated by Django 2.2.7 on 2020-11-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0003_auto_20200617_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='setor_visualiza_solucao',
            field=models.BooleanField(default=True, verbose_name='Setores podem ver soluçao'),
        ),
    ]