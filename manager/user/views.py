from django.shortcuts import render
from decorators.cookie import check_cookie
from utils.tools import get_admin_uid_cookie
from utils.html_render import web_render
from login.models import UserManagers
from .models import Users


# Create your views here.
@check_cookie
def user_list(request):
    context = {}

    if request.method == 'GET':
        # get authorize
        uid = get_admin_uid_cookie(request)
        user = {
            'uid': uid,
        }

        try:
            admin = UserManagers.objects.get(uid=uid)
            if not admin:
                return web_render(request, 'login.index.html', context=context)

            # check authorize
            authorize = admin.authorize
            if authorize < 1:
                return web_render(request, 'login.index.html', context=context)

            # get all user
            user_list = Users.objects.all()
            context['user_list'] = []
            for usr in user_list:
                context['user_list'].append({
                    'uid': usr.id,
                    'account': usr.account,
                    'name': usr.name,
                    'create_time': usr.create_time,
                    'update_time': usr.update_time,
                })

            context['user'] = admin.account
            print(context)

        except Exception:
            return web_render(request, 'login.index.html', context=context)

        return web_render(request, 'dashboard.index.html', context=context, user=user)

    return web_render(request, 'dashboard.index.html', context=context)


def user_cash_log(request):
    pass
