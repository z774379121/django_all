import ipaddress
import json
import random
import uuid
import csv

import requests
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import User, Group
from django.http import HttpResponse
from .models import *
from .form.form import *
from .fliter import *
from django.utils import timezone
import datetime

admin.site.site_header = "我的后台2.0"
admin.site.site_title = "我的后台2.0"
admin.site.index_title = '后台数据管理'


# admin.site.register(SysRole)

# admin.site.unregister(User)
# admin.site.unregister(Group)

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "导出所选内容到csv"



class DeviceInline(admin.TabularInline):
    model = SysUserDevice
    verbose_name = "登记设备"
    verbose_name_plural = "登记设备"
    # max_num = 3
    # min_num = 1
    extra = 1
    exclude = ('update_time', 'create_time', 'disable')


class UserRoleInline(admin.TabularInline):
    model = SysMapUserRole


class TradeTagsInline(admin.TabularInline):
    model = SysTrades.tags.through
    exclude = ('update_time', 'create_time', 'delete_time')
    fields = ('trade_id', 'tag_id')
    raw_id_fields = ('trade_id', 'tag_id')


class SysTradeInline(admin.TabularInline):
    model = SysTrades


class UserAppInline(admin.TabularInline):
    model = SysUser.apps.through
    exclude = ('update_time', 'create_time', 'disable')
    fields = ["appid", 'userid', ]
    # radio_fields = {"userid": admin.HORIZONTAL, "appid": admin.HORIZONTAL}
    raw_id_fields = ("userid", 'appid')
    # list_filter = (
    #     ('SysApp', admin.RelatedOnlyFieldListFilter),
    #     ('SysUser', admin.RelatedOnlyFieldListFilter),
    # )

    # list_select_related = ('SysApp', 'SysUser')



def create_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    for i in range(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


# 获取原始密码+salt的md5值
def create_md5(pwd, salt):
    md5_obj = hashlib.md5()
    md5_obj.update((salt + pwd).encode(encoding="utf-8"))
    return md5_obj.hexdigest()


# Register your models here.
@admin.register(SysUser)
class SysUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    save_on_top = True
    save_as_continue = False
    list_per_page = 25
    form = UserForm
    add_form = UserAddForm
    # exclude = ('roles',)
    # exact 精准搜索, 可以通过外键trade_id__name搜索trade name
    search_fields = ("user_name", "real_name", "cellphone__exact", "trade_id__name")
    # inlines = [DeviceInline, UserRoleInline, UserAppInline, ]
    # inlines = [DeviceInline, UserRoleInline, ]
    inlines = [UserRoleInline]
    ordering = ("-real_name",)
    list_display = (
        "user_name", "real_name", 'user_category', 'role_name', "position_job", "cellphone", "user_is_locked",
        "is_expire_at", 'is_device_bind', "is_device_limit",)

    # 设置进入更改页面的字段 篮子
    list_display_links = ("user_name", "real_name" )
    list_filter = ('position_job', ExpireKeywordFilter, UserRoleKeywordFilter)
    # exclude = ("roles",)
    # fieldsets = (
    #     ('Personal info', {'fields': ('user_name', 'real_name', 'cellphone')}),
    #     ('Permissions', {
    #         'fields': ('position_job', 'user_permissions'),
    #     }),
    #     ('Important dates', {'fields': ('expire_at',)}),
    # )
    # readonly_fields = ("user_name",)
    filter_horizontal = ('apps',)
    radio_fields = {"is_locked": admin.VERTICAL}

    empty_value_display = 'unknown'
    actions = ["add_expired", "set_user_decay", 'clean_user_device', 'export_as_csv']

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    # def get_user_app_count(self, obj):
    #     # return len(obj.apps.all())
    #     return obj.did.count()

    def is_device_bind(self, obj):
        return obj.device_id is not None and obj.device_id != ""

    is_device_bind.boolean = True
    is_device_bind.short_description = "设备绑定情况"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["user_name", ]
        else:
            return []

    def save_model(self, request, obj, form, change):
        if change:
            print("保存")
        else:
            obj.salt = create_salt(16)
            obj.password = create_md5(obj.password, obj.salt)
            obj.create_time = timezone.now()
            obj.user_id = uuid.uuid1()

        super().save_model(request, obj, form, change)

    def is_expire_at(self, obj):
        if obj.expire_at is None:
            return "未知"
        if timezone.now() > obj.expire_at:
            return "已经过期"
        return obj.expire_at

    is_expire_at.short_description = "账户时效"

    def is_device_limit(self, obj):
        return obj.device_free == 0

    is_device_limit.boolean = True
    is_device_limit.short_description = "设备限制"

    def user_category(self, obj):
        if obj.user_category == 1:
            return "行业用户"
        else:
            return "个人用户"

    def user_is_locked(self, obj):
        return obj.is_locked == 0

    user_is_locked.boolean = True

    user_is_locked.short_description = "账户有效性"

    def role_name(self, obj):
        return [role.role_name for role in obj.roles.all()]

    '''自定义actions'''

    def set_expired(self, request, queryset):
        queryset.update(expire_at=timezone.now() + datetime.timedelta(days=90))
        self.message_user(request, "操作成功, 已为{}个账户设置期限为3个月后".format(len(queryset)), messages.SUCCESS)

    set_expired.short_description = "将所选账户有效期设置为三个月之后"

    def add_expired(self, request, queryset):
        for obj in queryset:
            if obj.expire_at:
                obj.expire_at = obj.expire_at + datetime.timedelta(days=366)
            else:
                obj.expire_at = timezone.now() + datetime.timedelta(days=366)
            obj.save()

        self.message_user(request, "操作成功, 已为{}个账户增加期限".format(len(queryset)), messages.SUCCESS)

    add_expired.short_description = "续一年"

    def set_user_decay(self, request, queryset):
        queryset.update(expire_at=timezone.now() - datetime.timedelta(days=1))
        self.message_user(request, "操作成功, 已为{}个账户设置为过期".format(len(queryset)), messages.SUCCESS)

    set_user_decay.short_description = "使过期"

    def clean_user_device(self, request, queryset):
        queryset.update(device_id="")
        self.message_user(request, "操作成功", messages.SUCCESS)

    clean_user_device.short_description = "解绑已有设备"




@admin.register(SysApp)
class AppAdmin(admin.ModelAdmin, ExportCsvMixin):
    save_on_top = True
    # inlines = [UserAppInline, ]
    form = AppTagsForm
    list_display = ['app_name', 'description', 'tags', 'author', 'time', 'size', 'app_is_locked', 'app_is_enable',
                    'children_display']
    # fields = (("app_name", "description"), "tags", "author", 'time', 'size', ("locked", "enable"),
    #           )
    # list_select_related = ('SysUser',)
    search_fields = ('app_name',)
    # readonly_fields = ("user_name",)
    action = ('export_as_csv',)

    list_filter = ('author', 'enable', 'locked', 'tagsv2')

    def app_is_locked(self, obj):
        return obj.locked == 0

    app_is_locked.boolean = True

    def app_is_enable(self, obj):
        return obj.enable == 1

    app_is_enable.boolean = True

    def children_display(self, obj):
        return ", ".join([
            child.name for child in obj.tagsv2.filter(level__gte=1).all()[:5]
        ])

    children_display.short_description = "标签V2"


# @admin.register(SysUserApp)
# class UserAppAdmin(admin.ModelAdmin):
#
#     view_on_site = False
#     # raw_id_fields = ("userid", "appid")
#     # fields = ()
#     # exclude = ('update_at',)
#     # list_filter = (
#     #     ('userid', admin.RelatedOnlyFieldListFilter),
#     #     ('appid', admin.RelatedOnlyFieldListFilter),
#     # )


@admin.register(SysRole)
class UserRoleAdmin(admin.ModelAdmin):
    # view_on_site = False
    # raw_id_fields = ("userid", "appid")
    exclude = ('role_id',)
    # exclude = ('update_at',)
    # list_filter = (
    #     ('userid', admin.RelatedOnlyFieldListFilter),
    #     ('appid', admin.RelatedOnlyFieldListFilter),
    # )




@admin.register(SysTrades)
class SysTradesAdmin(admin.ModelAdmin):
    # view_on_site = False
    # raw_id_fields = ("userid", "appid")
    form = TradeForm
    # inlines = (TradeTagsInline,)

    # exclude = ('update_at',)
    # list_filter = (
    #     ('userid', admin.RelatedOnlyFieldListFilter),
    #     ('appid', admin.RelatedOnlyFieldListFilter),
    # )




@admin.register(SysTags)
class SysTagsAdmin(admin.ModelAdmin):
    save_on_top = True
    form = TagsForm
    add_form = TagsAddForm
    list_display = ('id', 'name', 'level', 'path', 'sequence')
    list_filter = ('level',)
    search_fields = ('name',)
    ordering = ('path', 'sequence')
    readonly_fields = ("path",)

    actions = ('delete_model',)

    # def has_change_permission(self, request, obj=None):
    #    if obj is None:  # 显示列表页
    #        return True
    #    else:  # 禁用详情页
    #        return False

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None or obj.level == 1:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            base_id = request.POST.get("tag")
            sequence = request.POST.get("sequence")
            # print(name, base_id)
            # print(obj.name)
            url = 'https://cloud.vitoreality.com/api/tags'
            s = json.dumps({'name': obj.name, 'base_id': int(base_id), 'sequence': int(sequence)})
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
            }
            r = requests.post(url, data=s, headers=headers)
            self.message_user(request, r.text, messages.SUCCESS)
        # super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    #    def has_change_permission(self, request, obj=None):
    #        return False
    #
    def delete_model(self, request, queryset):
        for obj in queryset:
            url = 'https://cloud.vitoreality.com/api/tags'
            s = json.dumps({'id': int(obj.id)})
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
            }
            r = requests.delete(url, data=s, headers=headers)
            self.message_user(request, r.text, messages.SUCCESS)

    delete_model.short_description = "删除"


@admin.register(PlayContent)
class PlayContentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('app_name', "version", 'user_name', "user_name_real", 'student_count', 'play_date')
    ordering = ('-play_date',)
    exclude = ('record_time',)
    date_hierarchy = 'play_date'
    search_fields = ('app_name', 'user_name')
    list_filter = ('play_date', UserNameKeywordFilter)
    can_delete = False
    fields = ('app_name',)
    readonly_fields = ('app_name',)
    actions = ["export_as_csv"]

    # list_filter = (
    #     ('userid', admin.RelatedOnlyFieldListFilter),
    #     ('appid', admin.RelatedOnlyFieldListFilter),
    # )
    # def name(self, obj):
    #
    #     if obj.user_name is None:
    #         return "n"
    #     return obj.user_name
    #
    # def real_name(self, obj):
    #     return obj.user_name.real_name


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user_name', "user_name_real", 'version', 'login_time')
    ordering = ('-login_time',)
    exclude = ('record_time',)
    date_hierarchy = 'login_time'
    search_fields = ('version', 'user_name')
    list_filter = ('login_time',)
    can_delete = False
    fields = ('user_name',)
    readonly_fields = ('user_name',)
    actions = ["export_as_csv"]
