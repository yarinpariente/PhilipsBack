# Generated by Django 4.1.3 on 2023-03-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0005_alter_item_machine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='room_description',
            field=models.CharField(max_length=100),
        ),
    ]
