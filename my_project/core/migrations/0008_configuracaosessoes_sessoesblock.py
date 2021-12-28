# Generated by Django 2.2.7 on 2021-12-28 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20211228_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoSessoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habilita_monitoramento', models.BooleanField(blank=True, default=True, verbose_name='Habilita monitoramento no banco?')),
                ('habilita_telegram', models.BooleanField(blank=True, default=True, verbose_name='Habilita envio de avisos telegram?')),
                ('minutos', models.IntegerField(blank=True, default=5, verbose_name='Minutos a considerar sessao travada p/ ativar avisos')),
            ],
            options={
                'verbose_name': 'Configuração de sessoes',
                'verbose_name_plural': 'Configuração de sessoes',
            },
        ),
        migrations.CreateModel(
            name='SessoesBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.IntegerField(blank=True, default=0, verbose_name='ID da sessao')),
                ('usuario', models.CharField(blank=True, default='', max_length=128, verbose_name='Usuário')),
                ('terminal', models.CharField(blank=True, default='', max_length=128, verbose_name='Terminal')),
                ('maquina', models.CharField(blank=True, default='', max_length=128, verbose_name='Maquina')),
                ('programa', models.CharField(blank=True, default='', max_length=128, verbose_name='Programa')),
                ('os_username', models.CharField(blank=True, default='', max_length=128, verbose_name='Usuário SO')),
                ('sessao_bloqueada', models.IntegerField(blank=True, default=0, verbose_name='Sessao bloqueada')),
                ('data', models.DateTimeField(blank=True, null=True, verbose_name='Ocorrencia')),
            ],
            options={
                'verbose_name': 'Sessoes bloqueadas',
                'verbose_name_plural': 'Sessoes bloqueadas',
            },
        ),
    ]
