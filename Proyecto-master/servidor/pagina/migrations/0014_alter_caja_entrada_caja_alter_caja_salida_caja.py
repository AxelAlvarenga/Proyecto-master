# Generated by Django 4.0.2 on 2022-02-24 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0013_alter_caja_fecha_caja_alter_caja_hora_caja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='entrada_caja',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='salida_caja',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
    ]
