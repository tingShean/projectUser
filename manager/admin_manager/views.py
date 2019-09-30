from django.shortcuts import render
from utils.tools import get_admin_uid_cookie, get_user_account
from utils.html_render import web_render
from login.models import PageName, UserManagers
from django.views.decorators.csrf import csrf_exempt


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
        print(request.body)

        render_context = web_render(request, 'dashboard.admin_dashboard.html', context=context, user=user)
        resp = render(request, 'dashboard.admin_dashboard.html', context=render_context)
        return resp


def admin_addadmin(request):
    pass
