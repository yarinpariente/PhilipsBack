# Generated by Django 4.2 on 2023-05-15 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0013_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]