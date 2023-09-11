from django.contrib import admin


class ExpireKeywordFilter(admin.SimpleListFilter):
    #  右侧栏人为可读的标题
    title = '按账户有效时间'

    # 在url中显示的参数名，如?keyword=xxx.
    parameter_name = 'expire'

    """
    自定义需要筛选的参数元组. 
    """

    def lookups(self, request, model_admin):
        return (
            ('unKnow', '未知时效的用户'),
            ('expired', '已经过期'),
            ('expired_within_month', '一个月内过期'),
            ('expired_without_month', '其他'),
        )

    def queryset(self, request, queryset):
        """
        调用self.value()获取url中的参数， 然后筛选所需的queryset.
        """

        if self.value() == 'unKnow':
            return queryset.filter(expire_at=None)
        if self.value() == 'expired':
            return queryset.filter(expire_at__lt=timezone.now())
        if self.value() == 'expired_within_month':
            return queryset.filter(expire_at__lt=timezone.now() + datetime.timedelta(days=30),
                                   expire_at__gt=timezone.now())
        if self.value() == 'expired_without_month':
            return queryset.filter(expire_at__gt=timezone.now() + datetime.timedelta(days=30))


class UserRoleKeywordFilter(admin.SimpleListFilter):
    #  右侧栏人为可读的标题
    title = '按账户角色筛选'

    # 在url中显示的参数名，如?keyword=xxx.
    parameter_name = 'role'

    """
    自定义需要筛选的参数元组. 
    """

    def lookups(self, request, model_admin):
        return (
            ('unKnow', '行业用户'),
            ('admin', 'admin'),
            ('ordinary', '普通用户'),
            ('ordinary_admin', '普通管理员'),
        )

    def queryset(self, request, queryset):
        """
        调用self.value()获取url中的参数， 然后筛选所需的queryset.
        """

        if self.value() == 'unKnow':
            return queryset.filter(roles__role_name='行业用户')
        if self.value() == 'admin':
            return queryset.filter(roles__role_name='admin')
        if self.value() == 'ordinary':
            return queryset.filter(roles__role_name='普通用户')
        if self.value() == 'ordinary_admin':
            return queryset.filter(roles__role_name='普通管理员')

class UserNameKeywordFilter(admin.SimpleListFilter):
    #  右侧栏人为可读的标题
    title = '按用户来源筛选'

    # 在url中显示的参数名，如?keyword=xxx.
    parameter_name = 'source'

    """
    自定义需要筛选的参数元组. 
    """

    def lookups(self, request, model_admin):
        return (
            ('unKnow', 'ip用户'),
            ('register', '登记用户'),
        )

    def queryset(self, request, queryset):
        """
        调用self.value()获取url中的参数， 然后筛选所需的queryset.
        """

        if self.value() == 'unKnow':
            return queryset.filter(user_name__contains=':')
        if self.value() == 'register':
            return queryset.exclude(user_name__contains=':')
