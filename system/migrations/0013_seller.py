# Generated by Django 2.0.5 on 2018-06-28 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_auto_20180628_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerName', models.CharField(max_length=200, null=True, verbose_name='商家名称')),
                ('uniqueCode', models.CharField(max_length=50, null=True, verbose_name='商家识别唯一编码（可打印条形码二维码）')),
                ('sellerAddress', models.CharField(max_length=500, null=True, verbose_name='商家地址')),
                ('sellerLinkman', models.CharField(max_length=50, null=True, verbose_name='商家联系人')),
                ('sellerTel', models.CharField(max_length=50, null=True, verbose_name='商家电话')),
                ('employeeSnGType', models.CharField(help_text='{"data":[{"id": "auto", "text": "自动[从1001开始]"}, {"id": "radom", "text": "4位随机"}, {"id": "input", "text": "输入"}]', max_length=50, null=True, verbose_name='员工编号生成方式')),
                ('sellerType', models.CharField(help_text='{"data":[{"id": "1", "text": "商家"}, {"id": "2", "text": "供应商"}]', max_length=10, null=True, verbose_name='商家类型')),
                ('status', models.CharField(help_text='{"data":[{"id": "T", "text": "有效"}, {"id": "F", "text": "无效"}]', max_length=1, null=True, verbose_name='状态')),
                ('memo', models.CharField(max_length=500, null=True, verbose_name='备注')),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatetime', models.DateTimeField(null=True, verbose_name='最后修改时间')),
                ('deletetime', models.DateTimeField(null=True, verbose_name='删除时间')),
                ('adder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_adder', to='system.User', verbose_name='添加人（users.id）')),
                ('deleter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_deleter', to='system.User', verbose_name='删除人')),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_updater', to='system.User', verbose_name='最后修改人（users.id）')),
                ('usersId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_usersId', to='system.User', verbose_name='关联系统用户名')),
            ],
        ),
    ]
