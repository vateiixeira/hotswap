# Generated by Django 2.2.7 on 2021-05-17 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210517_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaoemail',
            name='send_novos_atendimentos',
            field=models.BooleanField(blank=True, default=True, verbose_name='Envia e-mail de novos atendimentos ?'),
        ),
    ]
