# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import base64
import hashlib

import django
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

LOCKED = (
    (0, 'No'),
    (1, 'LOCK'),
)

CATEGORY = (
    (1, '企业用户'),
    (2, '个人用户'),
)

DEVICEFREE = (
    (0, '限制设备'),
    (1, '不限制设备'),
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, default=django.utils.timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=django.utils.timezone.now)

    class Meta:
        abstract = True

# class Classes(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     school_id = models.CharField(max_length=255, blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     remark = models.CharField(max_length=255, blank=True, null=True)
#     head_teacher = models.CharField(max_length=255, blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'classes'
#
#
# class MapClassApp(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     c_id = models.IntegerField(blank=True, null=True)
#     a_id = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'map_class_app'
#
#
# class MapClassStudents(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     s_id = models.IntegerField(blank=True, null=True)
#     c_id = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'map_class_students'
#         unique_together = (('s_id', 'c_id'),)
#
#
# class MapUserLocation(models.Model):
#     user_name = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'map_user_location'
#
#

#
#
# class Students(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     school_id = models.CharField(max_length=255, blank=True, null=True)
#     class_id = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     gender = models.IntegerField(blank=True, null=True)
#     s_number = models.CharField(max_length=255, blank=True, null=True)
#     age = models.IntegerField(blank=True, null=True)
#     remark = models.CharField(max_length=255, blank=True, null=True)
#     is_graduated = models.IntegerField(blank=True, null=True)
#     avatar = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'students'
#         unique_together = (('school_id', 's_number'),)


class SysApp(BaseModel):
    app_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    version_id = models.CharField(max_length=20, blank=True, null=True)
    version_code = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    icon_path = models.CharField(max_length=512, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    tags = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=128, blank=True, null=True)
    time = models.CharField(max_length=128, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    locked = models.IntegerField(blank=True, null=True)
    tagsv2 = models.ManyToManyField('SysTags', through="SysAppTags", through_fields=("app_id", "tag_id"), )
    enable = models.IntegerField()

    class Meta:
        verbose_name = '应用信息'
        verbose_name_plural = '应用信息'
        managed = True
        db_table = 'sys_app'

    def __str__(self):
        return self.app_name


# class SysAppResource(models.Model):
#     app_id = models.IntegerField(blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#     version_name = models.CharField(max_length=128, blank=True, null=True)
#     version_code = models.SmallIntegerField(blank=True, null=True)
#     package_name = models.CharField(max_length=512, blank=True, null=True)
#     download_url = models.CharField(max_length=512, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'sys_app_resource'
#
#
# class SysAppSubuserDisable(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     app_id = models.IntegerField(blank=True, null=True)
#     user_id = models.CharField(db_column='USER_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
#     flag = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'sys_app_subuser_disable'
#
#
# class SysGroup(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     mark = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'sys_group'
#
#
# class SysIdAccess(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     user_id = models.CharField(db_column='USER_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
#     access_key_id = models.CharField(unique=True, max_length=255)
#     secret_key = models.CharField(unique=True, max_length=255)
#     bind_ip = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'sys_id_access'
#
#
# class SysLog(models.Model):
#     log_id = models.CharField(db_column='LOG_ID', primary_key=True, max_length=36)  # Field name made lowercase.
#     user = models.ForeignKey('SysUser', models.DO_NOTHING, db_column='USER_ID', blank=True,
#                              null=True)  # Field name made lowercase.
#     operation_name = models.CharField(db_column='OPERATION_NAME', max_length=30)  # Field name made lowercase.
#     log_time = models.DateTimeField(db_column='LOG_TIME')  # Field name made lowercase.
#     result = models.IntegerField(db_column='RESULT', blank=True, null=True)  # Field name made lowercase.
#     result_description = models.CharField(db_column='RESULT_DESCRIPTION', max_length=200, blank=True,
#                                           null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = True
#         db_table = 'sys_log'
#
#
# class SysMapRolePermission(models.Model):
#     role = models.ForeignKey('SysRole', models.DO_NOTHING, db_column='ROLE_ID',
#                              primary_key=True)  # Field name made lowercase.
#     permission = models.ForeignKey('SysPermission', models.DO_NOTHING,
#                                    db_column='PERMISSION_ID')  # Field name made lowercase.
#
#     class Meta:
#         managed = True
#         db_table = 'sys_map_role_permission'
#         unique_together = (('role', 'permission'),)
#
#
# class SysMapUserGroup(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     group_id = models.IntegerField(blank=True, null=True)
#     user_id = models.CharField(db_column='USER_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = True
#         db_table = 'sys_map_user_group'
#
#
class SysMapUserRole(models.Model):
    user = models.ForeignKey('SysUser', models.CASCADE, db_column='USER_ID',
                             primary_key=True)  # Field name made lowercase.
    role = models.ForeignKey('SysRole', models.CASCADE, db_column='ROLE_ID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'sys_map_user_role'
        unique_together = (('user', 'role'),)


#
#
# class SysPermission(models.Model):
#     permission_id = models.CharField(db_column='PERMISSION_ID', primary_key=True,
#                                      max_length=36)  # Field name made lowercase.
#     permission_name = models.CharField(db_column='PERMISSION_NAME', max_length=128)  # Field name made lowercase.
#     permission_type = models.IntegerField(db_column='PERMISSION_TYPE')  # Field name made lowercase.
#     url = models.CharField(db_column='URL', max_length=128)  # Field name made lowercase.
#     percode = models.CharField(db_column='PERCODE', max_length=128)  # Field name made lowercase.
#     parent_permission = models.ForeignKey('self', models.DO_NOTHING, db_column='PARENT_PERMISSION_ID', blank=True,
#                                           null=True)  # Field name made lowercase.
#     sort = models.IntegerField(db_column='SORT')  # Field name made lowercase.
#     is_available = models.IntegerField(db_column='IS_AVAILABLE')  # Field name made lowercase.
#     icon = models.CharField(db_column='ICON', max_length=30, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = True
#         db_table = 'sys_permission'
#
#

class SysUserLocid(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    local_id = models.IntegerField(unique=True)
    user_id = models.CharField(db_column='USER_ID', max_length=255)  # Field name made lowercase.
    pid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sys_user_locid'


class SysRole(models.Model):
    role_id = models.AutoField(db_column='ROLE_ID', primary_key=True, max_length=36)  # Field name made lowercase.
    role_name = models.CharField(db_column='ROLE_NAME', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    is_available = models.IntegerField(db_column='IS_AVAILABLE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = '权限列表'
        verbose_name_plural = '权限列表'
        managed = True
        db_table = 'sys_role'

    def __str__(self):
        return self.role_name


#
#
#
# class SysUserResource(models.Model):
#     id = models.CharField(primary_key=True, max_length=36)
#     ower_id = models.CharField(max_length=36, blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#     uri = models.CharField(max_length=128, blank=True, null=True)
#     cover = models.CharField(max_length=128, blank=True, null=True)
#     create_time = models.DateTimeField(blank=True, null=True)
#     name = models.CharField(max_length=128, blank=True, null=True)
#     description = models.CharField(max_length=256, blank=True, null=True)
#     is_up = models.TextField(blank=True, null=True)  # This field type is a guess.
#     is_nice = models.TextField(blank=True, null=True)  # This field type is a guess.
#     disable = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'sys_user_resource'
#
#
# class SysUserSubuser(models.Model):
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     parent_user_id = models.CharField(max_length=255, blank=True, null=True)
#     user_id = models.CharField(db_column='USER_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = True
#         db_table = 'sys_user_subuser'
class SysUser(BaseModel):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=36)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', unique=True, max_length=30)  # Field name made lowercase.
    real_name = models.CharField(db_column='REAL_NAME', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=32)  # Field name made lowercase.
    user_category = models.IntegerField(db_column='USER_CATEGORY', choices=CATEGORY)  # Field name made lowercase.
    position_job = models.CharField(db_column='POSITION_JOB', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cellphone = models.CharField(db_column='CELLPHONE', max_length=15, blank=True,
                                 null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salt = models.CharField(db_column='SALT', max_length=24)  # Field name made lowercase.
    device_id = models.CharField(db_column='DEVICE_ID', max_length=128, blank=True,
                                 null=True)  # Field name made lowercase.
    is_locked = models.IntegerField(db_column='IS_LOCKED', choices=LOCKED)  # Field name made lowercase.
    device_free = models.IntegerField(db_column='DEVICE_FREE', choices=DEVICEFREE)  # Field name made lowercase.
    expire_at = models.DateTimeField(blank=True, null=True)
    trade_id = models.ForeignKey('SysTrades', db_column='TRADE_ID', on_delete=models.DO_NOTHING, verbose_name='行业')
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    apps = models.ManyToManyField('SysApp', through="SysUserApp", through_fields=("userid", "appid"))
    roles = models.ManyToManyField('SysRole', through='SysMapUserRole')

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = '账户信息'
        managed = True
        db_table = 'sys_user'

    def __str__(self):
        return self.user_name

    def gen_salted_password(self):
        md5_obj = hashlib.md5()
        md5_obj.update((self.salt + self.pwd).encode(encoding="utf-8"))
        self.password = md5_obj.hexdigest()
    # def get_absolute_url(self):
    #     return "/people/%i/" % self.id
    # def save_title_hash(self):
    #     title_hash = hash(title)
    #     return title_hash
    #
    #  = property(save_title_hash)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.salt == "":
            hl = hashlib.md5()
            self.salt = str(base64.b64encode(self.user_name[:5].encode(encoding="utf-8")))
            enpass = self.salt + self.password
            hl.update(enpass.encode(encoding='utf-8'))
            self.password = hl.hexdigest()
            self.create_time = timezone.now()
        super(SysUser, self).save()


class SysUserApp(BaseModel):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(SysUser, models.CASCADE, db_column='userId',
                               to_field='user_id')  # Field name made lowercase.
    appid = models.ForeignKey(SysApp, models.CASCADE, db_column='appId', to_field='id')  # Field name made lowercase.
    disable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sys_user_app'
        unique_together = ('userid', 'appid')

    def __str__(self):
        return f'{self.appid} for {self.userid}'


class SysUserDevice(BaseModel):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(SysUser, models.CASCADE, db_column='userId', related_query_name="did",
                               related_name="did", )  # Field name made lowercase.
    deviceid = models.CharField(unique=True, max_length=255)
    remark = models.CharField(max_length=512, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    disable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sys_user_device'


class LoginRecord(models.Model):
    user_name = models.CharField(max_length=128, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    record_time = models.BigIntegerField(blank=True, null=True)

    @property
    def user_name_real(self):
        try:
            sysUser = SysUser.objects.get(user_name=self.user_name)
            return sysUser.real_name
        except ObjectDoesNotExist:
            return "未知"

    class Meta:
        verbose_name = '登录历史'
        verbose_name_plural = '登录历史'
        managed = True
        db_table = 'login_record'


class PlayContent(models.Model):
    app_name = models.CharField(max_length=128, blank=True, null=True)
    # user_name = models.ForeignKey(SysUser, to_field="user_name", on_delete=models.DO_NOTHING, db_column="user_name",
    #                               null=True)
    user_name = models.CharField(max_length=128, blank=True, null=True)
    student_count = models.IntegerField(blank=True, null=True)
    play_date = models.DateTimeField(blank=True, null=True)
    record_time = models.BigIntegerField(blank=True, null=True)

    @property
    def user_name_real(self):
        try:
            sysUser = SysUser.objects.get(user_name=self.user_name)
            return sysUser.real_name
        except ObjectDoesNotExist:
            return "null"

    @property
    def version(self):
        try:
            Record = LoginRecord.objects.filter(user_name=self.user_name, login_time__lte=self.play_date).latest(
                "login_time")
            return Record.version
        except ObjectDoesNotExist:
            return "null"

    class Meta:
        verbose_name = '应用使用情况'
        verbose_name_plural = '应用使用情况'
        managed = True
        db_table = 'play_content'


class SysTrades(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    tags = models.ManyToManyField('SysTags', through="SysMapTradeTags", through_fields=('trade_id', 'tag_id'))

    class Meta:
        verbose_name = '行业'
        verbose_name_plural = '行业'
        managed = True
        db_table = 'sys_trades'

    def __str__(self):
        return self.name


class SysTags(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(default=0)
    apps = models.ManyToManyField('SysApp', through="SysAppTags", through_fields=("tag_id", "app_id"), )

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        managed = True
        db_table = 'sys_tags'

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        print(self.id)


class SysMapTradeTags(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    trade_id = models.ForeignKey(SysTrades, db_column='trade_id', on_delete=models.CASCADE, to_field='id')
    tag_id = models.ForeignKey(SysTags, db_column='tag_id', on_delete=models.CASCADE, to_field="id")

    class Meta:
        managed = True
        db_table = 'sys_map_trade_tags'
        unique_together = (('trade_id', 'tag_id'),)


class SysAppTags(BaseModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    app_id = models.ForeignKey(SysApp, db_column='app_id', on_delete=models.CASCADE, to_field='id')
    tag_id = models.ForeignKey(SysTags, db_column='tag_id', on_delete=models.CASCADE, to_field='id')

    class Meta:
        managed = True
        db_table = 'sys_app_tags'
        unique_together = (('app_id', 'tag_id'),)
