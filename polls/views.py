from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect


def redicter(request):
    return HttpResponseRedirect("/admin/")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
