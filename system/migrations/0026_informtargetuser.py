# Generated by Django 2.0.5 on 2018-07-13 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0025_sysparaforseller'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformTargetUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.CharField(max_length=500, null=True, verbose_name='备注')),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatetime', models.DateTimeField(null=True, verbose_name='最后修改时间')),
                ('deletetime', models.DateTimeField(null=True, verbose_name='删除时间')),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_adder', to='system.User', verbose_name='添加人（user.id）')),
                ('deleter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_deleter', to='system.User', verbose_name='删除人')),
                ('informTypeId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_informTypeId', to='system.InformType', verbose_name='通知消息标志ID（informType.id）')),
                ('sellersId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_sellersId', to='system.Seller', verbose_name='商家ID')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_updater', to='system.User', verbose_name='最后修改人（user.id）')),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='informTargetUser_userId', to='system.User', verbose_name='接收消息的用户ID')),
            ],
        ),
    ]
