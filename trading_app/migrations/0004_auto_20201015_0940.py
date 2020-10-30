# Generated by Django 3.1.2 on 2020-10-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0003_auto_20201013_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='demanded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='offer',
            name='order_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'market'), (2, 'limit'), (3, 'stop_loss')]),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trade_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'market'), (2, 'limit'), (3, 'stop_loss')]),
        ),
    ]