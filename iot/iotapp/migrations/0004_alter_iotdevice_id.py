# Generated by Django 3.2.5 on 2022-04-10 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotapp', '0003_auto_20220409_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iotdevice',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]