# Generated by Django 2.1.2 on 2018-11-06 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0034_auto_20181102_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role_dic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_id', models.IntegerField(null=True, verbose_name='用户ID（role.id）')),
                ('dic_id', models.IntegerField(null=True, verbose_name='字典ID(dic_id)')),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatetime', models.DateTimeField(null=True, verbose_name='最后修改时间')),
                ('deletetime', models.DateTimeField(null=True, verbose_name='删除时间')),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_dic_adder', to='system.User', verbose_name='添加人（user.id）')),
                ('deleter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_dic_deleter', to='system.User', verbose_name='删除人')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_dic_updater', to='system.User', verbose_name='最后修改人（user.id）')),
            ],
        ),
        migrations.CreateModel(
            name='RolePara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roleId', models.IntegerField(null=True, verbose_name='用户ID（role.id）')),
                ('sysparaId', models.IntegerField(null=True, verbose_name='参数ID（para.id）')),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatetime', models.DateTimeField(null=True, verbose_name='最后修改时间')),
                ('deletetime', models.DateTimeField(null=True, verbose_name='删除时间')),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rolePara_adder', to='system.User', verbose_name='添加人（user.id）')),
                ('deleter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rolePara_deleter', to='system.User', verbose_name='删除人')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rolePara_updater', to='system.User', verbose_name='最后修改人（user.id）')),
            ],
        ),
        migrations.CreateModel(
            name='User_dic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True, verbose_name='用户ID（user.id）')),
                ('dic_id', models.IntegerField(null=True, verbose_name='字典ID(dic_id)')),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatetime', models.DateTimeField(null=True, verbose_name='最后修改时间')),
                ('deletetime', models.DateTimeField(null=True, verbose_name='删除时间')),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_dic_adder', to='system.User', verbose_name='添加人（user.id）')),
                ('deleter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_dic_deleter', to='system.User', verbose_name='删除人')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_dic_updater', to='system.User', verbose_name='最后修改人（user.id）')),
            ],
        ),
    ]
