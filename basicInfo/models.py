from django.db import models
from system import models as systemModels

# Create your models here.

#绑定商家
class BindSeller(models.Model):
    sellerId = models.ForeignKey(systemModels.Seller, related_name="bindSeller_sellerId", on_delete=models.SET_NULL,
                                 verbose_name='商家', null=True, help_text='')
    bindSellerId = models.ForeignKey(systemModels.Seller, related_name="bindSeller_bindSellerId", on_delete=models.SET_NULL,
                                     verbose_name='被绑定的商家', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(systemModels.User, related_name="bindSeller_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(systemModels.User, related_name="bindSeller_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(systemModels.User, related_name="bindSeller_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')

#品牌
class Probrand(models.Model):
    c_name = models.CharField(verbose_name='中文名', max_length=50, help_text='')
    e_name = models.CharField(verbose_name='音文名', max_length=50, help_text='')
    name_head = models.CharField(verbose_name='拼音音头',max_length = 10, help_text = '')
    from_country = models.CharField(verbose_name='所属国家', max_length=50, help_text='')
    info = models.CharField(verbose_name='说明', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(systemModels.User, related_name="probrand_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(systemModels.User, related_name="probrand_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(systemModels.User, related_name="probrand_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')

#商品类目
class DicWareclass(models.Model):
    parentId = models.IntegerField(verbose_name='父类ID', null=True, help_text='')
    SellerId = models.ForeignKey(systemModels.Seller, related_name="dicWareclass_SellerId", on_delete=models.SET_NULL,
                                 verbose_name='所属商家（sellers.id）永远为0', null=True, help_text='')
    name = models.CharField(verbose_name='类目名称', max_length=50, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(systemModels.User, related_name="dicWareclass_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(systemModels.User, related_name="dicWareclass_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(systemModels.User, related_name="dicWareclass_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人', null=True, help_text='')

#区域维护
class DicArea(models.Model):
    parentId = models.IntegerField(verbose_name='父类ID', null=True, help_text='')
    SellerId = models.ForeignKey(systemModels.Seller, related_name="dicArea_SellerId", on_delete=models.SET_NULL,                               verbose_name='所属商家（sellers.id）永远为0', null=True, help_text='')
    name = models.CharField(verbose_name='类目名称', max_length=50, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(systemModels.User, related_name="dicArea_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(systemModels.User, related_name="dicArea_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(systemModels.User, related_name="dicArea_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class Ware(models.Model):
    wareClass = models.CharField(verbose_name='商品类别', max_length=50, null=True, help_text='')
    brandid = models.ForeignKey(Probrand, related_name="ware_brandid", on_delete=models.SET_NULL, verbose_name='品牌',
                                null=True, help_text='')
    name = models.CharField(verbose_name='商品名称', max_length=200, help_text='')
    abbreviation = models.CharField(verbose_name='产品简介', max_length=200, help_text='')
    nameE = models.CharField(verbose_name='英文名字', max_length=50, null=True, help_text='')
    sn = models.CharField(verbose_name='内码', max_length=10, help_text='')
    wareNo = models.CharField(verbose_name='货号', max_length=50, null=True, help_text='')
    warePOO = models.CharField(verbose_name='商品产地', max_length=50, null=True, help_text='')
    ifAccessory = models.CharField(verbose_name='是否为配件', max_length=1, null=True, help_text='')
    ifIndependentSend = models.CharField(verbose_name='是否独立包装发货', max_length=1, null=True, help_text='')
    ifSendScan = models.CharField(verbose_name='是否发货扫描', max_length=1, null=True, help_text='')
    grossWeight = models.IntegerField(verbose_name='毛重', null=True, help_text='')
    netWeight = models.IntegerField(verbose_name='净重', null=True, help_text='')
    length = models.IntegerField(verbose_name='长', null=True, help_text='')
    width = models.IntegerField(verbose_name='宽', null=True, help_text='')
    height = models.IntegerField(verbose_name='高', null=True, help_text='')
    lengthOut = models.IntegerField(verbose_name='外箱长', null=True, help_text='')
    widthOut = models.IntegerField(verbose_name='外箱宽', null=True, help_text='')
    heightOut = models.IntegerField(verbose_name='外箱高', null=True, help_text='')
    scription = models.CharField(verbose_name='商品描述', max_length=500, null=True, help_text='')
    extendPropIdList = models.CharField(verbose_name='', max_length=500, null=True, help_text='')
    extendPropNameList = models.CharField(verbose_name='', max_length=500, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(systemModels.User, related_name="ware_adder", on_delete=models.SET_NULL, verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(systemModels.User, related_name="ware_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(systemModels.User, related_name="ware_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')