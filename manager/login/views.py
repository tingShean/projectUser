from django.shortcuts import render
# from django.http import HttpResponse
from utils.html_render import web_render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.template import loader
from .serializers import UserManagersSerializer, UserManagersAddSerializer, UserAuthorizeGetSerializer, PageNameGetSerializer

import json


# Create your views here.
@csrf_exempt
def index(request):
    """
    Login index page
    :param request:
        - GET show login page
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.index.html', context={})

    elif request.method == 'POST':
        # print(request.POST)
        try:
            import hashlib
            data = {
                'account': request.POST['account'],
                'password': hashlib.sha1(request.POST['password'].encode('utf-8')).hexdigest(),
            }
            # login success
            serializer = UserManagersSerializer(data=data)
            if serializer.is_valid():
                uid = serializer.data['uid']

                user = {
                    'uid': uid,
                }

                # bar list
                bar_serializer = UserAuthorizeGetSerializer(data=user)

                if not bar_serializer.is_valid():
                    print(bar_serializer.errors)
                    return render(request, 'login.index.html', context={})

                # print(bar_serializer.validated_data['bar_list'])
                bar_list = bar_serializer.validated_data['bar_list']

                page = {}
                page_list = []
                page_title = ''
                bar_context = ''
                # get bar list by authorize
                for bar in bar_list:
                    page['id'] = bar['page']

                    page_serializer = PageNameGetSerializer(data=page)
                    if not page_serializer.is_valid():
                        print(page_serializer.errors)
                        return render(request, 'login.index.html', context={})

                    if not page_title:
                        page_title = page_serializer.validated_data['title']
                        bar_context += '<tr><td>' \
                                       '<h3>{}</h3>' \
                                       '</td></tr>'.format(page_title)

                    elif page_serializer.validated_data['title'] != page_title:
                        page_title = page_serializer.validated_data['title']
                        bar_context += '<tr><td>' \
                                  '<h3>{}</h3>' \
                                  '</td></tr>'.format(page_title)

                    bar_context += '<tr><td>' \
                                   '<a href="./{}/">{}</a></br>' \
                                   '</td></tr>'.format(page_serializer.validated_data['id'], page_serializer.validated_data['name'])

                # print(bar_context)

                context = {
                    'user': serializer.validated_data['account'],
                    # 'bar_list': bar_serializer.validated_data['bar_list'],
                    'bar_context': bar_context,
                }
                # render_context = web_render(request, 'dashboard.index.html', context=context, c_key='admin_uid', c_val=uid)
                resp = render(request, 'dashboard.index.html', context=context)
                resp.set_cookie('admin_uid', uid)
                # return web_render(request, 'dashboard.index.html', context=context, c_key='admin_uid', c_val=uid)
                return resp

            # print(serializer.errors)

        except Exception as e:
            print('error', e)
            return web_render(request, 'login.index.html', context={})

        return web_render(request, 'login.index.html', context={})


@csrf_exempt
def add_user(request):
    """
    Add new user manager
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'dashboard.adduser.html', context={})

    elif request.method == 'POST':
        try:
            import hashlib
            data = json.loads(request.body.decode('utf-8'))
            # print(data)

            data['password'] = hashlib.sha1(data['password'].encode('utf-8')).hexdigest()
            # print(data)
            context = {
                'status': 0,
                'msg': 'user added',
            }

            serializer = UserManagersAddSerializer(data=data)
            if serializer.is_valid():
                # print(serializer.data)
                serializer.save()

                return JSONRenderer(context)

            # print(serializer.errors)

        except Exception as e:
            print(e)
            context = {
                'status': 1,
                'error_code': '999',
                'msg': 'Add user got error',
            }

        return render(request, 'dashboard.adduser.html', context=context)
