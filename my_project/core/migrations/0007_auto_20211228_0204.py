# Generated by Django 2.2.7 on 2021-12-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_notassocin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuracaoemail',
            options={'verbose_name': 'Configuração de e-mail/Telegram', 'verbose_name_plural': 'Configurações de e-mails/Telegram'},
        ),
        migrations.AddField(
            model_name='configuracaoemail',
            name='telegram_notas_presas',
            field=models.BooleanField(blank=True, default=True, verbose_name='Habilita envio de notas presas telegram'),
        ),
    ]
