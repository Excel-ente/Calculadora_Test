# Generated by Django 4.2.2 on 2023-08-27 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_alter_compra_articulos_alter_compra_proveedor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumoscompra',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.compra_insumo'),
        ),
    ]