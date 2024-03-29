# Generated by Django 2.2.7 on 2021-05-18 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210518_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracaoemail',
            name='send_atendimentos_mensais',
            field=models.BooleanField(blank=True, default=True, verbose_name='Envia e-mail de atendimentos presas ?'),
        ),
        migrations.AlterField(
            model_name='configuracaoemail',
            name='send_chamados_mensais',
            field=models.BooleanField(blank=True, default=True, verbose_name='Envia e-mail de chamados presas ?'),
        ),
    ]
