# Generated by Django 4.2 on 2023-04-21 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0005_alter_item_column_alter_item_row_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.CharField(blank=True, max_length=1000000, null=True),
        ),
    ]
