# Generated by Django 4.2.4 on 2023-08-13 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketapp', '0003_envase_producto_envase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direccionenvio',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='direccion_envio',
        ),
        migrations.AddField(
            model_name='orden',
            name='apellido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='direccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketapp.direccionenvio'),
        ),
        migrations.AddField(
            model_name='orden',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='telefono',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketapp.direccionenvio'),
        ),
    ]
