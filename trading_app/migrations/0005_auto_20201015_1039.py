# Generated by Django 3.1.2 on 2020-10-15 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0004_auto_20201015_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer', to='trading_app.item'),
        ),
    ]
