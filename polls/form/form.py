from django import forms
from polls.models import *
from django.contrib import admin, messages
#from django.contrib.admin.widgets import FilteredSelectMultiple

class UserForm(forms.ModelForm):
    apps = forms.ModelMultipleChoiceField(widget=admin.widgets.FilteredSelectMultiple('apps', False),
                                          queryset=SysApp.objects.all(), required=False)

    class Meta:
        model = SysUser
        fields = (
            "user_name", "real_name", 'user_category', "position_job", "cellphone", "is_locked", "device_id",
            "device_free",
            "expire_at",
            'apps', 'trade_id')
        labels = ('账户', '真实姓名', '性质', '职位', '手机', '是否可用', '设备id', '设备限制', '过期时间', '拥有的应用')
        help_text = "编辑用户信息"


class UserAddForm(forms.ModelForm):
    apps = forms.ModelMultipleChoiceField(widget=admin.widgets.FilteredSelectMultiple('apps', False),
                                          queryset=SysApp.objects.all(), required=False)

    class Meta:
        model = SysUser
        fields = (
            "user_name", "password", "real_name", 'user_category', "position_job", "cellphone", "is_locked",
            "device_id",
            "device_free",
            "expire_at",
            'apps', 'trade_id')
        labels = ('账户', '真实姓名', '性质', '职位', '手机', '是否可用', '过期时间', '拥有的应用')
        help_text = "编辑用户信息"

class AppTagsForm(forms.ModelForm):
    tagsv2 = forms.ModelMultipleChoiceField(widget=admin.widgets.FilteredSelectMultiple('tags', False),
                                            queryset=SysTags.objects.filter(level__gt=1).all(), required=False)

    class Meta:
        model = SysApp
        fields = ("app_name", "description", "tags", "author", 'time', 'size', "locked", "enable", 'tagsv2'
                  )
        labels = {"app_name": "应用名", "description": "描述", "tagsv2": "标签",
                  }
        help_text = "编辑应用信息"

class TradeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(widget=admin.widgets.FilteredSelectMultiple('tags', False),
                                          queryset=SysTags.objects.filter(level=1).all(), required=False)

    class Meta:
        model = SysTrades
        fields = (
            'name',
            'tags')
        labels = ("名称", "标签")
        help_text = "编辑行业"

class TagsAddForm(forms.ModelForm):
    tag = forms.IntegerField(
        widget=forms.widgets.Select(), label="父标签", initial=0
    )

    class Meta:
        model = SysTags
        fields = (
            'name',
            'tag',
            'sequence',
        )
        labels = {'name': "名称", 'tag': "父标签"}
        help_text = "编辑标签"

    def __init__(self, *args, **kwargs):
        super(TagsAddForm, self).__init__(*args, **kwargs)
        self.fields["tag"].widget.choices = list(SysTags.objects.values_list("id", "name"))
        self.fields["tag"].widget.choices.append((0, "无父标签"))


class TagsForm(forms.ModelForm):
    apps = forms.ModelMultipleChoiceField(widget=admin.widgets.FilteredSelectMultiple('apps', False),
                                          queryset=SysApp.objects.all(), required=False)

    class Meta:
        model = SysTags
        fields = (
            'name',
            'path',
            'apps',
            'sequence',
        )
        labels = {'name': "名称", 'path': "路径"}
        help_text = "编辑标签"
