from django.shortcuts import render
from utils.tools import get_admin_uid_cookie, get_user_account
from utils.html_render import web_render
from login.models import PageName, UserManagers, UserAuthorize, Admin
from django.views.decorators.csrf import csrf_exempt

import json


# Create your views here.
@csrf_exempt
def admin_dashboard(request):
    context = {}

    uid = get_admin_uid_cookie(request)
    user = {
        'uid': uid,
    }

    if request.method == 'GET':
        admins = UserManagers.objects.all()

        # select box
        context['admin_lv'] = '<td><table class="admin_manage" width="100%"><tr>'
        context['admin_lv'] += '<td><select class="manage_lv">' \
                               '<option value=4>管理員</option>' \
                               '<option value=3>主管級</option>' \
                               '<option value=2>企劃/活動</option>' \
                               '<option value=1>一般</option>' \
                               '</select></td>' \
                               '<td><select class="manager">'
        for admin in admins:
            context['admin_lv'] += '<option value="{}">{}</option>'.format(admin.uid, admin.account)

        context['admin_lv'] += '</select></td></tr>'

        # checkbox
        page_list = PageName.objects.all()
        context['page_auth'] = '<tr>'
        for page in page_list:
            # print(page.name)
            context['page_auth'] += '<td>' \
                                    '<p>{}</p>' \
                                    '<p><input type="checkbox" class="auth" name="{}" value="r" />{}</p>' \
                                    '<p><input type="checkbox" class="auth" name="{}" value="u" />{}</p>' \
                                    '<p><input type="checkbox" class="auth" name="{}" value="d" />{}</p></td>' \
                                    ''.format(page.name, page.id, '閱讀', page.id, '修改', page.id, '刪除')

        context['page_auth'] += '</tr></table></td>'
        # user account
        context['user'] = get_user_account(uid)

        render_context = web_render(request, 'dashboard.admin_dashboard.html', context=context, user=user)
        resp = render(request, 'dashboard.admin_dashboard.html', context=render_context)
        return resp

    if request.method == 'POST':
        # print(request.body)
        post_data = json.loads(request.body)

        # cannot update myself
        if post_data['manager'] == uid:
            render_context = web_render(request, 'dashboard.admin_dashboard.html', context=context, user=user)
            resp = render(request, 'dashboard.admin_dashboard.html', context=render_context)
            return resp

        auth = '000'
        auth_list = {}
        for key in post_data:

            if key == 'manage_lv':
                manage_lv = post_data[key]
                continue

            if key == 'manager':
                manager = post_data[key]
                continue

            tmp_auth = auth
            if 'r' in post_data[key]:
                tmp_auth = tmp_auth[:2] + '1'

            if 'u' in post_data[key]:
                tmp_auth = tmp_auth[0] + '1' + tmp_auth[2]

            if 'd' in post_data[key]:
                tmp_auth = '1' + tmp_auth[1:]

            auth_list[key] = tmp_auth

        # print(manager, manage_lv, auth_list)
        try:
            # update user authorize
            for key in auth_list:
                UserAuthorize.objects.filter(
                    uid=post_data['manager'], page=key
                ).update(
                    authorize=auth_list[key]
                )

        except Exception as e:
            print(e)
            render_context = web_render(request, 'dashboard.admin_dashboard.html', context=context, user=user)
            resp = render(request, 'dashboard.admin_dashboard.html', context=render_context)
            return resp


        render_context = web_render(request, 'dashboard.admin_dashboard.html', context=context, user=user)
        resp = render(request, 'dashboard.admin_dashboard.html', context=render_context)
        return resp


@csrf_exempt
def admin_addadmin(request):
    context = {}

    uid = get_admin_uid_cookie(request)
    user = {
        'uid': uid,
    }

    if request.method == 'GET':
        render_context = web_render(request, 'dashboard.addadmin.html', context=context, user=user)
        resp = render(request, 'dashboard.addadmin.html', context=render_context)
        return resp

    if request.method == 'POST':
        post_data = json.loads(request.body)
        import hashlib
        post_data['password'] = hashlib.sha1(post_data['password'].encode('utf-8')).hexdigest()
        # print(post_data)

        try:
            obj, created = UserManagers.objects.filter(account=post_data['account']).get_or_create(**post_data)
            if not created:
                print(created, usr.uid)
                render_context = web_render(request, 'dashboard.addadmin.html', context=context, user=user)
                resp = render(request, 'dashboard.addadmin.html', context=render_context)
                return resp

            usr = UserManagers.objects.get(**post_data)

            # 新增開始
            # print(usr.uid)

            pages = PageName.objects.all()
            queryset = []
            for page in pages:
                queryset.append(UserAuthorize(uid=usr.uid,page=page.id,authorize="000"))

            UserAuthorize.objects.bulk_create(queryset)

            Admin.objects.create(uid=usr.uid, manage_lv=1)

        except Exception as e:
            print(e)
            render_context = web_render(request, 'dashboard.addadmin.html', context=context, user=user)
            resp = render(request, 'dashboard.addadmin.html', context=render_context)
            return resp

        render_context = web_render(request, 'dashboard.addadmin.html', context=context, user=user)
        resp = render(request, 'dashboard.addadmin.html', context=render_context)
        return resp
