# Generated by Django 2.2.5 on 2019-09-29 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190928_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='uid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userauthorize',
            name='uid',
            field=models.IntegerField(),
        ),
    ]
