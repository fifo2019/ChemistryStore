# Generated by Django 2.2 on 2019-07-19 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('STP', 'отправлен в обработку'), ('RDY', 'готов к выдаче'), ('CNC', 'отменен')], default='STP', max_length=3, verbose_name='статус'),
        ),
    ]
