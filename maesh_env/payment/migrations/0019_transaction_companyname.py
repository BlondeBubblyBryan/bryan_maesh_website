# Generated by Django 2.2.2 on 2019-08-07 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_auto_20190805_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='companyName',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]