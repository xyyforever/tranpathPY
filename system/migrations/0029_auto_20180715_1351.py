# Generated by Django 2.0.5 on 2018-07-15 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0028_informtargetdept'),
    ]

    operations = [
        migrations.RenameField(
            model_name='informtargetuser',
            old_name='sellersId',
            new_name='sellerId',
        ),
    ]
