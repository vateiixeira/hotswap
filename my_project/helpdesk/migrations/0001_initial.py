# Generated by Django 2.2.7 on 2020-06-17 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(choices=[('FRENTE CAIXA', 'Frente de caixa'), ('RECEPCAO', 'Recepção'), ('SALAO', 'Salao'), ('PERECIVEIS', 'Perecíveis'), ('GERENCIA', 'Gerência'), ('TESOURARIA', 'Tesouraria'), ('SEGURANCA', 'Segurança'), ('RM', 'Rm'), ('RM FISCAL', 'Rm Fiscal'), ('CONTABILIDADE', 'Contabilidade'), ('RH', 'Rh'), ('ACOUGUE', 'Açougue'), ('TREINAMENTO', 'Treinamento'), ('SOE', 'Soe'), ('ALMOXARIFADO', 'Almoxarifado'), ('CPD', 'CPD'), ('CALLCENTER', 'Callcenter'), ('COMERCIAL', 'Comercial'), ('PRECIFICACAO', 'Precificação'), ('PADARIA', 'Padaria'), ('MANUTENCAO', 'Manutenção'), ('HORTIFRUTI', 'Hortifruti'), ('CREDITO', 'Crédito'), ('ENCARREGADOS', 'Encarregados'), ('ALMOXARIFADO', 'Almoxarifado'), ('RESTAURANTE', 'Restaurante'), ('SND', 'SND'), ('GERAL', 'Geral'), ('POSTO-PISTA', 'Posto-Pista'), ('POSTO-ADM', 'Posto-Adm'), ('LOGISTICA', 'Logistica'), ('EXPEDICAO', 'Expedição'), ('PRESIDENCIA', 'Presidência')], max_length=50, verbose_name='Setor')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Lojas', verbose_name='Filial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuários',
            },
        ),
    ]
