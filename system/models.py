from django.db import models
from datetime import datetime


# Create your models here.

class User(models.Model):
    grade = models.IntegerField(verbose_name='等级', null=True,
                                help_text='{"form":"T","require":"T","title":"","eleType":"select","data":[{"id":"3","value":"系统级"},{"id":"2","value":"商家级"},{"id":"1","value":"客服级"}]}')
    sellerId = models.IntegerField(verbose_name='商家ID', null=True, default=0, db_index=True, help_text='{"form":"F"}')
    parentSellerId = models.IntegerField(verbose_name='所属商家ID', null=True, default=0, help_text='{"form":"F"}')
    name = models.CharField(verbose_name='姓名', max_length=100, null=True,
                            help_text='{"form":"T","require":"T","title":"","eleType":"text"}')
    username = models.CharField(verbose_name='用户名', max_length=50, null=True,
                                help_text='{"form":"T","require":"T","title":"","eleType":"text"}')
    password = models.CharField(verbose_name='密码', max_length=50, null=True,
                                help_text='{"form":"T","require":"T","title":"","eleType":"password"}')
    menuIdList = models.CharField(verbose_name='菜单权限列表', max_length=4000, null=True, help_text='{"form":"F"}')
    status = models.CharField(verbose_name='状态', max_length=1,
                              help_text='{"form":"T","require":"T","title":"","eleType":"select","data":[{"id":"T","value":"有效"},{"id":"F","value":"无效"}]}')
    memo = models.CharField(verbose_name='备注', max_length=4000, null=True,
                            help_text='{"form":"T","require":"F","title":"","eleType":"textarea"}')
    uniqueCode = models.CharField(verbose_name='唯一编码', max_length=4000, null=True, help_text='{"form":"F"}')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='{"form":"F"}')
    adder = models.IntegerField(verbose_name='添加人（User.id）', default=0, help_text='{"form":"F"}')
    updatetime = models.DateTimeField(verbose_name='最后更新时间', null=True, help_text='{"form":"F"}')
    updater = models.IntegerField(verbose_name='最后更新操作人（User.id）', default=0, help_text='{"form":"F"}')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='{"form":"F"}')
    deleter = models.IntegerField(verbose_name='删除操作人（User.id）', default=0, help_text='{"form":"F"}')

    @property
    def paras(self):
        '''用户的所有单值参数'''
        relations = UserPara.objects.filter(userId=self.id).filter(deletetime=None).only('sysparaId')
        sysparaIds = [r.sysparaId for r in relations]
        return Syspara.objects.filter(id__in=sysparaIds)

    @property
    def dic_list(self):
        '''用户所有的字典参数'''
        relations = User_dic.objects.filter(user_id=self.id).filter(deletetime=None).only('dicMainListId')
        dicMainListIds = [r.dic_id for r in relations]
        return DicMainListForSelect.objects.filter(dicMainListId__in=dicMainListIds)
    

class Excel_import_file_main(models.Model):
    filenameOriginal = models.CharField(verbose_name='原始文件名', max_length=500,
                                        help_text='{"form":"T","require":"T","title":"选择文件","eleType":"file","data":"xls,xlsx"}')
    filenameSaved = models.CharField(verbose_name='保存文件名', max_length=500, help_text='{"form":"F"}')
    tableName = models.CharField(verbose_name='生成的表名（以temp开头）', max_length=200,
                                 help_text='{"form":"T","require":"T","title":"生成的表名"}')
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True, help_text='{"form":"F"}')
    adder = models.ForeignKey(User, related_name="excel_import_file_main_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（User.id）', null=True, help_text='{"form":"F"}')
    setFieldNameTime = models.DateTimeField(verbose_name='设置字段名时间', null=True, help_text='{"form":"F"}')
    setFieldNamer = models.ForeignKey(User, related_name="setFieldNamer", on_delete=models.SET_NULL,
                                      verbose_name='设置字段名时间操作人（User.id）', null=True, help_text='{"form":"F"}')
    importTime = models.DateTimeField(verbose_name='设置字段名时间', null=True, help_text='{"form":"F"}')
    importer = models.ForeignKey(User, related_name='importer', on_delete=models.SET_NULL,
                                 verbose_name='设置字段名时间操作人（User.id）', null=True, help_text='{"form":"F"}')


class Excel_import_file_fields_name(models.Model):
    excelImportFileMainId = models.ForeignKey(Excel_import_file_main, related_name='excel_import_file_main_id',
                                              on_delete=models.SET_NULL, verbose_name='导入文件主表ID', null=True,
                                              help_text='{"form":"F"}')
    fieldSn = models.IntegerField(verbose_name='字段序号', default=0, help_text='{"form":"F"}')
    fieldNameOriginal = models.CharField(verbose_name='原始字段名', max_length=500, help_text='{"form":"F"}')
    fieldNameNew = models.CharField(verbose_name='新字段名(为空时该字段不导入系统)', max_length=500, help_text='{"form":"F"}')
    colType = models.CharField(verbose_name='段名类型（从excel判断 ）', null=True, max_length=50, help_text='{"form":"F"}')
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True, help_text='{"form":"F"}')
    adder = models.ForeignKey(User, related_name="excel_import_file_fields_name_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（User.id）', null=True, help_text='{"form":"F"}')


class Menu(models.Model):
    name = models.CharField(verbose_name='菜单显示名称', max_length=50, null=True, help_text='')
    grade = models.IntegerField(verbose_name='等级（3：系统级；2：商家级；1：客服级）', null=True,
                                help_text='{"data":[{"id": "3", "text": "系统级"}, {"id": "2", "text": "商家级"}, {"id": "1", "text": "客服级"}]')
    parentId = models.IntegerField(verbose_name='父菜单级别ID(0:顶级菜单)', null=True, help_text='')
    linkfile = models.CharField(verbose_name='链接URL', max_length=100, null=True, help_text='')
    paras = models.CharField(verbose_name='参数', max_length=255, null=True, help_text='')
    target = models.CharField(verbose_name='链接打开位置', max_length=50, null=True, help_text='')
    iconShow = models.CharField(verbose_name='图标类名', max_length=50, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=4000, null=True, help_text='')
    ifshow = models.CharField(verbose_name='是否显示（T：显示；F：隐藏）', max_length=1, null=True,
                              help_text='{"data":[{"id": "T", "text": "显示"}, {"id": "F", "text": "隐藏"}]')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="menu_adder", on_delete=models.SET_NULL, verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="menu_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="menu_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人（user.id）', null=True, help_text='')


class Purview(models.Model):
    purname = models.CharField(verbose_name='权限名称', max_length=50, null=True, help_text='')
    grade = models.IntegerField(verbose_name='等级（3：系统级；2：商家级；1：客服级）', null=True,
                                help_text='{"data":[{"id": "3", "text": "系统级"}, {"id": "2", "text": "商家级"}, {"id": "1", "text": "客服级"}]')
    purcode = models.CharField(verbose_name='权限代码', max_length=50, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="purview_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="purview_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="purview_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人（user.id）', null=True, help_text='')


class Syspara(models.Model):
    paraType = models.CharField(verbose_name='参数类型（系统;商家）', max_length=50, null=True,
                                help_text='{"data":[{"id": "系统", "text": "系统"}, {"id": "商家", "text": "商家"}]')
    paraShow = models.CharField(verbose_name='参数名称', max_length=200, null=True, help_text='')
    paraTag = models.CharField(verbose_name='参数标志（用于调用）', max_length=50, null=True, help_text='')
    paraValue = models.CharField(verbose_name='参数值', max_length=200, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="syspara_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="syspara_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="syspara_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人（user.id）', null=True, help_text='')

    @property
    def users(self):
        '''单值参数对应的用户'''
        relations = UserPara.objects.filter(sysparaId=self.id).only('userId')
        user_ids = [r.userId for r in relations]
        return User.objects.filter(id__in=user_ids)

    @property
    def roles(self):
        """单值参数对应的角色"""
        relations = RolePara.objects.filter(sysparaId=self.id).only('roleId')
        role_ids = [r.roleId for r in relations]
        return Role.objects.filter(id__in=role_ids)


class DicMainList(models.Model):
    keywords = models.CharField(verbose_name='相关关键字', max_length=500, null=True, help_text='')
    dicName = models.CharField(verbose_name='字典名称', max_length=50, null=True, help_text='')
    dicTag = models.CharField(verbose_name='字典标志', max_length=50, null=True, help_text='')
    allowSellerOp = models.CharField(verbose_name='是否允许商家维护可选项', max_length=1, null=True,
                                     help_text='{"data":[{"id": "T", "text": "允许"}, {"id": "F", "text": "不允许"}]')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=4000, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="dicMainList_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="dicMainList_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="dicMainList_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class Seller(models.Model):
    sellerName = models.CharField(verbose_name='商家名称', max_length=200, null=True, help_text='')
    userId = models.ForeignKey(User, related_name="seller_userId", on_delete=models.SET_NULL, verbose_name='关联系统用户名',
                               null=True, help_text='')
    parentSellerId = models.IntegerField(verbose_name='所属商家（seller.id，null:系统商家或供应商）', null=True, help_text='')
    uniqueCode = models.CharField(verbose_name='商家识别唯一编码（可打印条形码二维码）', max_length=50, null=True, help_text='')
    sellerAddress = models.CharField(verbose_name='商家地址', max_length=500, null=True, help_text='')
    sellerLinkman = models.CharField(verbose_name='商家联系人', max_length=50, null=True, help_text='')
    sellerTel = models.CharField(verbose_name='商家电话', max_length=50, null=True, help_text='')
    employeeSnGType = models.CharField(verbose_name='员工编号生成方式', max_length=50, null=True,
                                       help_text='{"data":[{"id": "auto", "text": "自动[从1001开始]"}, {"id": "radom", "text": "4位随机"}, {"id": "input", "text": "输入"}]')
    sellerType = models.CharField(verbose_name='商家类型', max_length=10, null=True,
                                  help_text='{"data":[{"id": "1", "text": "商家"}, {"id": "2", "text": "供应商"}]')
    status = models.CharField(verbose_name='状态', max_length=1, null=True,
                              help_text='{"data":[{"id": "T", "text": "有效"}, {"id": "F", "text": "无效"}]')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="seller_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="seller_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="seller_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class DicMainListForSelect(models.Model):
    sellerId = models.ForeignKey(Seller, related_name="dicMainListForSelect_sellerId", on_delete=models.SET_NULL,verbose_name='所属商家（0：系统）当允许商家维护选项时，显示可选内容为系统和商家的可选项', null=True, help_text='')
    dicMainListId = models.ForeignKey(DicMainList, related_name="dicMainListForSelect_dicMainListId",on_delete=models.SET_NULL, verbose_name='系统选择项字典表Id（dicMainList.id）', null=True,help_text='')
    textForSelect = models.CharField(verbose_name='可选项显示文本', max_length=50, null=True, help_text='')
    valueForSelect = models.CharField(verbose_name='可选项值', max_length=50, null=True, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="dicMainListForSelect_adder", on_delete=models.SET_NULL,verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="dicMainListForSelect_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="dicMainListForSelect_deleter", on_delete=models.SET_NULL,verbose_name='删除人', null=True, help_text='')

    @property
    def users(self):
        relations = User_dic.objects.filter(dicMainListId = self.id).only(userId)
        user_ids = [r.userId for r in relations]
        return User.objects.filter(id__in=user_ids)

    @property
    def roles(self):
        relations = Role_dic.objects.filter(dicMainListId = self.id).only(roleId)
        role_ids = [r.roleId for r in relations]
        return User.objects.filter(id__in=role_ids)

    
class Role(models.Model):
    roleName = models.CharField(verbose_name='角色名称', max_length=50, null=True, help_text='')
    sellerId = models.ForeignKey(Seller, related_name="role_sellerId", on_delete=models.SET_NULL,verbose_name='商家ID（seller.id）（null(0)：系统角色）', null=True, help_text='')
    memo = models.CharField(verbose_name='说明', max_length=200, null=True, help_text='')
    menuIdList = models.CharField(verbose_name='访问菜单权限(menu.id,nenu.id,...)', max_length=500, null=True, help_text='')
    sorts = models.IntegerField(verbose_name='排序', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="role_adder", on_delete=models.SET_NULL, verbose_name='添加人（users.id）',null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="role_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="role_deleter", on_delete=models.SET_NULL, verbose_name='删除人',null=True, help_text='')

    @property
    def paras(self):
        '''角色的所有单值参数'''
        relations = RolePara.objects.filter(roleId=self.id).filter(drletetime=None).only('sysparaId')
        sysparaIds = [r.sysparaId for r in relations]
        return Syspara.objects.filter(id__in=sysparaIds)

    @property
    def dic_list(self):
        '''角色所有的字典参数'''
        relations = Role_dic.objects.filter(role_id=self.id).filter(deletetime=None).only('dicMainListId')
        dicMainListIds = [r.dic_id for r in relations]
        return DicMainListForSelect.objects.filter(dicMainListId__in=dicMainListIds)


class RolePur(models.Model):
    roleId = models.ForeignKey(Role, related_name="rolePur_roleId", on_delete=models.SET_NULL, verbose_name='权限组',null=True, help_text='')
    purcode = models.CharField(verbose_name='权限代码', max_length=50, null=True, help_text='')
    purview = models.CharField(verbose_name='权限', max_length=1, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="rolePur_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="rolePur_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="rolePur_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class UserPur(models.Model):
    userId = models.ForeignKey(User, related_name="userPur_userId", on_delete=models.SET_NULL, verbose_name='权限组',
                               null=True, help_text='')
    purcode = models.CharField(verbose_name='权限代码', max_length=50, null=True, help_text='')
    purview = models.CharField(verbose_name='权限', max_length=1, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="userPur_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="userPur_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="userPur_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class UserRole(models.Model):
    userId = models.ForeignKey(User, related_name="userRole_userId", on_delete=models.SET_NULL,verbose_name='用户ID（user.id）', null=True, help_text='')
    roleId = models.ForeignKey(Role, related_name="userRole_roleId", on_delete=models.SET_NULL,verbose_name='角色ID（role.id）', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="userRole_adder", on_delete=models.SET_NULL,verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="userRole_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="userRole_deleter", on_delete=models.SET_NULL, verbose_name='删除人',null=True, help_text='')


class InformType(models.Model):
    informName = models.CharField(verbose_name='消息名称', max_length=50, null=True, help_text='')
    informTag = models.CharField(verbose_name='消息标志', max_length=50, null=True, help_text='')
    informInfo = models.CharField(verbose_name='大致内容', max_length=500, null=True, help_text='')
    condition = models.CharField(verbose_name='触发条件说明', max_length=500, null=True, help_text='')
    codePosition = models.CharField(verbose_name='触发代码位置', max_length=500, null=True, help_text='')
    paramMemo = models.CharField(verbose_name='参数说明', max_length=2000, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="informType_adder", on_delete=models.SET_NULL,verbose_name='添加人（users.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="informType_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="informType_deleter", on_delete=models.SET_NULL, verbose_name='删除人',null=True, help_text='')


class SysparaForSeller(models.Model):
    sysparaId = models.ForeignKey(Syspara, related_name="sysparaForSeller_sysparaId", on_delete=models.SET_NULL,verbose_name='参数ID（syspara.id）', null=True, help_text='')
    sellerId = models.ForeignKey(Seller, related_name="sysparaForSeller_sellerId", on_delete=models.SET_NULL,verbose_name='商家ID（seller.id）', null=True, help_text='')
    paraValue = models.CharField(verbose_name='参数值', max_length=200, null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="sysparaForSeller_adder", on_delete=models.SET_NULL,verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="sysparaForSeller_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="sysparaForSeller_deleter", on_delete=models.SET_NULL,verbose_name='删除人（user.id）', null=True, help_text='')

    @property
    def users(self):
        relations = User_dic.objects.filter(dic_id=self.id).only('userId')
        user_ids = [r.userId for r in relations]
        return User.objects.filter(id__in=user_ids)


class InformTargetUser(models.Model):
    sellerId = models.ForeignKey(Seller, related_name="informTargetUser_sellersId", on_delete=models.SET_NULL,
                                 verbose_name='商家ID', null=True, help_text='')
    informTypeId = models.ForeignKey(InformType, related_name="informTargetUser_informTypeId",
                                     on_delete=models.SET_NULL, verbose_name='通知消息标志ID（informType.id）', null=True,
                                     help_text='')
    userId = models.ForeignKey(User, related_name="informTargetUser_userId", on_delete=models.SET_NULL,
                               verbose_name='接收消息的用户ID', null=True, help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="informTargetUser_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="informTargetUser_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="informTargetUser_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人', null=True, help_text='')


class InformTargetDept(models.Model):
    sellerId = models.ForeignKey(Seller, related_name="informTargetDept_sellerId", on_delete=models.SET_NULL,
                                 verbose_name='商家ID', null=True, help_text='')
    informTypeId = models.ForeignKey(InformType, related_name="informTargetDept_informTypeId",
                                     on_delete=models.SET_NULL, verbose_name='通知消息标志ID（informType.id）', null=True,
                                     help_text='')
    deptName = models.CharField(verbose_name='接收消息的部门名称', max_length=500, null=True, help_text='')
    positionList = models.CharField(verbose_name='指定职位（不指定：部门所有人；格式：职位名称,职位名称,职位名称,...）', max_length=500, null=True,
                                    help_text='')
    memo = models.CharField(verbose_name='备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="informTargetDept_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="informTargetDept_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="informTargetDept_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人', null=True, help_text='')


class UserShortcutMenu(models.Model):
    userId = models.ForeignKey(User, related_name="userShortcutMenu_userId", on_delete=models.SET_NULL,
                               verbose_name='用户（user.id）', null=True, help_text='')
    menuId = models.ForeignKey(Menu, related_name="userShortcutMenu_menuId", on_delete=models.SET_NULL,
                               verbose_name='菜单ID（menu.id）', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="userShortcutMenu_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）', null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="userShortcutMenu_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（users.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="userShortcutMenu_deleter", on_delete=models.SET_NULL,
                                verbose_name='删除人（user.id）', null=True, help_text='')


class SysLog(models.Model):
    sellerId = models.ForeignKey(Seller, related_name="sysLog_sellerId", on_delete=models.SET_NULL, verbose_name='商家ID',
                                 null=True, help_text='')
    weiXinAppId = models.CharField(verbose_name='AppId', max_length=50, null=True, help_text='')
    openid = models.CharField(verbose_name='用户对应公众号唯一标识（微信授权信息）', max_length=50, null=True, help_text='')
    title = models.CharField(verbose_name='标题', max_length=500, null=True, help_text='')
    info = models.CharField(verbose_name='日志内容', max_length=8000, null=True, help_text='')
    listsnType = models.CharField(verbose_name='相关单号类型（订单;发货单）', max_length=50, null=True, help_text='')
    listsn = models.CharField(verbose_name='相关单号', max_length=50, null=True, help_text='')
    tableName = models.CharField(verbose_name='相关表名', max_length=200, null=True, help_text='')
    tableId = models.IntegerField(verbose_name='相关表名ID', null=True, help_text='')
    memo = models.CharField(verbose_name='日志备注', max_length=500, null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="sysLog_adder", on_delete=models.SET_NULL, verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="sysLog_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="sysLog_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')


class UserPara(models.Model):
    # 用户与参数的关联表
    userId = models.IntegerField(verbose_name='用户ID（user.id）', null=True, help_text='')
    sysparaId = models.IntegerField(verbose_name='参数ID（para.id）', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="userPara_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="userPara_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="userPara_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')

    @classmethod
    def add_relations(cls, userId, sysparaIds):
        '''批量建立user和syspara的关联'''
        for r in sysparaIds:
            user_para = cls.objects.filter(sysparaId=r, userId=userId)
            if user_para:
                user_para.update(updatetime=datetime.now(), deletetime=None)
            else:
                user_para.create(userId=userId, sysparaId=r, updatetime=datetime.now())

    @classmethod
    def del_relations(cls, userId, sysparaIds):
        '''批量删除user和syspara的关联'''
        cls.objects.filter(userId=userId, sysparaId__in=sysparaIds).update(deletetime=datetime.now())


class User_dic(models.Model):
    """docstring for User_dic"""
    user_id = models.IntegerField(verbose_name='用户ID（user.id）', null=True, help_text='')
    dic_id = models.IntegerField(verbose_name='字典ID(dic_id)', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="user_dic_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="user_dic_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="user_dic_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')

    @classmethod
    def add_relations(cls, userId, dicMainListIds):
        '''批量建立user和DicMainListForSelect的关联'''
        for r in dicMainListIds:
            user_para = cls.objects.filter(dic_id=r, user_id=userId)
            if user_para:
                user_para.update(updatetime=datetime.now(), deletetime=None)
            else:
                user_para.create(user_id=userId, dic_id=r, updatetime=datetime.now())

    @classmethod
    def del_relations(cls, userId, dicMainListIds):
        '''批量删除user和DicMainListForSelect的关联'''
        cls.objects.filter(user_id=userId, dic_id__in=dicMainListIds).update(deletetime=datetime.now())


class RolePara(models.Model):
    # 用户与参数的关联表
    roleId = models.IntegerField(verbose_name='用户ID（role.id）', null=True, help_text='')
    sysparaId = models.IntegerField(verbose_name='参数ID（para.id）', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="rolePara_adder", on_delete=models.SET_NULL,verbose_name='添加人（user.id）',null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="rolePara_updater", on_delete=models.SET_NULL,verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="rolePara_deleter", on_delete=models.SET_NULL, verbose_name='删除人',null=True, help_text='')

    @classmethod
    def add_relations(cls, roleId, sysparaIds):
        '''批量建立user和syspara的关联'''
        for r in sysparaIds:
            role_para = cls.objects.filter(sysparaId=r, roleId=roleId)
            if role_para:
                role_para.update(updatetime=datetime.now(), deletetime=None)
            else:
                role_para.create(roleId=roleId, sysparaId=r, updatetime=datetime.now())

    @classmethod
    def del_relations(cls, roleId, sysparaIds):
        '''批量删除role和syspara的关联'''
        cls.objects.filter(roleId=roleId, sysparaId__in=sysparaIds).update(deletetime=datetime.now())


class Role_dic(models.Model):
    """docstring for Role_dic"""
    role_id = models.IntegerField(verbose_name='用户ID（role.id）', null=True, help_text='')
    dic_id = models.IntegerField(verbose_name='字典ID(dic_id)', null=True, help_text='')
    addtime = models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True, help_text='')
    adder = models.ForeignKey(User, related_name="role_dic_adder", on_delete=models.SET_NULL,
                              verbose_name='添加人（user.id）',
                              null=True, help_text='')
    updatetime = models.DateTimeField(verbose_name='最后修改时间', null=True, help_text='')
    updater = models.ForeignKey(User, related_name="role_dic_updater", on_delete=models.SET_NULL,
                                verbose_name='最后修改人（user.id）', null=True, help_text='')
    deletetime = models.DateTimeField(verbose_name='删除时间', null=True, help_text='')
    deleter = models.ForeignKey(User, related_name="role_dic_deleter", on_delete=models.SET_NULL, verbose_name='删除人',
                                null=True, help_text='')

    @classmethod
    def add_relations(cls, roleId, dicMainListIds):
        '''批量建立role和DicMainListForSelect的关联'''
        for r in dicMainListIds:
            role_para = cls.objects.filter(dicMainListId=r, roleId=roleId)
            if role_para:
                role_para.update(updatetime=datetime.now(), deletetime=None)
            else:
                role_para.create(roleId=roleId, dicMainListId=r, updatetime=datetime.now())

    @classmethod
    def del_relations(cls, roleId, dicMainListIds):
        '''批量删除role和DicMainListForSelect的关联'''
        cls.objects.filter(roleId=roleId, dicMainListId__in=dicMainListIds).update(deletetime=datetime.now())

