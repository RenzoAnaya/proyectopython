# Generated by Django 4.2.4 on 2023-08-16 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketapp', '0002_alter_usuario_direccion_alter_usuario_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='apellido',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='orden',
            old_name='nombre',
            new_name='last_name',
        ),
    ]
