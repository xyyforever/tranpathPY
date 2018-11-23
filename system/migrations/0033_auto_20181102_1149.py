# Generated by Django 2.1.2 on 2018-11-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0032_userpara'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpara',
            name='adder',
        ),
        migrations.RemoveField(
            model_name='userpara',
            name='addtime',
        ),
        migrations.RemoveField(
            model_name='userpara',
            name='deleter',
        ),
        migrations.RemoveField(
            model_name='userpara',
            name='deletetime',
        ),
        migrations.RemoveField(
            model_name='userpara',
            name='updater',
        ),
        migrations.RemoveField(
            model_name='userpara',
            name='updatetime',
        ),
        migrations.AlterField(
            model_name='userpara',
            name='sysparaId',
            field=models.IntegerField(null=True, verbose_name='参数ID（para.id）'),
        ),
        migrations.AlterField(
            model_name='userpara',
            name='userId',
            field=models.IntegerField(null=True, verbose_name='用户ID（user.id）'),
        ),
    ]
