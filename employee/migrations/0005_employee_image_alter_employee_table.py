# Generated by Django 4.2.7 on 2023-11-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employee_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(null=True, upload_to='employee/'),
        ),
        migrations.AlterModelTable(
            name='employee',
            table='employee',
        ),
    ]
