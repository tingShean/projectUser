# -*- coding: utf-8 -*
from django.shortcuts import render
# from django.http import JsonResponse
# from django.template import RequestContext
from login.models import UserAuthorize


def check_user_canread(view_func):

    def _wrapped_view_func(request, *args, **kwargs):
        try:
            uid = request.POST['uid']
            authorize = UserAuthorize.objects.get(uid=uid)

            if not authorize:
                return render(request, 'login.index.html', context={})

            if int(authorize.authorize) < 1:
                return render(request, 'login.index.html', context={})

        except Exception:
            return render(request, 'login.index.html', context={})

        # return func
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func