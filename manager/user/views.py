from django.shortcuts import render
from decorators.cookie import check_cookie
from utils.tools import get_admin_uid_cookie
from utils.html_render import web_render
from login.models import UserAuthorize, UserManagers
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
            admin = UserAuthorize.objects.get(uid=uid, page='user/list')
            if not admin:
                return web_render(request, 'login.index.html', context=context)

            # check authorize
            authorize = admin.authorize
            if authorize[2] == '0':
                return web_render(request, 'login.index.html', context=context)

            # print(authorize)
            upd_btn = '' if authorize[1] == '0' else '<input type="button" id="upd_btn" value="修改" />'
            del_btn = '' if authorize[0] == '0' else '<input type="button" id="del_btn" value="刪除" />'
            # get all user
            user_list = Users.objects.all()
            context['user_list'] = '<td><table width=100%>' \
                                   '<tr><td>{}</td>' \
                                   '<td>{}</td>' \
                                   '<td>{}</td>' \
                                   '<td>{}</td>' \
                                   '<td>{}</td>' \
                                   '<td>{}</td></tr>'.format('ID', 'user_account', 'user_name', 'create_time',
                                                                       'update_time', 'authorize function')
            for usr in user_list:
                context['user_list'] += '<tr><td>{}</td>' \
                                        '<td>{}</td>' \
                                        '<td>{}</td>' \
                                        '<td>{}</td>' \
                                        '<td>{}</td>' \
                                        '<td>{} {}</td></tr>' \
                                        ''.format(usr.id, usr.account, usr.name, usr.create_time, usr.update_time,
                                                  upd_btn, del_btn)

            context['user_list'] += '</table></td>'

            context['user'] = get_user_account(uid)
            # print(context)

        except Exception as e:
            print(e)
            return web_render(request, 'login.index.html', context=context)

        # print(context)
        render_context = web_render(request, 'dashboard.index.html', context=context, user=user)
        resp = render(request, 'dashboard.user_list.html', context=render_context)
        resp.set_cookie('admin_uid', user['uid'])
        return resp

    return web_render(request, 'dashboard.index.html', context=context)


def user_cash_log(request):
    pass


# get user account by uid
def get_user_account(uid):
    try:
        usr = UserManagers.objects.get(uid=uid)

        if not usr:
            raise

    except Exception as e:
        raise e

    return usr.account
