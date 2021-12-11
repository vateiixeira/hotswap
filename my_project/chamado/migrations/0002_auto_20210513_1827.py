# Generated by Django 2.2.7 on 2021-05-13 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210510_2354'),
        ('chamado', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='fornecedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chamado', to='core.Fornecedor'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='justificativa',
            field=models.TextField(blank=True, null=True, verbose_name='Justificativa do chamado'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='nfe',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Nota Fiscal'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='status',
            field=models.CharField(choices=[('corretivo', 'Corretivo'), ('mau-uso', 'Mau uso'), ('aquisicao', 'Aquisição'), ('pendente', 'Pendente')], default='pendente', max_length=60),
        ),
    ]