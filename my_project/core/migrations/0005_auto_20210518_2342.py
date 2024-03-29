# Generated by Django 2.2.7 on 2021-05-19 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210518_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracaoemail',
            name='send_atendimentos_mensais',
            field=models.BooleanField(blank=True, default=True, verbose_name='Envia e-mail de atendimentos mensais ?'),
        ),
        migrations.AlterField(
            model_name='configuracaoemail',
            name='send_chamados_mensais',
            field=models.BooleanField(blank=True, default=True, verbose_name='Envia e-mail de chamados mensais ?'),
        ),
    ]
