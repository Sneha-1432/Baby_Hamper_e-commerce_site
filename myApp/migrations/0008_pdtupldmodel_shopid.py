# Generated by Django 4.1.5 on 2023-02-21 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_cardpaydetailsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdtupldmodel',
            name='shopid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]