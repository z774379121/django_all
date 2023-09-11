from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('^polls/sysuser/(?P<object_id>.+)/change/$', views.index)
]
